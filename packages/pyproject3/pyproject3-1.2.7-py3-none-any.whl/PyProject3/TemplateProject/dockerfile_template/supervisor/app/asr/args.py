# coding: utf-8 

import argparse
from schema import Args

parser = argparse.ArgumentParser()
parser.add_argument("--host",
                    type=str,
                    default="192.168.88.101",
                    required=False,
                    help="host ip, localhost, 0.0.0.0")
parser.add_argument("--port",
                    type=int,
                    default=31366,
                    required=False,
                    help="grpc server port")
parser.add_argument("--chunk_size",
                    type=str,
                    default="5, 10, 5",
                    help="chunk")
parser.add_argument("--chunk_interval",
                    type=int,
                    default=10,
                    help="chunk")
parser.add_argument("--hotword",
                    type=str,
                    default="",
                    help="hotword file path, one hotword perline (e.g.:阿里巴巴 20). "
                    "For good recognition result, the hotword score should better be lower than 50.")
parser.add_argument("--audio_in",
                    type=str,
                    default=None,
                    help="audio_in")
parser.add_argument("--audio_fs",
                    type=int,
                    default=16000,
                    help="audio_fs")
parser.add_argument("--send_without_sleep",
                    action="store_true",
                    default=True,
                    help="if audio_in is set, send_without_sleep")
parser.add_argument("--thread_num",
                    type=int,
                    default=1,
                    help="thread_num")
parser.add_argument("--words_max_print",
                    type=int,
                    default=10000,
                    help="chunk")
parser.add_argument("--output_dir",
                    type=str,
                    default=None,
                    help="output_dir")

parser.add_argument("--ssl",
                    type=int,
                    default=0,
                    help="1 for ssl connect, 0 for no ssl")
parser.add_argument("--itn",
                    type=int,
                    default=1,
                    help="1 for using itn, 0 for not itn")
parser.add_argument("--vad_tail_sil",
                    type=int,
                    default=350,
                    help="tail silence length for VAD, in ms. "
                    "if consecutive silence time exceed this value, VAD will cut.")
parser.add_argument("--vad_max_len",
                    type=int,
                    default=20000,
                    help="max duration of a audio clip cut by VAD, in ms")

# we use itn to control whether to use itn in SenseVoice also.
# parser.add_argument("--svs_itn",
#                     type=int,
#                     default=1,
#                     help="1 for SenseVoice model using itn, 0 for not itn")
parser.add_argument("--svs_lang",
                    type=str,
                    default='auto',
                    help="Set language for SenseVoice model: "
                    "zh/中, en/英, ja/日, ko/韩, yue/粤, default=auto/自动判别语种")

parser.add_argument("--mode",
                    type=str,
                    default="2pass",
                    help="offline, online, 2pass")

def get_args() -> Args:
    _args = parser.parse_args()
    _args.chunk_size = [int(x) for x in _args.chunk_size.split(",")]
    return Args(**vars(_args))
