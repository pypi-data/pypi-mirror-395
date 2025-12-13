# coding: utf-8
import time
import json
import websockets
from make_signature import make_signature
import asyncio
from schema import Args
from utils import parser_wav

args = Args()

async def run_send_task(ws, wav: str):
    """ 发送音频数据任务。
    Args:
        ws: websocket
        wav: str
    """
    audio_bytes, chunk_num, wav_name, stride, wave_length_seconds = parser_wav(wav, args)
    start_message = {
        "signal": "start", "hotword_list": []
    }
    await ws.send(json.dumps(start_message))
    for i in range(chunk_num):
        audio_chunk = audio_bytes[i * stride: (i + 1) * stride]
        if i % 20 == 0:
            print(f"send audio chunk {i} {len(audio_chunk)}")
        await ws.send(audio_chunk)
        await asyncio.sleep(0.06)
    blank_audio_600ms = b"\x00" * 1920 * 10
    await ws.send(blank_audio_600ms)
    for i in range(10):
        await asyncio.sleep(1)
        print(f"prepare to close websocket")
    stop_message = {
        "signal": "stop"
    }
    await ws.send(json.dumps(stop_message))
    await ws.close()
    print(f"websocket closed")

async def run_recv_task(ws):
    """ 接收ASR结果任务。
    Args:
        ws: websocket
    """
    try:
        while True:
            message = await ws.recv()
            # print(message)
            message = json.loads(message)
            print(f"message: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("WebSocket连接已关闭，停止接收消息")
    except Exception as e:
        print(f"接收消息时出错: {e}")


def make_url(app_id: int, secret: str, ASR_API_ENDPOINT: str) -> str:
    """ 生成 websocket url。
    Args:
        app_id: int
        secret: str
        ASR_API_ENDPOINT: str

    Returns:
        str: websocket url
    
    Examples:
        >>> make_url(15, "123456", "wss://test-asr-api.xmov.ai/ws/asr/")
        "wss://test-asr-api.xmov.ai/ws/asr/?app_id=15&timestamp=1733251200&signature=123456"
    """
    timestamp = int(time.time())
    params = {
        "app_id": app_id,
        "timestamp": timestamp,
    }
    signature = make_signature(params, secret)
    return f"{ASR_API_ENDPOINT}?app_id={app_id}&timestamp={timestamp}&signature={signature}"


async def run_asr():
    # 参数配置
    args.chunk_size = [int(x) for x in args.chunk_size.split(",")]
    print(args.chunk_size)

    ASR_API_ENDPOINT = "wss://test-asr-api.xmov.ai/ws/asr/"
    wav = "gaoxingdong-new.wav"
    app_id = 13
    secret = "123456"

    websocket_url = make_url(app_id, secret, ASR_API_ENDPOINT)
    async with websockets.connect(websocket_url) as ws:
        print("connected!!!")
        task1 = asyncio.create_task(run_send_task(ws, wav))
        task2 = asyncio.create_task(run_recv_task(ws))
        await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(run_asr())
