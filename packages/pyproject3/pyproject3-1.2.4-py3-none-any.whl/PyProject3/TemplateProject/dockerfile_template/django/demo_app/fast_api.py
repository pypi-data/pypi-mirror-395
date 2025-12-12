from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import time
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator, List, Dict, Any, Optional
from pydantic import BaseModel
import time
import json
import asyncio
from openai.types.chat import ChatCompletion, ChatCompletionMessage, Choice
import httpx

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.7
    timeout: Optional[int] = 30

class NonStandardAPIClient:
    """非标准 API 客户端"""
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.AsyncClient()
    
    async def create_chat_completion_stream(self, messages: List[Dict[str, str]]) -> AsyncGenerator[Dict[str, Any], None]:
        """调用非标准 API 并返回流式响应"""
        data = {
            "model": "your-model",
            "input": messages,
            "reasoning": {"effort": "medium"},
            "stream": True  # 启用流式响应
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with self.client.stream(
            "POST",
            f"{self.base_url}/chat",
            json=data,
            headers=headers
        ) as response:
            async for chunk in response.aiter_lines():
                if chunk:
                    yield json.loads(chunk)

class OpenAIAdapter:
    """OpenAI 格式适配器"""
    @staticmethod
    def convert_chunk_to_openai_format(chunk: Dict[str, Any]) -> Dict[str, Any]:
        # 将非标准流式响应块转换为 OpenAI 格式
        message = ChatCompletionMessage(
            role="assistant",
            content=chunk.get("content", ""),
            function_call=None,
            tool_calls=None
        )
        
        choice = Choice(
            finish_reason=None if not chunk.get("done") else "stop",
            index=0,
            message=message
        )
        
        return {
            "id": f"adapted-{time.time()}",
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "adapted-model",
            "choices": [choice],
        }

@app.post("/v1/chat/completions")
async def create_chat_completion(request: ChatCompletionRequest):
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # 检查是否请求流式响应
        stream = request.dict().get("stream", False)
        
        if stream:
            async def generate_stream():
                async for chunk in non_standard_client.create_chat_completion_stream(messages):
                    yield f"data: {json.dumps(OpenAIAdapter.convert_chunk_to_openai_format(chunk))}\n\n"
                yield "data: [DONE]\n\n"
            
            return StreamingResponse(
                generate_stream(),
                media_type="text/event-stream"
            )
        else:
            # 非流式响应处理
            response = await non_standard_client.create_chat_completion(messages)
            return OpenAIAdapter.convert_to_openai_format(response)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)