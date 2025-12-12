from demo_app.model_vendors.abstract_vendor import AbstractModelVendor
import json
from typing import Dict, List


class Demo1ModelVendor(AbstractModelVendor):
    """非标准 大模型1"""

    def __init__(self, base_url: str, api_key: str):
        super().__init__(base_url, api_key)

    def create_chat_completion_stream(self, messages: List[Dict[str, str]]):
        """调用非标准 API 并返回流式响应（同步版本）"""
        data = {
            "model": "your-model",
            "input": messages,
            "reasoning": {"effort": "medium"},
            "stream": True
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}
        with self.client.stream(
            "POST",
            f"{self.base_url}/chat",
            json=data,
            headers=headers
        ) as response:
            for line in response.iter_lines():
                if line:
                    yield json.loads(line)

    def create_chat_completion(self, messages: List[Dict[str, str]]):
        """调用非标准 API 并返回非流式响应（同步版本）"""
        data = {
            "model": "your-model",
            "input": messages,
            "reasoning": {"effort": "medium"},
            "stream": False
        }

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = self.client.post(
            f"{self.base_url}/chat",
            json=data,
            headers=headers
        )
        return response.json()