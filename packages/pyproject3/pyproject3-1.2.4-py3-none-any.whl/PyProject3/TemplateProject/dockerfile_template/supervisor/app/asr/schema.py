# coding: utf-8
import os
import json
from dataclasses import dataclass
from dataclasses import field
from typing import List
from xmovsystemmonitor.schema import Statistic


@dataclass
class Args:
    host: str = "192.168.88.101"
    port: int = 31366
    chunk_size: str = "5, 10, 5"
    chunk_interval: int = 10
    hotword: str = ""
    audio_in: str = None
    audio_fs: int = 16000
    send_without_sleep: bool = True
    thread_num: int = 1
    words_max_print: int = 10000
    output_dir: str = None
    ssl: int = 0
    itn: int = 1
    vad_tail_sil: int = 350
    vad_max_len: int = 20000
    svs_lang: str = "auto"
    mode: str = "2pass"


@dataclass
class StreamModePerformance:
    name: str = "default"
    wav_path: str = ""

    connection_init_time: float = 0  # 连接开始时间
    connection_established_time: float = 0  # 连接完成时间

    init_audio_time: float = 0  # 初始化音频时间
    audio_loaded_time: float = 0  # 音频加载时间
    
    first_audio_chunk_sent_time: float = 0  # 第一个音频块发送时间
    first_word_received_time: float = 0  # 第一个词接收时间

    last_audio_chunk_sent_time: float = 0  # 最后一个音频块发送时间
    last_word_received_time: float = 0  # 最后一个词接收时间

    debug_info: dict = field(default_factory=dict)  # 调试信息

    avg_cpu: float = 0  # 平均CPU使用量
    max_cpu: float = 0  # 最大CPU使用量
    avg_memory: float = 0  # 平均内存使用量
    max_memory: float = 0  # 最大内存使用量

    # 音频长度和ASR处理时间
    wave_length_seconds: float = 0  # 音频长度(秒) 
    asr_seconds: float = 1  # ASR处理时间(秒)
    asr_result: str = ""  # ASR结果
    
    @property
    def rtf(self):
        return self.asr_seconds / self.wave_length_seconds

    @property
    def id(self):
        wav_name = self.wav_path.split("/")[-1].split(".")[0]
        return f"{self.name}_{wav_name}"

    @property
    def init_audio_latency(self):
        return self.audio_loaded_time - self.init_audio_time

    @property
    def connection_latency(self):
        return self.connection_established_time - self.connection_init_time

    @property
    def first_word_latency(self):
        return self.first_word_received_time - self.first_audio_chunk_sent_time

    @property
    def last_word_latency(self):
        return self.last_word_received_time - self.last_audio_chunk_sent_time
    
    def to_dict(self):
        data = {}
        data.update(self.__dict__)
        data.update({
            "connection_latency": self.connection_latency,
            "first_word_latency": self.first_word_latency,
            "last_word_latency": self.last_word_latency,
        })
        return data
    
    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    def csv_header(self, sleep_mode: bool = True):
        return "id,connection_latency,first_word_latency,last_word_latency,avg_cpu,max_cpu,avg_memory,max_memory,wave_length_seconds,asr_seconds,asr_result,rtf"

    def csv_data(self, sleep_mode: bool = True):
        return f"{self.id},{self.connection_latency},{self.first_word_latency},{self.last_word_latency},{self.avg_cpu},{self.max_cpu},{self.avg_memory},{self.max_memory},{self.wave_length_seconds},{self.asr_seconds},{self.asr_result},{self.rtf}"
    

@dataclass
class NoneStreamModePerformance:
    wav_path: str = ""
    first_word_latency: float = 0  # 第一个词延迟
    rtf: float = 0  # 最后一个词延迟
    # avg_cpu: float  # 平均CPU使用量
    # max_cpu: float  # 最大CPU使用量
    # avg_memory: float  # 平均内存使用量
    # max_memory: float  # 最大内存使用量


@dataclass
class StreamModePerformanceResult:
    name: str = "default"
    performances: List[StreamModePerformance] = field(default_factory=list)

    def put(self, performance: StreamModePerformance):
        self.performances.append(performance)

    def updaete_cpu_memory_statistic(self, statistic: Statistic):
        """ 更新CPU和内存统计信息, 并更新到每个performance中.
        Args:
            statistic: Statistic
        Returns:
            None
        """
        avg_cpu = statistic.cpu.avg
        max_cpu = statistic.cpu.max
        avg_memory = statistic.memory.avg
        max_memory = statistic.memory.max
        for performance in self.performances:
            performance.avg_cpu = avg_cpu
            performance.max_cpu = max_cpu
            performance.avg_memory = avg_memory
            performance.max_memory = max_memory

    def csv_header(self, sleep_mode: bool = True):
        return self.performances[0].csv_header(sleep_mode)

    def csv_detail_data(self, sleep_mode: bool = True):
        return "\n".join([performance.csv_data(sleep_mode) for performance in self.performances])
    
    def csv_summary_header(self, sleep_mode: bool = True):
        if sleep_mode:
            return "name,connection_latency,first_word_latency,last_word_latency,avg_cpu,max_cpu,avg_memory,max_memory"
        else:
            return "name,connection_latency,first_word_latency,last_word_latency,avg_cpu,max_cpu,avg_memory,max_memory,rtf"

    def csv_summary_data(self, sleep_mode: bool = True):
        connection_latency = sum([performance.connection_latency for performance in self.performances]) / len(self.performances)
        first_word_latency = sum([performance.first_word_latency for performance in self.performances]) / len(self.performances)
        last_word_latency = sum([performance.last_word_latency for performance in self.performances]) / len(self.performances)
        avg_cpu = sum([performance.avg_cpu for performance in self.performances]) / len(self.performances)
        max_cpu = max([performance.max_cpu for performance in self.performances])
        avg_memory = sum([performance.avg_memory for performance in self.performances]) / len(self.performances)
        max_memory = max([performance.max_memory for performance in self.performances])
        rtf = sum([performance.rtf for performance in self.performances]) / len(self.performances)
        if sleep_mode:
            return f"\n{self.name},{connection_latency},{first_word_latency},{last_word_latency},{avg_cpu},{max_cpu},{avg_memory},{max_memory}"
        else:
            return f"\n{self.name},{connection_latency},{first_word_latency},{last_word_latency},{avg_cpu},{max_cpu},{avg_memory},{max_memory},{rtf}"

    def to_detail_csv(self, csv_file_path: str, sleep_mode: bool = True) -> bool:
        """  写入明细数据到csv文件
        Args:
            csv_file_path: csv文件路径
        Returns:
            bool: 是否成功
        """
        from utils import csv_write

        if len(self.performances) == 0:
            return False
        return csv_write(csv_file_path, self.csv_header(sleep_mode), self.csv_detail_data(sleep_mode))
    
    def append_summary_csv(self, csv_file_path: str, sleep_mode: bool = True) -> bool:
        """ 写入或追加summary数据到csv文件
        Args:
            csv_file_path: csv文件路径
        Returns:
            bool: 是否成功
        """
        from utils import csv_append, csv_write

        if os.path.exists(csv_file_path):
            return csv_append(csv_file_path, self.csv_summary_data(sleep_mode=sleep_mode))
        else:
            return csv_write(csv_file_path, self.csv_summary_header(sleep_mode=sleep_mode), self.csv_summary_data(sleep_mode=sleep_mode))

    def print(self, sleep_mode: bool = True):
        # 打印结果
        print("-------------- detail ------------------")
        print(self.csv_header(sleep_mode=sleep_mode))
        print(self.csv_detail_data(sleep_mode=sleep_mode))
        print("-------------- summary ------------------")
        print(self.csv_summary_header(sleep_mode=sleep_mode))
        print(self.csv_summary_data(sleep_mode=sleep_mode))

    def __add__(self, other: 'StreamModePerformanceResult') -> 'StreamModePerformanceResult':
        """ 合并两个StreamModePerformanceResult
        Args:
            other: StreamModePerformanceResult
        Returns:
            StreamModePerformanceResult
        """
        result = StreamModePerformanceResult(name=self.name)
        result.performances.extend(self.performances)
        result.performances.extend(other.performances)
        return result
    
    def __radd__(self, other: 'StreamModePerformanceResult') -> 'StreamModePerformanceResult':
        """ 定义了 __add__ 和 __radd__ 后, 可以使用 sum 函数来合并两个StreamModePerformanceResult，返回的结果是StreamModePerformanceResult。
        """
        if isinstance(other, int):
            return self
        result = StreamModePerformanceResult(name=self.name)
        result.performances.extend(other.performances)
        result.performances.extend(self.performances)
        return result
    