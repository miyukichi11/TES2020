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
from multiprocessing import Value, Array, Process
import subprocess
import socket_server
import socket
import myio
#from queue import Queue
#import leg
import RPi.GPIO as GPIO
import touch_sensor
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
#   for x in range(0, PiAudio.get_device_count()):
#       print ("オーディオデバイスの情報を取得、マイクのインデックス番号を入手する")
#       print(PiAudio.get_device_info_by_index(x))
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

#########################
#タッチセンサ読み込み
#########################
touch_back = 5
touch_neck = 6
touch_head = 13

power_back = 16
power_neck = 20
power_head = 21

gnd_back = 19
gnd_neck =26
#gnd_head =  もともとGNDのピン


touch_sw_back=0
touch_sw_neck=0
touch_sw_head=0

def switch_callback_back(gpio_pin):
    print('touch! 背中')
    print('output')
    mp3 = "sound/calm/1.mp3" 
    subprocess.call("mpg321 sound/calm/1.mp3", shell=True)
    time.sleep(1)
    

def switch_callback_neck(gpio_pin):
    print('touch! 首')
    touch_sw_neck=1

def switch_callback_head(gpio_pin):
    print('touch! 頭')
    touch_sw_head=1

def touch():
    #GPIO番号指定の準備
    GPIO.setmode(GPIO.BCM)

    # スイッチピンを入力、プルアップに設定
    GPIO.setup(touch_back, GPIO.IN)
    GPIO.setup(touch_neck, GPIO.IN)
    GPIO.setup(touch_head, GPIO.IN)

    # 出力pin設定
    GPIO.setup(power_back, GPIO.OUT)
    GPIO.setup(power_neck, GPIO.OUT)
    GPIO.setup(power_head, GPIO.OUT)
    GPIO.setup(gnd_back, GPIO.OUT)
    GPIO.setup(gnd_neck, GPIO.OUT)

    #　power3.3V出力
    GPIO.output(power_back,GPIO.HIGH)
    GPIO.output(power_neck,GPIO.HIGH)
    GPIO.output(power_head,GPIO.HIGH)

    #　gnd 0V出力
    GPIO.output(gnd_back,GPIO.LOW)
    GPIO.output(gnd_neck,GPIO.LOW)
    #GPIO.output(gnd_head,GPIO.LOW)

# スイッチの状態を取得
    GPIO.add_event_detect(touch_back, GPIO.RISING,bouncetime=100)
    GPIO.add_event_callback(touch_back, switch_callback_back) 

    GPIO.add_event_detect(touch_neck, GPIO.RISING,bouncetime=100)
    GPIO.add_event_callback(touch_neck, switch_callback_neck) 
    
    GPIO.add_event_detect(touch_head, GPIO.RISING,bouncetime=100)
    GPIO.add_event_callback(touch_head, switch_callback_head) 

    try:
        while True:
            time.sleep(1)


    except KeyboardInterrupt:
        print("break")


#########################
# アウトプット
#########################
def output():

    if touch_sw_back == 1:
        print('output')
        mp3 = "calm/1.mp3" 
        RunAudio(mp3)
        time.sleep(1)
        touch_sw_back=0


#########################
# main
#########################
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
        #thread_1 = Process(target=cv)
        print ("thread_1")
        thread_1.start()
        print ("thread_1 start")
        
        thread_2 = threading.Thread(target=RecogAudio, args=([em_wav, 11025]))
        #thread_2 = Process(target=RecogAudio, args=([em_wav, 11025]))
        print ("thread_2")
        thread_2.start()
        print ("thread_2 start")
        
        thread_3 = threading.Thread(target=touch)
        #thread_3 = Process(target=touch)
        print ("thread_3")
        thread_3.start()
        print ("thread_3 start")
        
        thread_4 = threading.Thread(target=output)
        #thread_4 = Process(target=output)
        print ("thread_4")
        thread_4.start()

        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()

        time.sleep(1)

if __name__ == '__main__':
    main()
