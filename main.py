# -*- coding: utf-8 -*-
import os
import sys
import codecs
import numpy as np
#from poster.encode import multipart_encode, MultipartParam
#from poster.streaminghttp import register_openers
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
#from voice import Julius
#import socket
import transcribe

host = '127.0.0.1'   # IPアドレス
port = 10500         # Juliusとの通信用ポート番号

def LoadstrMatrix( filename , type = str , encoding="sjis" ):
    list = []
    for line in codecs.open( filename , "r" , encoding ):
        if line.find("//")==0:
            continue
        items = []
        for i in line.split():
            if type==str:
                items.append( i )
            else:
                items.append( type( i ) )
        list.append( items )
    return list

def LoadMatrix( filename , type = float , encoding="sjis" ):
    list = []
    for line in codecs.open( filename , "r" , encoding ):
        if line.find("//")==0:
            continue
        items = []
        for i in line.split():
            if type==str:
                items.append( i )
            else:
                items.append( type( i ) )
        list.append( items )
    return list

def LoadArray( filename , type = float , encoding="sjis" ):
    list = []
    for line in codecs.open( filename , "r" , encoding ):
        if line.find("//")==0:
            continue
        line = line.replace( "\r\n" , "" )
        line = line.replace( "\n" , "" )
        if type==str:
            list.append( line )
        else:
            list.append( type(line) )
    return list

def SaveMatrix( mat , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for line in mat:
        for i in line:
            f.write( i )
            f.write( "\t" )
        f.write( "\n" )
    f.close()

def SaveintMatrix( mat , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for line in mat:
        for i in line:
            f.write( int(i) )
            f.write( "\t" )
        f.write( "\n" )
    f.close()

def SaveArray( arr , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for i in arr:
        f.write( i )
        f.write( "\n" )
    f.close()

def SaveintArray( arr , filename , encoding="sjis" ):
    f = codecs.open( filename , "w" , encoding )
    for i in arr:
        f.write( int(i) )
        f.write( "\n" )
    f.close()

def MakeDir( dir ):
    try:
        os.mkdir( dir )
    except:
        return False

    return True

def GetFromlistArr( data , i ):
    newData = data[6000:6001]
    for j in range(1,i):
        newData = newData + data[(j*10)+6000:(j*10)+6001]
    return newData

def GetOneFromMat( data , i ):
    newData = data[i:i+1]
    return newData

def RecogAudio(wav, RATE):
    print ("RecogAudio")
    #iAudio = pyaudio.PyAudio()
    #for x in range(0, iAudio.get_device_count()): 
    #    print(iAudio.get_device_info_by_index(x))

    threshold = 0.4

    RECORD_SECONDS = 3
    WAVE_OUTPUT_FILENAME = wav
    iDeviceIndex = 0
 
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

        if (x.max() > threshold):
            #recstatus = 1
            #filename = datetime.today().strftime("word/%Y%m%d%H%M%S") + ".wav"
            #print(cnt, filename)
            
            print ("recording...")
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
  
def recogKana( wavfile , nbest , space ):
    if space == True:
        t = "\t"

    sentences = []

    #p = os.popen( "~/julius/julius-4.6/julius/julius -C ~/julius/julius-kit/dictation-kit-4.5/main.jconf -C ~/julius/julius-kit/dictation-kit-4.5/am-gmm.jconf -filelist %s -n %d") % (wavfile, nbest)
    p = os.popen( "~/julius/julius-4.6/julius/julius -C ~/julius/julius-kit/dictation-kit-4.5/main.jconf -C ~/julius/julius-kit/dictation-kit-4.5/am-gmm.jconf -nostrip -input word/sample.wav")

    line = p.readline()
    while line:
        searchRes = re.search( "sentence[0-9]+:(.+)" , line )
        print (searchRes)
        if searchRes:
            sentence = searchRes.group(1).strip().replace("silB" , "" ).replace("silE" , "" ).replace(" " , "%s" % t )
            print (sentence)
            sentences.append( sentence )
        line = p.readline()
    p.close()
    sentences = [ s.decode("sjis") for s in sentences ]
    return sentences

def Recogjulius(wav):
    space_sentences = []
    space_recogres = recogKana( wav , 1 , space=True )
    if len(space_recogres)>0:
        for s in space_recogres:
            space_sentences.append( s.replace(u"ー","") )
        print (space_sentences)
    else:
        print ("Can not recog!")

def Recogjulius_mic():
    print ("Recogjulius_mic")
    # Juliusにソケット通信で接続
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    data = ""
    try:
        while True:
            if '</RECOGOUT>\n.' in data:
                # 出力結果から認識した単語を取り出す
                recog_text = ""
                for line in data.split('\n'):
                    index = line.find('WORD="')
                    if index != -1:
                        line = line[index+6:line.find('"', index+6)]
                        recog_text = recog_text + line
                if '晴れ' in recog_text:
                    print("今の天気は晴れ")
                elif '雨' in recog_text:
                    print("今の天気は雨")
                elif '曇' in recog_text:
                    print("今の天気は曇り")
                elif '攻撃' in recog_text:
                    print("攻撃")
                    mp3 = "sound/attack/se_zudaaan.mp3"
                    RunAudio(mp3)
                    time.sleep(2)
                elif 'こうげき' in recog_text:
                    print("こうげき")
                    mp3 = "sound/attack/se_zudaaan.mp3"
                    RunAudio(mp3)
                    time.sleep(2)
                elif 'コウゲキ' in recog_text:
                    print("コウゲキ")
                    mp3 = "sound/attack/se_zudaaan.mp3"
                    RunAudio(mp3)
                    time.sleep(2)
                else:                    
                    print("認識結果: " + recog_text)
                data =""
            else:
                data += str(client.recv(1024).decode('utf-8'))
                print('NotFound')
                
    except KeyboardInterrupt:
        print('finished')
        client.send("DIE".encode('utf-8'))
        client.close()

    
def Empath(wav):
    url ='https://api.webempath.net/v2/analyzeWav'
    apikey = 'ry8XIuja_lBgvdxM9Ruh0m_aCqsXiDet5DDd0R7rUkg'
    payload = {'apikey': apikey}
    
    data = open(wav, 'rb')
    file = {'wav': data}
    
    res = requests.post(url, params=payload, files=file)
        
    scor = res.json()
    print(scor)

    return scor

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
        #thread_1 = threading.Thread(target=Recogjulius_mic)
        #print ("thread_1")
        #thread_1.start()
        #print ("thread_1 start")
        thread_2 = threading.Thread(target=RecogAudio, args=([em_wav, 11025]))
        print ("thread_2")
        thread_2.start()
        print ("thread_2 start")
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
        
        recog_text = transcribe.transcribe_file(em_wav)
        
        em_start = 0
        
        for result in recog_text:
            alternative = result.alternatives[0]

            for word_info in alternative.words:
                word = word_info.word
                if "攻撃。" in word:
                    print("攻撃。")
                    mp3 = "sound/attack/se_zudaaan.mp3"
                    RunAudio(mp3)
                    em_start = 0
                    break
                elif "攻撃" in word:
                    print("攻撃")
                    mp3 = "sound/attack/se_zudaaan.mp3"
                    RunAudio(mp3)
                    em_start = 0
                    break
                elif "攻撃|コーゲキ" in word:
                    print("攻撃|コーゲキ")
                    mp3 = "sound/attack/se_zudaaan.mp3"
                    RunAudio(mp3)
                    em_start = 0
                    break
                else:
                    print(word)
                    em_start = 1
            else:
                continue
            break
        if em_start==1:                    
            scor = Empath(em_wav)
            print(scor["calm"])
            max_v = max(scor.values())
            print(max_v)
            max_k = max(scor, key=scor.get)
            print(max_k)
        
            c = random.randint(1,4)
            mp3 = "sound/%s/%d.mp3" % (max_k, c)
        RunAudio(mp3)
            
        time.sleep(2)
        #print ("Finish")
        #break
    
        # baseDir = "init/"
        # MakeDir( baseDir )
        # configFile = os.path.join( "MakeVariConfig.txt" )
    
        # vision = LoadstrMatrix( configFile )
    
        # print(vision)
        # mat = np.matrix(vision)
        # print(mat)
        # print(mat[0,1])
        # list = GetOneFromMat( vision , 0 )
        # print(list)
        # list = GetFromlistArr( list , 0 )
        #print("test")

if __name__ == '__main__':
    main()