# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

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
from multiprocessing import Value, Array, Process, Manager
from ctypes import c_char_p
import subprocess
import socket_server
import socket
import myio
#----一時コメントアウト----
import head_motion as hm
import RPi.GPIO as GPIO
#----一時コメントアウト----
import detect_opencv

from tflite_runtime.interpreter import Interpreter
import tflite_runtime.interpreter as tflite

import argparse
import io
import cv2

EDGETPU_SHARED_LIB = 'libedgetpu.so.1'

HOST = '127.0.0.1'   # IPアドレス
PORT = 10500         # Juliusとの通信用ポート番号
DATESIZE = 1024     # 受信データバイト数



#########################
    #wavファイル録音
#########################
def RecogAudio(wav, RATE):
    print ("RecogAudio")
    
#---マイクのインデックス確認後⇒コメントアウト----------------------
    #オーディオデバイスの情報を取得、マイクのインデックス番号を入手する
#    PiAudio = pyaudio.PyAudio()
#   for x in range(0, PiAudio.get_device_count()):
#       print ("オーディオデバイスの情報を取得、マイクのインデックス番号を入手する")
#       print(PiAudio.get_device_info_by_index(x))
#-------------------------
        
    #マイクのインデックス番号を定義する
    iDeviceIndex = 0

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
            data = stream.read(CHUNK)
            x = np.frombuffer(data, dtype="int16") / 32768.0
            print ("話しかけていいよ")
    
            if (x.max() > threshold):
                
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
        

#########################
    #wavファイル再生
#########################
def RunAudio(mp3):
    print (mp3)
    subprocess.Popen(['mplayer', mp3])
    #pygame.mixer.init(frequency = 44100)
    #pygame.mixer.music.load(mp3)
    #pygame.mixer.music.play(1)
    #time.sleep(2)
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
def load_labels(path):
  """Loads the labels file. Supports files with or without index numbers."""
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels


def set_input_tensor(interpreter, image):
  """Sets the input tensor."""
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  """Returns the output tensor at the given index."""
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold, c_camera, array):
  """Returns a list of detection results, each a dictionary of object info."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': classes[i],
          'score': scores[i]
      }
      print (classes[i])
      if classes[i]==15:
        c_camera.value = c_camera.value + 1
        print ("bird 1")
        print (c_camera.value)
        print (array)
        array[0] = -1
      elif classes[i]==16:
        c_camera.value = c_camera.value + 1
        print ("cat 1")
        print (c_camera.value)
        array[1] = -1
        print (array)
      elif classes[i]==17:
        c_camera.value = c_camera.value + 1
        print ("dog 1")
        print (c_camera.value)
        array[2] = -1
        print (array)
      elif classes[i]==9:
        c_camera.value = c_camera.value - 1
        print ("sign")
        print (c_camera.value)
        array[0] = -50
        print (array)
      elif classes[i]==58:
        c_camera.value = c_camera.value - 1
        print ("sign")
        print (c_camera.value)
        array[1] = -50
        print (array)
      elif classes[i]==59:
        c_camera.value = c_camera.value - 1
        print ("sign")
        print (c_camera.value)
        array[1] = -50
        print (array)
      elif classes[i]==56:
        c_camera.value = c_camera.value - 1
        print ("sign")
        print (c_camera.value)
        array[1] = -50
        print (array)
      results.append(result)
  return results

def cv():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--model',
      help='File path of .tflite file.', required=False,
      type=str,
      default="object_detection/models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
  parser.add_argument(
      '--labels',
      help='File path of labels file.', required=False,
      type=str,
      default="object_detection/models/coco_labels.txt")
  parser.add_argument(
      '--threshold',
      help='Score threshold for detected objects.',
      required=False,
      type=float,
      default=0.4)
  args = parser.parse_args()

  labels = load_labels(args.labels)
  model_file, *device = args.model.split('@')
  try:
    interpreter = Interpreter(model_file, experimental_delegates=[
                                        tflite.load_delegate(EDGETPU_SHARED_LIB,
                                        {'device': device[0]} if device else {})
                                        ])
  except (ValueError, OSError):
    interpreter = Interpreter(model_file)
  interpreter.allocate_tensors()
  _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']


  cap = cv2.VideoCapture(0)

  while True:        
    ret, frame = cap.read()
    (CAMERA_WIDTH, CAMERA_HEIGHT) = (frame.shape[1], frame.shape[0])
    image = cv2.resize(frame, 
                       dsize=(input_width, input_height), 
                       interpolation=cv2.INTER_NEAREST)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    start_time = time.monotonic()
    results = detect_objects(interpreter, image, args.threshold, c_camera, c_boost)

    elapsed_ms = (time.monotonic() - start_time) * 1000
    for obj in results:
      ymin, xmin, ymax, xmax = obj['bounding_box']
      xmin = int(xmin * CAMERA_WIDTH)
      xmax = int(xmax * CAMERA_WIDTH)
      ymin = int(ymin * CAMERA_HEIGHT)
      ymax = int(ymax * CAMERA_HEIGHT)

      cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
      text = '{} {:.2f}'.format(labels[obj['class_id']], obj['score'])
      (text_width, text_height), baseline = cv2.getTextSize(text,
                                              cv2.FONT_HERSHEY_SIMPLEX,
                                              0.5, 1)
      cv2.rectangle(frame,
                    (xmin, ymin),
                    (xmin + text_width, ymin - text_height - baseline),
                    (255, 0, 0),
                    thickness=cv2.FILLED)
      cv2.putText(frame, 
                  text,
                  (xmin, ymin - baseline), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.putText(frame, 
                '{:.1f}ms'.format(elapsed_ms),
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
 
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  cap.release()
  cv2.destroyAllWindows()
  return

def object_cv(c_camera, c_boost):
    c_camera.value = 0
    print ("cat 0")
    print (c_camera.value)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--model', help='File path of .tflite file.',
        required=False,
        type=str, 
        default="object_detection/models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite")
    parser.add_argument(
        '--labels', help='File path of labels file.',
        required=False,
        type=str, 
        default="object_detection/models/coco_labels.txt")
    parser.add_argument(
        '--threshold',
        help='Score threshold for detected objects.',
        required=False,
        type=float,
        default=0.4)
    args = parser.parse_args()

    labels = load_labels(args.labels)
    model_file, *device = args.model.split('@')
    try:
        interpreter = Interpreter(model_file, experimental_delegates=[
                                            tflite.load_delegate(EDGETPU_SHARED_LIB,
                                            {'device': device[0]} if device else {})
                                            ])
    except (ValueError, OSError):
        interpreter = Interpreter(model_file)
    interpreter.allocate_tensors()
    _, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']


    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        (CAMERA_WIDTH, CAMERA_HEIGHT) = (frame.shape[1], frame.shape[0])
        image = cv2.resize(frame, 
                           dsize=(input_width, input_height), 
                           interpolation=cv2.INTER_NEAREST)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        start_time = time.monotonic()
        results = detect_objects(interpreter, image, args.threshold, c_camera, c_boost)
#---------------------
        elapsed_ms = (time.monotonic() - start_time) * 1000
#---------------------
        for obj in results:
            ymin, xmin, ymax, xmax = obj['bounding_box']
            xmin = int(xmin * CAMERA_WIDTH)
            xmax = int(xmax * CAMERA_WIDTH)
            ymin = int(ymin * CAMERA_HEIGHT)
            ymax = int(ymax * CAMERA_HEIGHT)

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            text = '{} {:.2f}'.format(labels[obj['class_id']], obj['score'])
            (text_width, text_height), baseline = cv2.getTextSize(text,
                                                    cv2.FONT_HERSHEY_SIMPLEX,
                                                    0.5, 1)
            cv2.rectangle(frame,
                    (xmin, ymin),
                    (xmin + text_width, ymin - text_height - baseline),
                    (255, 0, 0),
                    thickness=cv2.FILLED)
            cv2.putText(frame, 
                    text,
                    (xmin, ymin - baseline), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.putText(frame, 
                    '{:.1f}ms'.format(elapsed_ms),
                    (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
 
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return


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
    
def switch_callback_neck(gpio_pin):
    print('touch! 首')

def switch_callback_head(gpio_pin):
    print('touch! 頭')

def touch(c_touch):
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
            if GPIO.input(touch_back):
                c_touch.value=1
            elif GPIO.input(touch_neck):
                c_touch.value=2
            elif GPIO.input(touch_head):
                c_touch.value=3
            else:
                c_touch.value=0


    except KeyboardInterrupt:
        print("break")


#########################
# アウトプット
#########################
def output(c_touch,c_wav,c_camera, array):

    while True:
        if c_touch.value == 1:
            print('output')
            c_wav.value = "sound/calm/1.mp3" 
            #subprocess.call("mpg321 %s" % c_wav.value ,shell=True)
            RunAudio(c_wav.value)
            hm.motion(2)
            c_touch.value=0
            time.sleep(1)
        if c_touch.value == 2:
            print('output')
            c_wav.value = "sound/calm/2.mp3" 
            #subprocess.call("mpg321 %s" % c_wav.value ,shell=True)
            RunAudio(c_wav.value)
            c_touch.value=0
            time.sleep(1)
        if c_touch.value == 3:
            print('output')
            c_wav.value = "sound/calm/3.mp3" 
            #subprocess.call("mpg321 %s" % c_wav.value ,shell=True)
            RunAudio(c_wav.value)
            c_touch.value=0
            time.sleep(1)
        if c_camera.value >= 20:
            count = 0
            print (array[:])
            #allc = array[0]+array[1]+array[2]
            #print ("allc")
            if array[0] == -1 and array[1] == -1 and array[2] == -1:
                c_wav.value = "sound/joy/2.mp3" 
                RunAudio(c_wav.value)
                c_camera.value = 0
            else:
                c_wav.value = "sound/joy/1.mp3" 
                RunAudio(c_wav.value)
                c_camera.value = 0
        if c_camera.value <= -20:
            count = 0
            print (array[:])
            #allc = array[0]+array[1]+array[2]
            #print ("allc")
            if array[0] == -50:
                print ("いやいや危険")
                c_wav.value = "sound/anger/1.mp3" 
                RunAudio(c_wav.value)
                #いやいや
                hm.motion(2)
                c_camera.value = 0
            elif array[1] == -50:
                print ("ノーマル")
                c_wav.value = "sound/sorrow/2.mp3" 
                RunAudio(c_wav.value)
                #ノーマル
                hm.motion(2)
                c_camera.value = 0
            else:
                print ("ノーマルelse")
                c_wav.value = "sound/sorrow/2.mp3" 
                RunAudio(c_wav.value)
                c_camera.value = 0
          


#########################
# main
#########################
def main():    
    ju_wav = "word/ju_sample.wav"
    em_wav = "word/em_sample.wav"
    mp3 = "sound/res.mp3"
    RunAudio(mp3)
    
    # 共有メモリ生成
    mng = Manager()
    c_touch = Value('i',0)
    c_mic = Value('i',0)
    c_wav = mng.Value(c_char_p,"sound/res.mp3")
    c_camera = Value('i',0)
    #c_boost = Value('i',0)
    # Arrayオブジェクトの生成
    array = Array('i', range(3))

    #while True:
        #ju = Julius()
        #print ("thread_0")
        #ju_recog = ju.run()
        #print ("thread_01")
        

    #thread_1 = threading.Thread(target=cv)
    thread_1 = Process(target=object_cv, args=([c_camera, array]))
    print ("thread_1")
    thread_1.start()
    print ("thread_1 start")
        
    #thread_2 = threading.Thread(target=RecogAudio, args=([em_wav, 11025]))
    thread_2 = Process(target=RecogAudio, args=([em_wav, 11025]))
    print ("thread_2")
    thread_2.start()
    print ("thread_2 start")
        
    #thread_3 = threading.Thread(target=touch)
    thread_3 = Process(target=touch, args=([c_touch]))
    print ("thread_3")
    thread_3.start()
    print ("thread_3 start")
        
    #thread_4 = threading.Thread(target=output)
    thread_4 = Process(target=output, args=([c_touch,c_wav,c_camera, array]))
    print ("thread_4")
    thread_4.start()
    print ("thread_4 start")

    thread_1.join()
    print('katahaba check done')

    thread_2.join()
    thread_3.join()
    thread_4.join()

    time.sleep(1)

if __name__ == '__main__':
    main()
