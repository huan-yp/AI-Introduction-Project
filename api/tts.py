import simpleaudio as sa
import io
import time

from playsound import playsound
from pydub import AudioSegment
from fish_audio_sdk import Session, TTSRequest
from utils.config import config

def tts(text):
    """
    该函数用于将文本转换为语音。

    参数:
        text (str): 需要转换为语音的文本。

    返回:
        bytes: 合并后的音频数据块 (mp3 format)。
    """
    session = Session(config.FISH_AUDIO_KEY)
    # receive chunks
    chunks = []
    for chunk in session.tts(TTSRequest(
        reference_id=config.FISH_AUDIO_MODEL_ID,
        text=text
    )):
        chunks.append(chunk) 

    return b''.join(chunks)

def play_audio(audio_bytes):
    """
    播放音频数据。

    参数:
        audio_bytes (bytes): 音频数据。

    返回:
        None
    """
    tmp_filename = ".temp/voice.wav"
    with open(tmp_filename, mode="wb+") as tmp_file:
        # 将音频数据转换为WAV格式并写入临时文件
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
        wav_bytes = bytes(audio.export(io.BytesIO(), format="wav").getvalue())
        tmp_file.write(wav_bytes)
    
    playsound(tmp_filename)

def speak(text):
    """
    该函数用于将文本转换为语音并播放。
    """
    start = time.time()
    audio_bytes = tts(text)
    print(time.time() - start)
    start = time.time()
    play_audio(audio_bytes)
    print(time.time() - start)

if __name__ == "__main__":
    audio_bytes = tts("你好世界")
    play_audio(audio_bytes)
