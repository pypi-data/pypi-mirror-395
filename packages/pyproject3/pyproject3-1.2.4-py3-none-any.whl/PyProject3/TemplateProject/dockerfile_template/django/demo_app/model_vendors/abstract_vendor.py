import httpx
from typing import Dict, Any, List


class AbstractModelVendor:
    """抽象 API 客户端"""
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.Client()  # 改用同步客户端

    def create_chat_completion_stream(self, messages: List[Dict[str, str]]):
        """抽象方法，子类必须实现
        :param messages: 历史消息列表
        :return: 流式响应
        """
        raise NotImplementedError("子类必须实现 create_chat_completion_stream 方法")

    def create_chat_completion(self, messages: List[Dict[str, str]]):
        """抽象方法，子类必须实现
        """
        raise NotImplementedError("子类必须实现 create_chat_completion 方法")
