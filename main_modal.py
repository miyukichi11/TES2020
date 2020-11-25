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
#from queue import Queue
#import leg
import detect_opencv

from tflite_runtime.interpreter import Interpreter
import tflite_runtime.interpreter as tflite

#########################
    #MUGYUの感情レベル
#########################
#global MUGYU_level

#########################
    #flag
#########################
#global conf_flag
#conf_flag = 0


HOST = '127.0.0.1'   # IPアドレス
PORT = 10500         # Juliusとの通信用ポート番号
DATESIZE = 1024     # 受信データバイト数



#########################
    #wavファイル録音
#########################
def RecogAudio(wav, RATE):
    
#########################
    #flag
#########################
#    global conf_flag
#    conf_flag = 0

    print ("RecogAudio")
    
#---マイクのインデックス確認後⇒コメントアウト----------------------
    #オーディオデバイスの情報を取得、マイクのインデックス番号を入手する
#    PiAudio = pyaudio.PyAudio()
#    for x in range(0, PiAudio.get_device_count()):
#        print ("オーディオデバイスの情報を取得、マイクのインデックス番号を入手する")
#        print(PiAudio.get_device_info_by_index(x))
#-------------------------
        
    #マイクのインデックス番号を定義する
    iDeviceIndex = 1

    threshold = 0.6

    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = wav
 
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #RATE = 16000
    CHUNK = 1024
#    audio = pyaudio.PyAudio()
 
#    stream = audio.open(format=FORMAT, channels=CHANNELS,
#        rate=RATE, input=True,
#        input_device_index = iDeviceIndex,
#        frames_per_buffer=CHUNK)
    
    while True:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex,
            frames_per_buffer=CHUNK)
        
        while True:
    #        if conf_flag == 1:
    #            print ("audio sleep")
    #            time.sleep(10)
            data = stream.read(CHUNK)
            x = np.frombuffer(data, dtype="int16") / 32768.0
            print ("話しかけていいよ")
    
            if (x.max() > threshold):
                
    #            conf_flag = 1
                print ("recording...")
                print ("録音開始...")
                frames = []
                frames.append(data)
                for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    data = stream.read(CHUNK)
                    frames.append(data)
                    
                waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
                waveFile.setnchannels(CHANNELS)
                waveFile.setsampwidth(audio.get_sample_size(FORMAT))
                waveFile.setframerate(RATE)
                waveFile.writeframes(b''.join(frames))
                waveFile.close()
    
                print("Saved.")
                print ("録音終了...")
    
                break
     
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Saved as %s" % wav)
        
    #-------------------
        #サーバー送受信
    #-------------------
        mp3f = send_recv(wav)
        mp3f_str = mp3f.decode("utf-8")
        print ( mp3f )
    #-------------------       
        em_start = 0
            
    #-------------------
        #em_start level
        c = random.randint(1,3)
    #-------------------
        mp3 = "%s/%d.mp3" % (mp3f_str, c)
        RunAudio(mp3)
        time.sleep(1)
    #    conf_flag = 0


#########################
    #wavファイル再生
#########################
def RunAudio(mp3):
    print (mp3)
    pygame.mixer.init(frequency = 44100)
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play(1)
    time.sleep(2)
    #pygame.mixer.music.stop()


#########################
    #サーバー送受信
#########################
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


#########################
    #画処理
#########################
def cv():
    #detect_opencv.pyの呼び出し
    pytfile = "detect_opencv.py"
    modelPATH = "object_detection/models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
    labelsPATH = "object_detection/models/coco_labels.txt"
    os.system("python %s --model %s --labels %s" % (pytfile, modelPATH, labelsPATH))

    
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
        thread_1.start()
        print ("thread_1 start")
        thread_2 = threading.Thread(target=RecogAudio, args=([em_wav, 11025]))
        print ("thread_2")
        thread_2.start()
        print ("thread_2 start")
        thread_1.join()
        thread_2.join()
            
        time.sleep(1)

if __name__ == '__main__':
    main()