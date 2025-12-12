"""工具模块."""

import hmac
import logging
from base64 import b64encode
from hashlib import sha1


def verify_sign(params: dict, sign_str, app_secret) -> bool:
    """对数据进行字段 ASCII 码排序验签.

    :param params:
    :param sign_str:
    :return:
    """
    sign = "&".join([f"{key}={params[key][0]}" for key in sorted(params.keys())])
    hmac_sign = hmac.new(
        app_secret.encode("utf-8"), sign.encode("utf-8"), sha1
    ).digest()
    b64_sign = b64encode(hmac_sign).decode("utf-8")
    return b64_sign == sign_str


def combine_objs_to_string(*args):
    """
    合并字符串
    :param args:
    :return:
    """
    try:
        format_string = "{}" * len(args)
        format_string = format_string.format(*args)
        return format_string
    except:  # noqa: E722
        logging.error(
            "combine_objs_to_string # there are some error happened", exc_info=True
        )
        return ""
