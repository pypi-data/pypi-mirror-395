import hashlib
import hmac
from base64 import b64encode
from urllib import parse


def make_signature(params, secret=None):
    """对数据进行字段ASCII码排序验签

    :param params: 参数字典   
    :param secret: app 密钥    
    :return: str  
    """
    assert isinstance(params, dict)
    params_str = '&'.join(
        [f'{key}={params[key]}' for key in sorted(params.keys())])
    if secret is not None:
        params_str = hmac.new(secret.encode(
            'utf-8'), params_str.encode('utf-8'), hashlib.sha1).digest()
    else:
        params_str = params_str.encode('utf-8')
    signature = b64encode(params_str).decode('utf-8')
    return parse.quote(signature)
