from collections import namedtuple

XmovError = namedtuple("XmovError", ["code", "message"])

SYSTEM_ERROR = XmovError(101, "系统异常，请联系管理员")

PARAMS_ERROR = XmovError(102, "缺少参数")

APP_ERROR = XmovError(201, "ASR服务授权失败")

APP_MAX_WORKERS_ERROR = XmovError(202, "ASR超过最大连接数")

APP_PROTOCOL_ERROR = XmovError(203, "ASR连接数据格式错误")

HOT_WORD_REPEAT_ERROR = XmovError(301, "热词已存在”")

TERM_REPEAT_ERROR = XmovError(302, "目标词已存在”")

SIGNATURE_ERROR = XmovError(303, "signature验证失败”")

MODEL_NO_EXIST_ERROR = XmovError(304, "模型不存在”")


class XmovException(Exception):
    """
    异常处理类
    """

    def __init__(self, error, *args, **kwargs):
        self.error = error
        self.message = error.message
        self.code = error.code
        super(XmovException, self).__init__(*args, **kwargs)
