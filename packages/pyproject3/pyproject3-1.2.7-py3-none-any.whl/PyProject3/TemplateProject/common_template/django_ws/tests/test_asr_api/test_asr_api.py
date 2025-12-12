# coding: utf-8
from make_signature import make_signature

def test_make_signature():
    params = {
        "app_id": 13,
        "timestamp": 1733251200,
        "nonce": "1234567890"
    }
    secret = "123456"
    signature = make_signature(params, secret)
    print(signature)

 
