import simpleaudio as sa
import io
import time
import logging

from playsound import playsound
from pydub import AudioSegment
from fish_audio_sdk import Session, TTSRequest
from utils.config import config
from flask import Flask, request

# 调整日志级别
logger = logging.getLogger('httpcore.http11')
logger.setLevel(logging.INFO)
logger = logging.getLogger('httpcore.connection')
logger.setLevel(logging.INFO)
logger = logging.getLogger('httpcore.proxy')
logger.setLevel(logging.INFO)
logger = logging.getLogger('openai._base_client')
logger.setLevel(logging.INFO)

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
    tmp_filename = f"temp/{time.time()}voice.wav"
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

app = Flask(__name__)

@app.route('/speak', methods=['GET'])
def speak_route():
    text = request.args.get('text', '')
    if text:
        speak(text)
        return "Speaking initiated", 200
    else:
        return "No text provided", 400

if __name__ == "__main__":
    app.run(port=3367)