from demo_app.model_vendors.abstract_vendor import AbstractModelVendor
from demo_app.types.chunk import ModelVendorChunk


from typing import Dict, List


class Demo2ModelVendor(AbstractModelVendor):
    """非标准 大模型2"""

    def __init__(self, base_url: str, api_key: str):
        super().__init__(base_url, api_key)

    def create_chat_completion_stream(self, messages: List[Dict[str, str]]):
        """调用非标准 API 并返回流式响应（同步版本）"""
        lines = [
            "这",
            "是",
            "一",
            "个",
            "测",
            "试",
            "。",
        ]
        for idx, line in enumerate(lines):
            is_last = idx+1 == len(lines)
            yield ModelVendorChunk(content=line, done=is_last)