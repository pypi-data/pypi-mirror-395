"""数据库模型."""


import random
import string
from typing import Annotated, Literal, NotRequired, TypedDict

from annotated_types import Gt, MinLen
from django.db import models
from django_pydantic_field import SchemaField
from ninja import Field, Schema
from pydantic import field_validator, ValidationError


def generate_password():
    # 定义密码字符集
    characters = string.ascii_letters + string.digits
    # 确保密码中至少包含一个小写字母、一个大写字母、一个数字
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
    ]

    # 填充剩余的密码长度
    password += random.choices(characters, k=6)

    # 打乱密码列表中的元素顺序
    random.shuffle(password)

    # 将列表转换为字符串
    return "".join(password)


class ReplaceWord(Schema):
    """词改写."""

    old: str = Field(title="目标词(不能空)", min_length=1)
    new: str = Field(title="改写词")

    count: int = Field(default=0, title="改写次数，0 表示不限", ge=0)

    @field_validator("old")
    @classmethod
    def new_empty_word(cls, v: str | None) -> str:
        if v is None or len(v.strip()) == 0:
            raise ValueError("目标词不能为空")
        return v


class HotWordConfigs(Schema):
    name: str = Field(title="名字")
    score: float = Field(default=20, title="分数(范围10-50)", ge=10, le=50)


DEFAULT_SVS_LANGS = ['auto', 'zh', 'en', 'ja', 'ko', 'yue']


class SvsLangs(models.TextChoices):
    AUTO = "auto", "auto"
    ZH = "zh", "zh"
    EN = "en", "en"


class AsrAppConfig(Schema):
    """配置."""

    mode: Literal["2pass", "offline"] = Field(
        default="2pass", description="模式，offline 是离线模式"
    )

    chunk_size: list[Annotated[int, Gt(0)]] = Field(
        default_factory=lambda: [5, 10, 5], min_length=3, max_length=3
    )

    chunk_interval: int = Field(default=10, gt=0)

    wav_name: Literal["microphone"] = Field(default="microphone")

    hotword_scores: list[HotWordConfigs] = Field(default_factory=list, title="热词和分数")

    replace_words: list[ReplaceWord] = Field(default_factory=list, title="词改写列表")

    secret: str = Field(
        title="授权码",
        default_factory=generate_password,
        description="身份校验时需要的授权码",
    )

    max_workers: int = Field(default=10, title="最大并发数", ge=1)

    itn: bool = Field(
        title="是否将中文数字转成阿拉伯数字",
        default=True,
        description="是否将中文数字转成阿拉伯数字，例如一二三转成 123。fasle 表示不启用；true 表示启用",
    )

    vad_tail_sil: int = Field(
        title="VAD 的尾部静音长度，单位毫秒",
        default=800,
        description="VAD 的尾部静音长度，如果静音时间超过这个值，VAD 会在此处进行一次切分。单位毫秒，如果不设该值，默认取 800",
        ge=1,
    )

    vad_max_len: int = Field(
        title="VAD 切分的最大音频长度，单位毫秒",
        default=60000,
        description="VAD 切分的最大音频长度，单位毫秒。如果不设该值，默认取 60000",
    )


class AsrApp(models.Model):
    """ASR App."""

    id = models.BigAutoField(primary_key=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=60, verbose_name="应用名称")

    config = SchemaField(
        schema=AsrAppConfig, verbose_name="应用配置", help_text="大多数选项只需保持默认"
    )

    svs_lang = models.CharField(max_length=20, choices=SvsLangs, default=SvsLangs.AUTO)


    def __str__(self) -> str:
        return self.name

    class Meta:
        """元数据."""

        ordering = ("-create_time",)
        verbose_name = "ASR 应用"
        verbose_name_plural = verbose_name
        app_label = "asr"


class HotWords(models.Model):
    """热词."""

    id = models.BigAutoField(primary_key=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    app = models.ForeignKey(AsrApp, on_delete=models.CASCADE, related_name="hotwords")
    word = models.CharField(max_length=30, verbose_name="热词")

    class Meta:
        ordering = ("-create_time",)
        verbose_name = "热词"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=["app_id", "word"], name="u_app_word")
        ]


class SubstituteWords(models.Model):
    """改写词."""

    id = models.BigAutoField(primary_key=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    org_term = models.CharField(max_length=30, verbose_name="目标词")

    des_term = models.CharField(max_length=30, verbose_name="改写词")

    app = models.ForeignKey(
        AsrApp, on_delete=models.CASCADE, related_name="substitutewords"
    )

    count = models.IntegerField(
        default=1,
        verbose_name="改写次数",
        help_text="大于 0 表示具体的改写次数，0 表示不限制次数",
    )

    class Meta:
        ordering = ("-create_time",)
        verbose_name = "词改写"
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(
                fields=["app_id", "org_term"], name="u_app_org_term"
            )
        ]


class SpeechFormat(TypedDict):
    """音频格式."""

    encoding: str  # 音频编码格式，当前只有一个 PCM
    sampling_rate: int  # 采样率

    # 例如 s16le：s（signed integer）表示样本为有符号整数，16 表示位宽为 16 个 bit，le 表示小端
    sample_format: str  # 样本格式：整数还是浮点数、位宽、大小端，例如 s16le


class Speech(TypedDict):
    """语音信息."""

    bucket_name: str  # 语音文件在 minio 上所属的 bucket
    object_name: str  # 语音文件在 minio 上的对象名

    dur: int  # 时长，单位毫秒

    format: SpeechFormat  # 音频格式


class AsrResult(TypedDict):
    """语音识别结果."""

    create_time: int  # 创建时间，单位毫秒

    # start_ts: int  # 相对于音频的起始时间戳，单位毫秒
    # end_ts: int  # 相对于音频的结束时间戳，单位毫秒

    text: str  # 从语音识别出的文本

    post_text: NotRequired[str]  # 处理后发送给调用方的文本


class AsrRecord(models.Model):
    """语音识别记录.

    客户可能需要下载语音和识别文字，算法也可能需要识别结果来改进算法，所以得保存下来.
    """

    id = models.BigAutoField(primary_key=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    app = models.ForeignKey(
        to=AsrApp,
        on_delete=models.DO_NOTHING,
        related_name="records",
        help_text="该记录所属 app",
    )

    session_id = models.CharField(
        max_length=128, verbose_name="会话标识", help_text="每次 ASR 会话都有唯一标识"
    )

    asr_model_version = models.CharField(
        max_length=8, verbose_name="算法模型版本", help_text="asr 算法模型的版本号"
    )

    session_args = models.JSONField(verbose_name="会话参数")

    speeches: list[Speech] = models.JSONField(verbose_name="语音数据列表", default=list)  # type: ignore

    asr_results: list[AsrResult] = models.JSONField(
        verbose_name="识别结果列表", default=list
    )  # type: ignore

    class Meta:
        """元数据."""

        ordering = ("-create_time",)
        verbose_name = "语音识别记录"
        verbose_name_plural = verbose_name
        app_label = "asr"
