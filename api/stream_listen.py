# -*- coding: utf-8 -*-
# 引用 SDK
import time
import json
import pyaudio
import wave

from queue import Queue
from threading import Lock
from datetime import datetime
from api.common import credential
from api.asr import speech_recognizer
from utils.config import config

APPID = config.TENCENT_ID
SECRET_ID = config.TENCENT_SECRET
SECRET_KEY = config.TENCENT_KEY
ENGINE_MODEL_TYPE = "16k_zh"
SLICE_SIZE = 6400
INTERVAL_LIMIT = 4

action_time_lock = Lock()
last_action_time = time.time()
voice_text_queue = Queue()

class MySpeechRecognitionListener(speech_recognizer.SpeechRecognitionListener):
    def __init__(self, id):
        self.id = id

    def on_recognition_start(self, response):
        print("%s|%s|OnRecognitionStart\n" % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), response['voice_id']))

    def on_sentence_begin(self, response):
        rsp_str = json.dumps(response, ensure_ascii=False)
        print("%s|%s|OnRecognitionSentenceBegin, rsp %s\n" % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), response['voice_id'], rsp_str))

    def on_recognition_result_change(self, response):
        global last_action_time, action_time_lock
        action_time_lock.acquire()
        last_action_time = time.time()
        action_time_lock.release()
        rsp_str = json.dumps(response, ensure_ascii=False)
        print("%s|%s|OnResultChange, rsp %s\n" % (datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), response['voice_id'], rsp_str))

    def on_sentence_end(self, response):
        global voice_text_queue, last_action_time, action_time_lock
        action_time_lock.acquire()
        rsp_str = json.dumps(response, ensure_ascii=False)
        last_action_time = time.time()
        action_time_lock.release()
        voice_text_queue.put(rsp_str)
        print("%s|%s|OnSentenceEnd, rsp %s\n" % (datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), response['voice_id'], rsp_str))

    def on_recognition_complete(self, response):
        print("%s|%s|OnRecognitionComplete\n" % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), response['voice_id']))

    def on_fail(self, response):
        rsp_str = json.dumps(response, ensure_ascii=False)
        print("%s|%s|OnFail,message %s\n" % (datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), response['voice_id'], rsp_str))

def process_mic(id=0):
    """从麦克风动态录音到当前说话结束为止
    Args:
        id (int): id 编号, 随便写个整数
    Returns:
        str: 录音文本
    """
    global last_action_time
    last_action_time = time.time()
    listener = MySpeechRecognitionListener(id)
    credential_var = credential.Credential(SECRET_ID, SECRET_KEY)
    recognizer = speech_recognizer.SpeechRecognizer(
        APPID, credential_var, ENGINE_MODEL_TYPE,  listener)
    recognizer.set_filter_modal(1)
    recognizer.set_filter_punc(1)
    recognizer.set_filter_dirty(1)
    recognizer.set_need_vad(1)
    recognizer.set_vad_silence_time(1600)
    recognizer.set_voice_format(1)
    recognizer.set_word_info(1)
    #recognizer.set_nonce("12345678")
    recognizer.set_convert_num_mode(1)
    try:
        def record_audio(callback):
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            RECORD_SECONDS = 120
        
            p = pyaudio.PyAudio()
        
            stream = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)
        
            print("Recording...")
        
            frames = []
        
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                if time.time() - last_action_time > INTERVAL_LIMIT:
                    break
                data = stream.read(CHUNK)
                frames.append(data)
                callback(data)
        
            print("Recording finished.")
        
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # 记录日志
            wf = wave.open(f"temp/{time.time()}.wav", 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
        
        def process_audio_data(data):
            recognizer.write(data)
        
        recognizer.start()
        record_audio(process_audio_data)
        try:
            while True:
                time.sleep(0.1)
                action_time_lock.acquire()
                if time.time() - last_action_time > INTERVAL_LIMIT:
                    action_time_lock.release()
                    print("Recive End")
                    voices = []
                    while voice_text_queue.qsize() > 0:
                        print("GET TEXT")
                        voices.append(json.loads(voice_text_queue.get())["result"]["voice_text_str"])
                    return "\n".join(voices)
                action_time_lock.release()
                
        except KeyboardInterrupt:
            pass
    except Exception as e:
        print(e)
    finally:
        recognizer.stop()

def process_rec(id):
    # audio = "output.wav"
    audio = "tests/test.wav"
    listener = MySpeechRecognitionListener(id)
    credential_var = credential.Credential(SECRET_ID, SECRET_KEY)
    recognizer = speech_recognizer.SpeechRecognizer(
        APPID, credential_var, ENGINE_MODEL_TYPE,  listener)
    recognizer.set_filter_modal(1)
    recognizer.set_filter_punc(1)
    recognizer.set_filter_dirty(1)
    recognizer.set_need_vad(1)
    #recognizer.set_vad_silence_time(600)
    recognizer.set_voice_format(1)
    recognizer.set_word_info(1)
    #recognizer.set_nonce("12345678")
    recognizer.set_convert_num_mode(1)
    try:
        recognizer.start()
        with open(audio, 'rb') as f:
            content = f.read(SLICE_SIZE)
            while content:
                recognizer.write(content)
                content = f.read(SLICE_SIZE)
                #sleep模拟实际实时语音发送间隔
                time.sleep(0.4)
    except Exception as e:
        print(e)
    finally:
        recognizer.stop()

if __name__ == "__main__":
    result = process_mic(0)
    print(result)
