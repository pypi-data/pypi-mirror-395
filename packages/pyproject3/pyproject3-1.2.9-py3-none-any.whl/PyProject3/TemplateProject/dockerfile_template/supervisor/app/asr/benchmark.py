# coding: utf-8
import os
import time
from multiprocessing import Process
from threading import Thread
import asyncio
import json
import websockets
import ssl
from xmovsystemmonitor.client.client import Client

# local import
from args import get_args
from utils import parse_hotword, parser_wav, clear_console
from schema import StreamModePerformance, NoneStreamModePerformance, StreamModePerformanceResult
from typing import List


CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR, "data")

args = get_args()


async def send_audio(wavs, ws, performance: StreamModePerformance):
    """ 发送音频
    Args:
        chunk_begin: int
        chunk_size: int
        ws: websocket
    Returns:
        None
    """
    is_finished = False
    websocket = ws
    performance.wav_path = wavs[0]

    # hotwords
    hotword_msg = parse_hotword(args)

    sample_rate = args.audio_fs
    wav_format = "pcm"

    for wav in wavs:
        performance.init_audio_time = time.perf_counter()  # 初始化音频时间
        audio_bytes, chunk_num, wav_name, stride, wave_length_seconds = parser_wav(wav, args)
        performance.wave_length_seconds = wave_length_seconds
        performance.audio_loaded_time = time.perf_counter()  # 音频加载时间
        # 发送音频第一帧
        message = json.dumps({"mode": args.mode, "chunk_size": args.chunk_size, "chunk_interval": args.chunk_interval, "audio_fs": sample_rate,
                              "wav_name": wav_name, "wav_format": wav_format,  "is_speaking": True, "hotwords": hotword_msg, "itn": (args.itn == 1),
                              "vad_tail_sil": args.vad_tail_sil, "vad_max_len": args.vad_max_len, "svs_lang": args.svs_lang})
        await websocket.send(message)
        performance.first_audio_chunk_sent_time = time.perf_counter()  # 第一个音频块发送时间

        is_speaking = True
        for i in range(chunk_num):
            beg = i * stride
            data = audio_bytes[beg:beg + stride]
            message = data
            await websocket.send(message)
            performance.last_audio_chunk_sent_time = time.perf_counter()  # 最后一个音频块发送时间

            if i == chunk_num - 1:
                is_speaking = False
                message = json.dumps({"is_speaking": is_speaking})
                await websocket.send(message)
                performance.last_audio_chunk_sent_time = time.perf_counter()  # 最后一个音频块发送时间

            sleep_duration = 60 * args.chunk_size[1] / args.chunk_interval / 1000 if args.send_without_sleep else 0
        
            performance.debug_info["chunk_sleep_time"] = sleep_duration  # debug
            performance.debug_info["chunk_num"] = chunk_num  # debug
            performance.debug_info["chunk_size"] = args.chunk_size  # debug
            performance.debug_info["chunk_interval"] = args.chunk_interval  # debug
            performance.debug_info["audio_fs"] = sample_rate  # debug
            performance.debug_info["wav_name"] = wav_name  # debug
            performance.debug_info["wav_format"] = wav_format  # debug
            performance.debug_info["is_speaking"] = is_speaking  # debug
            performance.debug_info["hotwords"] = hotword_msg  # debug
            performance.debug_info["itn"] = args.itn  # debug  
            performance.debug_info["stride"] = stride  # debug
            performance.debug_info["audio_bytes_size"] = len(audio_bytes)  # debug
    
            if args.send_without_sleep:
                expected_duration = sleep_duration * (i + 1)  # 第i+1个音频块预期发送时间(秒)
                real_sleep_duration = expected_duration - (time.perf_counter() - performance.first_audio_chunk_sent_time)
                performance.debug_info["i+1"] = i + 1  # debug
                performance.debug_info["real_sleep_duration"] = real_sleep_duration  # debug
                performance.debug_info["expected_duration"] = expected_duration  # debug
                if real_sleep_duration > 0:
                    await asyncio.sleep(real_sleep_duration)

    # fixme: 这里得修改一下。使用is_final来进行ws连接断开，否则多线程情况下，可能推理没有结束就断开了连接，导致
    # 尾字延时计算不准。 这里简单的先把等待时间延长，最好还是用is_final来判断。
    await asyncio.sleep(10)
    await websocket.close()


async def recv_result(id, ws, performance: StreamModePerformance):
    """ 接收消息
    Args:
        id: str
        ws: websocket
        performance: StreamModePerformance
    Returns:
        None
    """
    websocket = ws
    text_print = ""
    text_print_2pass_online = ""
    text_print_2pass_offline = ""
    time_stamp_print = ""
    try:
        is_first_word = True

        while True:
            msg = await websocket.recv()
            msg = json.loads(msg)
            wav_name = msg.get("wav_name", "demo")
            text = msg["text"]
            performance.last_word_received_time = time.perf_counter()
            performance.asr_seconds = time.perf_counter() - performance.first_audio_chunk_sent_time
            if is_first_word and text != "":
                performance.first_word_received_time = time.perf_counter()
                is_first_word = False
            offline_msg_done = msg.get("is_final", False)
            timestamp = ""
            if "timestamp" in msg:
                timestamp = msg["timestamp"]
                time_stamp_print += timestamp+"\n"
            if 'mode' not in msg:
                continue
            if msg["mode"] == "2pass-online":
                text_print_2pass_online += "{}".format(text)
                text_print = text_print_2pass_offline + text_print_2pass_online
                print("xmov_benchmark: 2pass-online")
            else:   # 2pass-offline
                text_print_2pass_online = ""

                text_print = text_print_2pass_offline + "{}".format(text)
                text_print_2pass_offline += "{}".format(text)
            text_print = text_print[-args.words_max_print:]
            
            performance.asr_result = text_print

            if id == "0":  # 只打印第一个线程的日志
                clear_console()
                print("\rpid" + str(id) + ": " + text_print)
                print(f"xmov_benchmark: 2pass-offline, {offline_msg_done}, {msg}")
                print(performance.to_json())
            if msg["is_final"]:
                offline_msg_done = True
                print(time_stamp_print)

    except Exception as e:
        print("Exception:", e)


async def run_ws_client(thread_num, id, wavs, performance_result: StreamModePerformanceResult):
    global websocket, offline_msg_done
    offline_msg_done = False
    if args.ssl == 1:
        ssl_context = ssl.SSLContext()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        uri = "wss://{}:{}".format(args.host, args.port)
    else:
        uri = "ws://{}:{}".format(args.host, args.port)
        ssl_context = None
    print("connect to", uri)

    performance = StreamModePerformance(name=f"并发{thread_num}线程_{id}号")
    performance.connection_init_time = time.perf_counter()
    async with websockets.connect(uri, subprotocols=["binary"], ping_interval=None, ssl=ssl_context) as websocket:
        performance.connection_established_time = time.perf_counter()
        task1 = asyncio.create_task(send_audio(wavs, websocket, performance))
        task2 = asyncio.create_task(recv_result(str(id), websocket, performance))
        await asyncio.gather(task1, task2)
    print(performance.to_json())
    performance_result.put(performance)


def run_in_thread(thread_num, id, wavs, performance_result: StreamModePerformanceResult):
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(run_ws_client(thread_num, id, wavs, performance_result))


def get_result_dir(ensure_exists: bool = True):
    d = os.path.join(CUR_DIR, "result")
    if ensure_exists and not os.path.exists(d):
        os.makedirs(d)
    return d


def run_performance_test(thread_num: int=11, run_num_index: int=0, wavs: List[str]=None):
    """ 执行性能测试
    Args:
        thread_num: int 
        run_num_index: int
        wavs: List[str]
    Returns:
        None
    """
    RESULT_DIR = get_result_dir(ensure_exists=True)
    # wavs = [f"{DATA_DIR}/gaoxingdong-new.wav"] 
    # 启动监控CPU和内存使用情况
    client.start()
    performance_result = StreamModePerformanceResult(name=f"并发数{thread_num}")

    # 创建线程, 执行性能测试任务
    processes = []
    for i in range(thread_num):
        p = Thread(target=run_in_thread, args=(thread_num,i, wavs, performance_result))
        processes.append(p)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    # 停止监控CPU和内存使用情况
    client.stop()
    # 更新CPU和内存统计信息
    performance_result.updaete_cpu_memory_statistic(statistic=client.statistic)
    # 保存结果
    # performance_result.to_detail_csv(os.path.join(RESULT_DIR, f"ASR性能测试明细-{thread_num}并发.csv"))
    # performance_result.append_summary_csv(os.path.join(RESULT_DIR, "ASR性能测试汇总.csv"))
    # 打印结果
    # performance_result.print()
    return performance_result

def run_performance_test_multi_run(thread_num: int=11, run_num: int=5, wavs_list: List[List[str]]=None) -> StreamModePerformanceResult:
    """ 执行多次性能测试
    Args:
        thread_num: int
        run_num: int
        wavs: List[str]
    Returns:
        None
    """
    performance_results: List[StreamModePerformanceResult] = []
    for wavs in wavs_list:
        for i in range(run_num):
            print(f"{thread_num}并发, 音频文件: {wavs}, 执行第{i+1}次性能测试, 共{run_num}次")
            performance_result = run_performance_test(thread_num=thread_num, run_num_index=i+1, wavs=wavs)
            performance_results.append(performance_result)
    total_performance_result = sum(performance_results)
    return total_performance_result

if __name__ == "__main__":
    is_local = False
    args.send_without_sleep = True
    if is_local:
        SYSTEM_MONITOR_HOST = "127.0.0.1"
        SYSTEM_MONITOR_PORT = 8000
        args.host = "192.168.88.101"
        args.port = 31366
        # 并发数，执行次数
        thread_num_max = 2
        run_num = 1
        # 音频文件列表
        wavs_list = [
                    # [f"{DATA_DIR}/gaoxingdong-new.wav"],
                    # [f"{DATA_DIR}/number.wav"],
                    # [f"{DATA_DIR}/SteveJobs_10s.wav"],
                    # [f"{DATA_DIR}/xmov.wav"],
                    [f"{DATA_DIR}/性能测试用/CN1-短-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN2-短-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN3-中-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN4-中-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN5-长-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN1-短-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN2-短-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN3-中-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN4-中-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN5-长-无数字.wav"],
                    ]
    else:
        SYSTEM_MONITOR_HOST = "asr-2pass"
        SYSTEM_MONITOR_PORT = 8999
        args.host = "asr-2pass"
        args.port = 10096
        # 并发数，执行次数
        thread_num_max = 20
        run_num = 5
        # 音频文件列表
        wavs_list = [
                    #[f"{DATA_DIR}/gaoxingdong-new.wav"],
                    # [f"{DATA_DIR}/number.wav"],
                    # [f"{DATA_DIR}/SteveJobs_10s.wav"],
                    # [f"{DATA_DIR}/xmov.wav"],
                    [f"{DATA_DIR}/性能测试用/CN1-短-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN2-短-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN3-中-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN4-中-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/CN5-长-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN1-短-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN2-短-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN3-中-无数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN4-中-有数字.wav"],
                    [f"{DATA_DIR}/性能测试用/EN5-长-无数字.wav"],
                    ]
    args.vad_tail_sil = 600
    # args.vad_max_len = 20000
    # args.svs_lang = "auto"
    # args.mode = "2pass"
    # args.itn = 1
    # args.chunk_size = "5, 10, 5"
    # args.chunk_interval = 10
    # args.words_max_print = 10000
    # args.ssl = 0

    client = Client(host=SYSTEM_MONITOR_HOST, port=SYSTEM_MONITOR_PORT)
    if not client.is_alive():
        print("系统监控服务未启动，请先在ASR服务机器上启动系统监控服务")
        exit(1)

    RESULT_DIR = get_result_dir(ensure_exists=True)
    st = time.time()
    for thread_num in range(1, thread_num_max):
        sleep_mode = args.send_without_sleep
        print(f"================并发数: {thread_num}=================")
        total_performance_result = run_performance_test_multi_run(thread_num=thread_num, run_num=run_num, wavs_list=wavs_list)
        if sleep_mode: 
            detail_file_name = f"ASR性能测试明细-{thread_num}并发.csv"
            summary_file_name = "ASR性能测试汇总.csv"
        else:
            detail_file_name = f"ASR性能测试明细-RTF-{thread_num}并发.csv"
            summary_file_name = "ASR性能测试汇总-RTF.csv"
        total_performance_result.to_detail_csv(os.path.join(RESULT_DIR, detail_file_name), sleep_mode=sleep_mode)
        total_performance_result.append_summary_csv(os.path.join(RESULT_DIR, summary_file_name), sleep_mode=sleep_mode)
        total_performance_result.print(sleep_mode=sleep_mode)

    end = time.time()
    print(f"总时间: {end - st}秒")