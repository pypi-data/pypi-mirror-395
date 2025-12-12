"""通过 websocket 协议提供的 asr 服务."""

import asyncio
import json
import logging
import os
import time
from typing import override
from urllib.parse import parse_qs

import websockets
import websockets.asyncio
import websockets.asyncio.client
import websockets.client
import websockets.exceptions
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from response import (
    APP_NOT_FOUND,
    AUTHORIZEDFAILED,
    EXCEED_APP_MAX_OCCURS,
    EXCEED_MAX_OCCURS,
    MISS_AUTH_PARAM,
    SERVER_ERROR,
    SOCKET_TIMEOUT,
    ConnectSuccess,
    MissParamError,
)
from util import verify_sign

from . import currentlimit
from .models import AsrApp, AsrRecord, AsrResult, Speech, SpeechFormat, HotWordConfigs
from .objectstorre import StreamUploadThread

logger = logging.getLogger("common.logger")


# todo,创建续约任务
class AsrConsumer(AsyncWebsocketConsumer):
    """响应 ASR WebSocket 请求."""

    def __init__(self, *args, **kwargs):
        """每来一个 websocket 连接都会创建一个该实例."""
        super().__init__(*args, **kwargs)
        self.is_started = False
        self.params = {}
        self.app: AsrApp | None = None
        self.session_id = ""

        # 本服务到 asr 推理服务的 websocket 连接.
        self.server_ws: websockets.asyncio.client.ClientConnection | None = None
        self.server_recv_task: asyncio.Task | None = None

        # 音频数据上传线程
        self.voice_upload_tread: StreamUploadThread | None = None

        self.asr_record: AsrRecord | None = None  # asr 记录
        self.renew_task: asyncio.Task | None = None  # 续约任务

    @override
    async def connect(self):
        """继承自基类，该方法会在收到连接请求时触发."""
        logger.info("收到来自 %s 的 websocket 连接请求", self.scope["client"])
        try:
            logger.info("提取请求参数")
            self.params = parse_qs(self.scope["query_string"].decode())

            # 按照原项目的逻辑，先接受连接，验证不合法就发送错误信息并关闭连接.
            await self.accept()

            logger.info("验证参数")
            if not (await self._validate_params(self.params)):
                logger.warning("验证不通过，主动关闭连接")
                await self.close()
                return

            self.app = await AsrApp.objects.aget(id=self.params["app_id"][0])
            assert self.app is not None
            logger.info("当前 app=%d 的配置为：%s, 客户端: %s", self.app.id, self.app.config, self.scope["client"])
            logger.info("申请 session_id")
            try:
                self.session_id = currentlimit.generate_session_id(
                    app_id=self.app.id, app_max_occurs=self.app.config.max_workers
                )
                # 申请 session_id 后开启续约任务，避免 session_id 在 redis 中过期被删除
                self.renew_task = asyncio.create_task(
                    self._renew_session(self.app.id, self.session_id)
                )
            except currentlimit.ExceedAppMaxOccursExcepttion:
                logger.warning("超过 APP 的并发限制")
                await self.send(text_data=EXCEED_APP_MAX_OCCURS.dumps())
                await self.close()
            except currentlimit.ExceedMaxOccursExcepttion:
                logger.warning("超过服务的总并发限制")
                await self.send(text_data=EXCEED_MAX_OCCURS.dumps())
                await self.close()

            logger.info("连接服务端")
            if not (await self._connect_to_server()):
                await self.close()
                return

            logger.info("向客户端发送连接成功的消息")
            await self.send(
                text_data=ConnectSuccess(session_id=self.session_id).dumps()
            )
            logger.info("已向客户端发送连接成功的消息")
        except Exception as e:
            logger.info(e, exc_info=True)
            logger.error(e, exc_info=True, stack_info=True)

    async def _validate_params(self, query_params: dict) -> bool:
        """验证请求参数."""
        # 当前 app_id 是否存在对应的配置 asr_config
        app_id = query_params["app_id"][0]
        app = await AsrApp.objects.filter(id=app_id).afirst()
        if app is None:
            logger.warning("找不到 app_id=%s 对应的配置", app_id)
            await self.send(text_data=APP_NOT_FOUND.dumps())
            return False

        if "signature" not in query_params:
            await self.send(text_data=MISS_AUTH_PARAM.dumps())
            return False
        if "timestamp" not in query_params:
            await self.send(text_data=MissParamError(message="缺少 timestamp").dumps())
            return False
        if int(time.time()) - int(query_params["timestamp"][0]) > int(
            os.environ.get("SOCKET_CONNECTION_TIMEOUT", 300)
        ):
            await self.send(text_data=SOCKET_TIMEOUT.dumps())
            return False
        signature = query_params.pop("signature")[0]
        if not verify_sign(query_params, signature, app.config.secret):
            await self.send(text_data=AUTHORIZEDFAILED.dumps())
            return False

        return True

    async def _connect_to_server(self):
        """创建到服务的连接."""
        uri = f"ws://{settings.ASR_SERVER_HOST}:{settings.ASR_SERVER_PORT}"
        try:
            self.server_ws = await websockets.asyncio.client.connect(
                uri=uri,
                subprotocols=[websockets.Subprotocol("binary")],
                ping_interval=None,
                ssl=None,
            )
        except (
            websockets.exceptions.InvalidURI,
            OSError,
            websockets.exceptions.InvalidHandshake,
            TimeoutError,
            asyncio.TimeoutError,
            Exception,
        ):
            logger.error("连接服务端出错", exc_info=True)
            await self.send(text_data=SERVER_ERROR.dumps())
            return False

        logger.info("连接服务端成功")
        return True

    @override
    async def disconnect(self, code):
        """继承自基类，websocket 连接断开后会触发该方法."""
        logger.info(f"已关闭来自自 {self.scope['client']} 的 websocket 连接请求, code: {code}")
        if self.session_id:
            assert self.app is not None
            if currentlimit.terminate(self.app.id, self.session_id) == 1:
                logger.info("成功从 redis 中删除 session_id=%s", self.session_id)
            else:
                logger.warning("从 redis 中删除 session_id=%s 失败!", self.session_id)

        if self.renew_task:
            if self.renew_task.cancel():
                logger.info("等待续约任务取消")
                try:
                    await self.renew_task
                except asyncio.CancelledError:
                    logger.info("续约任务已取消")
            else:
                logger.info("续约任务已被取消，无需重复取消")
            del self.renew_task
            self.renew_task = None

        if self.server_recv_task:
            if self.server_recv_task.cancel():
                logger.info("等待接收服务端消息的任务取消")
                try:
                    await self.server_recv_task
                except asyncio.CancelledError:
                    logger.info("接收服务端消息的协程任务已取消")
            else:
                logger.info("接收服务端消息的协程任务已被取消，无需重复取消")
            del self.server_recv_task
            self.server_recv_task = None

        if self.server_ws:
            await self.server_ws.close()
            del self.server_ws
            self.server_ws = None

        if self.voice_upload_tread:
            self.voice_upload_tread.append(b"")
            logger.info("等待音频上传线程退出.")
            self.voice_upload_tread.join()
            logger.info("音频上传线程已退出，保存音频关联数据")
            assert self.asr_record is not None
            self.asr_record.speeches.append(
                Speech(
                    bucket_name=settings.MINIO_BUCKET_NAME,
                    object_name=self.voice_upload_tread.obj_name,
                    dur=self.voice_upload_tread.obj_size // 32,
                    format=SpeechFormat(
                        encoding="PCM", sampling_rate=16000, sample_format="s16le"
                    ),
                )
            )
            await self.asr_record.asave()
            logger.info("保存完毕")
            del self.voice_upload_tread
            self.voice_upload_tread = None

    @override
    async def receive(self, text_data=None, bytes_data=None):
        """继承自基类，收到 websocket 消息时就会触发该消息."""
        assert self.server_ws is not None
        if not self.is_started:
            if text_data is None:
                logger.error("第一条指令不是文本类型")
                await self.close()
                return
            message = json.loads(text_data)
            signal = message.get("signal", "start")
            if signal != "start":
                logger.error("第一条指令不是 start")
                await self.close()
                return
            assert self.app is not None
            logger.info(f"从 {self.app.id} 读取热词")
            try:
                hotword_scores = self.app.config.hotword_scores
                logger.info(f"从 {self.app.id} 读到热词 {hotword_scores}")
                hotword_scores = {i.name: i.score for i in hotword_scores}
                input_hotwords = message.get("hotword_list", [])
                for i_hotword in input_hotwords:
                    if i_hotword not in hotword_scores:
                        hotword_scores[i_hotword] = HotWordConfigs.model_fields["score"].default
                logger.info(f"和消息中的热词汇总后，{hotword_scores}")
            except Exception as e:
                logger.error(e, exc_info=True, stack_info=True)
                raise e

            message = self.app.config.model_dump(
                exclude={"max_workers", "secret", "hotwords", "hotword_scores", "replace_words"}
            ) | {
                "is_speaking": True,
                "hotwords": json.dumps(hotword_scores),
            }
            message["svs_lang"] = self.app.svs_lang
            self.is_started = True
            await self.server_ws.send(json.dumps(message))
            self.server_recv_task = asyncio.create_task(self._receive_from_server())
            if settings.RECORD_VOICE:
                obj_name = f"asr/{self.app.id}/{self.session_id}"
                self.voice_upload_tread = StreamUploadThread(obj_name=obj_name)
                self.voice_upload_tread.start()
                self.asr_record = AsrRecord(
                    app=self.app,
                    session_id=self.session_id,
                    asr_model_version="2.0.0",
                    session_args=message,
                )
                await self.asr_record.asave()
            return

        if bytes_data is not None:
            voice_data = bytes_data
            await self.server_ws.send(voice_data)
            if self.voice_upload_tread:
                self.voice_upload_tread.append(voice_data)
        else:
            assert text_data is not None
            message = json.loads(text_data)
            signal = message.get("signal")
            if signal == "end":
                await self.server_ws.send(json.dumps({"is_speaking": False}))
                if not message.get("graceful_close"):
                    if self.voice_upload_tread:
                        self.voice_upload_tread.append(b"")
                    await self.close()
            else:
                logger.error("未识别的消息 %s", text_data)

    async def _receive_from_server(self):
        """接收来自服务端的 ws 消息并发送给调用方."""
        while True:
            try:
                assert self.server_ws is not None
                data = await self.server_ws.recv()
            except websockets.exceptions.ConnectionClosedError:
                logger.error("和服务端的连接异常关闭")
                await self.close()
                return
            except websockets.exceptions.ConnectionClosedOK:
                logger.info("和服务端的连接已正常关闭")
                await self.close()
                return
            except RuntimeError:
                logger.warning("结束服务端数据出错，可能是另一个协程任务在并发 recv")
                continue
            except asyncio.exceptions.CancelledError:
                logger.warning("收到协程取消信号")
                raise
            except:  # noqa: E722
                logger.error("未预料到的错误", exc_info=True)
                return

            try:
                msg = json.loads(data)
                text = msg["text"]
                assert self.app is not None
                if msg.get("mode") == "2pass-offline":
                    post_text = await self._term_replace(msg["text"])
                    if post_text != text:
                        rr = AsrResult(
                            create_time=int(time.time() * 1000),
                            text=text,
                            post_text=post_text,
                        )
                        text = post_text
                    else:
                        rr = AsrResult(create_time=int(time.time() * 1000), text=text)
                    if settings.RECORD_VOICE:
                        assert self.asr_record is not None
                        self.asr_record.asr_results.append(rr)
                        await self.asr_record.asave()

                # 发送给调用方
                await self.send(
                    text_data=json.dumps(
                        {
                            "type": (
                                "final_result"
                                if msg.get("mode") == "2pass-offline"
                                else "partial_result"
                            ),
                            "text": text,
                        }
                    )
                )
                if msg.get("is_final"):
                    logger.info("收到 asr 算法侧的结束消息，主动关闭到调用方的连接.")
                    await self.close()
            except:  # noqa: E722
                logger.error("未预料到的错误", exc_info=True)

    async def _term_replace(self, text: str) -> str:
        """词替换."""
        assert self.app is not None
        org_text = text
        for replace_word in self.app.config.replace_words:
            text = text.replace(
                replace_word.old,
                replace_word.new,
                replace_word.count if replace_word.count > 0 else -1,
            )
        if org_text != text:
            logger.info(f"“{org_text}”被替换成“{text}”")
        return text

    async def _renew_session(self, app_id: str | int, session_id: str):
        """对 session 循环续约直到被取消或检测到 session_id 已不存在."""
        while True:
            try:
                await asyncio.sleep(settings.ASR_SESSION_RENE_INTERVAL)
                if currentlimit.renew(app_id=app_id, session_id=session_id) == 1:
                    logger.info("续约成功 app_id=%s,session_id=%s", app_id, session_id)
                else:
                    logger.warning(
                        "续约失败 app_id=%s,session_id=%s", app_id, session_id
                    )
                    break
            except asyncio.CancelledError:
                logger.info(
                    "续约任务收到取消信号，开始退出, app_id=%s,session_id=%s",
                    app_id,
                    session_id,
                )
                break
            except:  # noqa: E722
                logger.error("续约异常", exc_info=True)
