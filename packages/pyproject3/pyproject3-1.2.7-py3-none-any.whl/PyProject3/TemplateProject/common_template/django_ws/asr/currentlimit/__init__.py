"""并发控制模块.
限制每个客户能同时接入的并发数，以及整个 asr 服务总的并发数。
"""

import pathlib

from django.conf import settings
from django_redis import get_redis_connection
from redis import Redis


def init():
    """模块加载时执行一些初始化操作."""
    # 读取同目录下的三个 lua 脚本
    cur_dir = pathlib.Path(__file__).parent
    with open(file=cur_dir.joinpath("generate.lua"), mode="r", encoding="utf8") as file:
        generate_lua_code = file.read()
    with open(file=cur_dir.joinpath("renew.lua"), mode="r", encoding="utf8") as file:
        renew_lua_code = file.read()
    with open(
        file=cur_dir.joinpath("terminate.lua"), mode="r", encoding="utf8"
    ) as file:
        terminate_lua_code = file.read()
    # 将 lua 脚本缓存到 redis，避免后续的网络开销
    redis_client: Redis = get_redis_connection()
    return (
        redis_client.register_script(script=generate_lua_code),
        redis_client.register_script(script=renew_lua_code),
        redis_client.register_script(script=terminate_lua_code),
    )


generate_script, renew_script, terminate_script = init()


class ExceedAppMaxOccursExcepttion(Exception):
    """超过 app 的并发限制."""


class ExceedMaxOccursExcepttion(Exception):
    """超过总的并发限制."""


def generate_session_id(app_id: str | int, app_max_occurs: int) -> str:
    """生成一个会话 id.

    Args:
        app_id：申请创建会话的 app_id。
        app_max_occurs：该 app 允许的最大并发数。

    return:
        session_id：str 类型的会话 id。

    Excepthon：
        ExceedAppMaxOccursExcepttion：超过 app 的并发限制。
        ExceedMaxOccursExcepttion：超过总的并发限制。

    """
    session_id = generate_script(
        keys=[
            settings.SESSION_SET,
            settings.APP_SESSION_SET.format(app_id=app_id),
            settings.ASR_SESSION_COUNT,
        ],
        args=[
            app_max_occurs,
            settings.ASR_MAX_OCCURS,
            settings.ASR_SESSION_EXPIRE_TIME,
        ],
        client=get_redis_connection(),
    )
    if session_id == -1:
        raise ExceedAppMaxOccursExcepttion
    if session_id == -2:
        raise ExceedMaxOccursExcepttion
    assert isinstance(session_id, bytes)
    return session_id.decode()


def renew(app_id: str | int, session_id: str):
    """对 session id 进行续约.

    Args:
        app_id：session_id 所属的应用 id。
        session_id：要续约的会话 id。

    return:
        1：续约成功。
        -1：续约失败，session_id 已过期或不存在。
    """
    return renew_script(
        keys=[
            settings.SESSION_SET,
            settings.APP_SESSION_SET.format(app_id=app_id),
        ],
        args=[
            session_id,
            settings.ASR_SESSION_EXPIRE_TIME,
        ],
        client=get_redis_connection(),
    )


def terminate(app_id: str | int, session_id: str):
    """删除（结束） session_id.

    Args:
        app_id：session_id 所属的应用 id。
        session_id：要删除的会话 id。

    return:
        1：删除成功。
        0：删除失败，session_id 已过期或不存在。
    """
    return terminate_script(
        keys=[settings.APP_SESSION_SET.format(app_id=app_id), settings.SESSION_SET],
        args=[session_id],
        client=get_redis_connection(),
    )


__all__ = [
    "generate_session_id",
    "renew",
    "terminate",
    "ExceedAppMaxOccursExcepttion",
    "ExceedMaxOccursExcepttion",
]
