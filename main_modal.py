# -*- coding: utf-8 -*-
import os
import sys
import codecs
import numpy as np
import requests
import pyaudio
import wave
import pygame.mixer
import time
from datetime import datetime
import random
import re
from fractions import Fraction
import scipy as sp
import matplotlib.pyplot as plt
import scipy.signal as sg
import soundfile as sf
import threading
import socket_server
import socket
import myio
from queue import Queue
#import leg
import detect_opencv

from tflite_runtime.interpreter import Interpreter
import tflite_runtime.interpreter as tflite

HOST = '127.0.0.1'   # IPアドレス
PORT = 10500         # Juliusとの通信用ポート番号
DATESIZE = 1024     # 受信データバイト数

def RecogAudio(wav, RATE):
    print ("RecogAudio")
#########################
#オーディオデバイスの情報を取得、マイクのインデックス番号を入手する
    PiAudio = pyaudio.PyAudio()
    for x in range(0, PiAudio.get_device_count()):
        print ("オーディオデバイスの情報を取得、マイクのインデックス番号を入手する")
        print(PiAudio.get_device_info_by_index(x))
#マイクのインデックス番号を定義する
    iDeviceIndex = 1
#########################
    threshold = 0.4

    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = wav
 
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #RATE = 16000
    CHUNK = 1024
    audio = pyaudio.PyAudio()
 
    stream = audio.open(format=FORMAT, channels=CHANNELS,
        rate=RATE, input=True,
        input_device_index = iDeviceIndex,
        frames_per_buffer=CHUNK)
    
#    cnt = 0
#    recstatus = 0
#    start_at = time.time()
    
    while True:
        data = stream.read(CHUNK)
        x = np.frombuffer(data, dtype="int16") / 32768.0
        print ("話しかけていいよ")

        if (x.max() > threshold):
            #recstatus = 1
            #filename = datetime.today().strftime("word/%Y%m%d%H%M%S") + ".wav"
            #print(cnt, filename)
            
            print ("recording...")
            print ("録音開始...")
            frames = []
            frames.append(data)
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

#        elif (recstatus == 1) and (x.max() > threshold):
#            start_at = time.time()
#            print("Update rec time")
#            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#                data = stream.read(CHUNK)
#                frames.append(data)
#
#        elif (recstatus == 1) and (x.max() <= threshold):
#            if (time.time() - start_at) >1:
#                recstatus = 0
#                print("finished recording")
#                break

    #waveFile = wave.open(filename, 'wb')
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()

            print("Saved.")
            print ("録音終了...")

#            cnt += 1
#
#        if cnt > 5:
            break
 
#    #--------------Start---------------
# 
#    print ("recording...")
#    frames = []
#    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#        data = stream.read(CHUNK)
#        frames.append(data)
# 
#    print ("finished recording")
# 
#    #--------------Finish---------------
 
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("Saved as %s" % wav)
 
#    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#    waveFile.setnchannels(CHANNELS)
#    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
#    waveFile.setframerate(RATE)
#    waveFile.writeframes(b''.join(frames))
#    waveFile.close()

def RunAudio(mp3):
    print (mp3)
    pygame.mixer.init(frequency = 44100)
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play(1)
    #time.sleep(100)
    #pygame.mixer.music.stop()

def send_recv(input_data):
        
    # sockインスタンスを生成
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # ソケットをオープンにして、サーバーに接続
        sock.connect((HOST, PORT))
        print('[{0}] input data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), input_data) )
        # 入力データをサーバーへ送信
        sock.send(input_data.encode('utf-8'))
        print("Send to server : %s" % input_data)
        print("入力データをサーバーへ送信")
        # サーバーからのデータを受信
        rcv_data = sock.recv(DATESIZE)
        print("Receive from server : %s" % rcv_data.decode("utf-8"))
        print("サーバーからのデータを受信")
        #rcv_data = rcv_data.decode('utf-8')
        #print('[{0}] recv data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data) )
        return rcv_data

def cv():
    os.system("python3 detect_opencv.py --model object_detection/models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite --labels object_detection/models/coco_labels.txt")
    
def main():    
    ju_wav = "word/ju_sample.wav"
    em_wav = "word/em_sample.wav"
    mp3 = "sound/res.mp3"
    RunAudio(mp3)
    
    while True:
        #ju = Julius()
        #print ("thread_0")
        #ju_recog = ju.run()
        #print ("thread_01")
        thread_1 = threading.Thread(target=cv)
        print ("thread_1")
        #thread_1.start()
        print ("thread_1 start")
        thread_2 = threading.Thread(target=RecogAudio, args=([em_wav, 11025]))
        print ("thread_2")
        thread_2.start()
        print ("thread_2 start")
        #thread_1.join()
        thread_2.join()
        
        #thread_1.start()
        #print ("thread_11 start")
        #thread_1.join()
        
        #Thread(target = RecogAudio).start(ju_wav, 16000)
        #Thread(target = RecogAudio).start(em_wav, 11025)
        #RecogAudio(wav)
        #upsampling(wav)
        #Recogjulius(wav)
        #iAudio = pyaudio.PyAudio()
        #for x in range(0, iAudio.get_device_count()): 
        #    print(iAudio.get_device_info_by_index(x))
        #wav = "2.wav"
        
#        recog_text = transcribe.transcribe_file(em_wav)
#############################################
        mp3f = send_recv(em_wav)
        mp3f_str = mp3f.decode("utf-8")
        print ( mp3f )
################################################        
        em_start = 0
        
#-------------------
        #em_start level
        c = random.randint(1,3)
#-------------------
        mp3 = "%s/%d.mp3" % (mp3f_str, c)
        RunAudio(mp3)
            
        time.sleep(2)

if __name__ == '__main__':
    main()