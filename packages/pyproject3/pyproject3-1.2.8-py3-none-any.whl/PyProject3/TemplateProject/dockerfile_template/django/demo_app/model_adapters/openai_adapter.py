import time
from openai.types.chat.chat_completion_chunk import (
    Choice,
    ChatCompletionChunk,
    ChoiceDelta,
    CompletionUsage
)
from ..types.chunk import ModelVendorChunk


class OpenAIAdapter:
    """OpenAI 格式适配器"""
    @staticmethod
    def convert_chunk_to_openai_format(
            chunk: ModelVendorChunk
    ) -> ChatCompletionChunk:
        """
        {"id":"","object":"","created":0,"model":"","choices":[{"delta":{"role":"assistant","content":"\n\n上海"},"index":0,"finish_reason":null}]}
        """
        choice_delta = ChoiceDelta(
            role="assistant",
            content=chunk.content,
            tool_calls=None,
            function_call=None
        )

        choice = Choice(
            finish_reason=None if not chunk.done else "stop",
            index=0,
            delta=choice_delta
        )

        return ChatCompletionChunk(
            id=f"adapted-{time.time()}",
            object="chat.completion.chunk",
            created=int(time.time()),
            model="adapted-model",
            choices=[choice]
        )

    @staticmethod
    def convert_to_openai_format(
        response: ModelVendorChunk
    ) -> ChatCompletionChunk:
        """将非标准 API 响应转换为 OpenAI 格式"""

        choice_delta = ChoiceDelta(
            role="assistant",
            content=response.content,
            tool_calls=None,
            function_call=None
        )

        choice = Choice(
            index=0,
            delta=choice_delta,
            finish_reason="stop" if response.done else None
        )
        usage = CompletionUsage(
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0
        )

        return ChatCompletionChunk(
            id=f"adapted-{time.time()}",
            choices=[choice],
            created=int(time.time()),
            object="chat.completion.chunk",
            model="adapted-model",
            usage=usage
        )
