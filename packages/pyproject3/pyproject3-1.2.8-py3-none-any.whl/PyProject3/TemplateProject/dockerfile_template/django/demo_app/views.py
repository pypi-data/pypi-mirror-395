from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from django.http import JsonResponse, StreamingHttpResponse
from rest_framework.response import Response
import json
import logging

from demo_app.serializers import ChatCompletionSerializer
from demo_app.model_vendors.demo1_vendor import Demo1ModelVendor
from demo_app.model_vendors.demo2_vendor import Demo2ModelVendor
from demo_app.model_adapters.openai_adapter import OpenAIAdapter


logger = logging.getLogger("django.logger")


class DemoChatCompletionView(APIView):
    """
    OpenAI API 兼容接口示例。
    这是一个测试接口示例，实际使用时，请使用自己的 API 接口。
    
    # curl -X POST http://localhost:8000/demo_app/v1/chat/completions \
    curl -X POST http://localhost:9000/demo_app/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"stream": true, "model": "gpt-4o-mini-search-preview", "messages": [{"role": "user", "content": "上海天气怎么样？"}]}'
    
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Demo2ModelVendor(
            base_url="https://test-llmops.xmov.ai/api/", api_key="fastgpt-eTkOQLwapEDSjvKEy5V8ouwzjWCvHLygjIGrnV9L12gYEaFVVksYSCSFXf")

    def get(self, request):
        logger.info("Hello, it works! get request")
        return JsonResponse({"message": "Hello, it works!"})

    def post(self, request):
        logger.info("Hello, it works! post request")
        try:
            serializer = ChatCompletionSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=400)
            messages = [{"role": msg["role"], "content": msg["content"]}
                        for msg in serializer.validated_data["messages"]]
            # 检查是否请求流式响应
            stream = request.data.get("stream", False)
            if stream:  # 流式响应处理
                return StreamingHttpResponse(
                    self._generate_stream(messages),
                    content_type="text/event-stream"
                )
            else:  # 非流式响应处理
                response = self.client.create_chat_completion(messages)
                openai_response = OpenAIAdapter.convert_to_openai_format(response)
                return JsonResponse(openai_response)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def _generate_stream(self, messages):
        """生成流式响应的生成器函数"""
        # 使用同步方式处理流式响应
        for chunk in self.client.create_chat_completion_stream(messages):
            chunk_data = OpenAIAdapter.convert_chunk_to_openai_format(chunk)
            json_data = chunk_data.model_dump_json()
            yield f"data: {json_data}\n\n"
        yield "data: [DONE]\n\n"
