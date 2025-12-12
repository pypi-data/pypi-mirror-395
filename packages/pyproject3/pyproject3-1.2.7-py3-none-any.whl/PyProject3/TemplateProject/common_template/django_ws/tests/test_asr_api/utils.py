import json
import ffmpeg

from schema import Args



def parse_hotword(args: Args):
    fst_dict = {}
    hotword_msg = ""
    if args.hotword.strip() != "":
        f_scp = open(args.hotword, encoding='utf-8')
        hot_lines = f_scp.readlines()
        hotword_list = []
        for line in hot_lines:
            words = line.strip().split(" ")
            if len(words) < 2:
                print("Adding hotword:", line.strip())
                hotword_list.append(line.strip())
                print(
                    "Please checkout format of hotwords, hotword and score, separated by space")
                words.append('20')
            try:
                fst_dict[" ".join(words[:-1])] = int(words[-1])
            except ValueError:
                print("Please checkout format of hotwords")
        hotword_msg = json.dumps(fst_dict)
        print(hotword_msg)
    return hotword_msg


def parser_wav(wav, args: Args):
    """ 解析wav文件，返回音频字节、音频块数、音频名称、音频步长
    Args:
        wav: str
        args: Args
    Returns:
        audio_bytes: bytes
        chunk_num: int
        wav_name: str
        stride: int
    """
    sample_rate = args.audio_fs
    wav_splits = wav.strip().split()
    wav_name = wav_splits[0] if len(wav_splits) > 1 else "demo"
    wav_path = wav_splits[1] if len(wav_splits) > 1 else wav_splits[0]
    if wav_path.endswith(".pcm"):
        with open(wav_path, "rb") as f:
            audio_bytes = f.read()
    else:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        audio_bytes, _ = (
            ffmpeg.input(wav_path, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sample_rate)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )

    stride = int(60 * args.chunk_size[1] / args.chunk_interval / 1000 * sample_rate * 2)
    chunk_num = (len(audio_bytes) - 1) // stride + 1
    wave_length_seconds = len(audio_bytes) / sample_rate / 2
    return audio_bytes, chunk_num, wav_name, stride, wave_length_seconds


def clear_console():
    print("\033c", end="")


def csv_write(file_path: str, header: str, data: str) -> bool:
    try:
        with open(file_path, "w") as f:
            f.write(header + "\n" + data)
        return True
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False


def csv_append(file_path: str, data: str) -> bool:
    try:
        with open(file_path, "a") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Error appending CSV file: {e}")
        return False
