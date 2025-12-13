"""返回给调用方的返回信息."""

import json
from dataclasses import asdict, dataclass


@dataclass
class ASRReponse:
    """返回信息."""

    code: int
    message: str

    def dumps(self) -> str:
        """返回本实例转 json 后再序列化成的字符串."""
        return json.dumps(asdict(self), ensure_ascii=False)

    def __str__(self) -> str:
        """返回本实例的字符串表示."""
        return self.dumps()


@dataclass
class MissParamError:
    """参数错误."""

    code: int = 10040100
    message: str = ""

    def dumps(self) -> str:
        """返回本实例转 json 后再序列化成的字符串."""
        return json.dumps(asdict(self), ensure_ascii=False)

    def __str__(self) -> str:
        """返回本实例的字符串表示."""
        return self.dumps()


@dataclass
class ConnectSuccess(ASRReponse):
    """连接成功."""

    code: int = 10020000
    message: str = "成功创建 session"
    session_id: str = ""

    def __init__(self, session_id: str):
        self.session_id = session_id


APP_NOT_FOUND = ASRReponse(code=100404000, message="App 不存在")


MISS_AUTH_PARAM = MissParamError(message="缺少 signature 参数")


AUTHORIZEDFAILED = ASRReponse(code=10040101, message="身份验证失败")


EXCEED_APP_MAX_OCCURS = ASRReponse(code=100429000, message="超过 APP 的最大并发请求数")

EXCEED_MAX_OCCURS = ASRReponse(code=100503000, message="超过 ASR 服务总的最大并发限制")

SERVER_ERROR = ASRReponse(code=100500000, message="连接算法服务出错")

SOCKET_TIMEOUT = ASRReponse(10040101, "socket 超时")


if __name__ == "__main__":
    r = ConnectSuccess(session_id="123")
    print(r.dumps())
