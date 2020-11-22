# -*- coding: utf-8 -*-
import socket
import threading
from datetime import datetime
import time
import argparse
import requests

HOST = '127.0.0.1'   # サーバーのIPアドレス
PORT = 10500         # サーバーの待ち受けポート
DATESIZE = 1024     # 受信データバイト数
CLIENTNUM = 3 # クライアントの接続上限数

# サーバー起動 
def run_server():

    # server_socketインスタンスを生成
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(CLIENTNUM)
        print('[{}] run server'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
        while True:
            # クライアントからの接続要求受け入れ
            client_socket, address = server_socket.accept()
            print('[{0}] connect client -> address : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), address) )
            client_socket.settimeout(60)
            # クライアントごとにThread起動 send/recvのやり取りをする
            t = threading.Thread(target = conn_client, args = (client_socket,address))
            t.setDaemon(True)
            t.start()

# クライアントごとにThread起動する関数
def conn_client(client_socket, address):
        
    with client_socket:
        while True:
            # クライアントからデータ受信
            rcv_data = client_socket.recv(DATESIZE)
            if rcv_data:
                mp3f = transcribe_file(rcv_data)
                a_utf8 = mp3f.encode("utf-8")
                client_socket.send(a_utf8)
                # データ受信したデータをそのままクライアントへ送信
                #client_socket.send(rcv_data)
                #print('[{0}] recv date : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data.decode('utf-8')) )
            else:
                break

    print('[{0}] disconnect client -> address : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), address) )

# [START speech_transcribe_sync]
def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    speechContexts = [{
      "phrases": ["むぎゅ", "攻撃"]
     }]

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=11025,
        language_code="ja-JP",
        speech_contexts = speechContexts,
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
    )
    # [END speech_python_migration_config]

    # [START speech_python_migration_sync_response]
    response = client.recognize(config=config, audio=audio)

    # [END speech_python_migration_sync_request]
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        print("Confidence: {}".format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time

            print(
                f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            )
            
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print("First alternative of result {}".format(i))
        print("Transcript: {}".format(alternative.transcript))
        recog_text = response.results
        mp3f = RecogWord(recog_text, speech_file)
    # [END speech_python_migration_sync_response]

    #return response.results
    return mp3f

def RecogWord(recog_text, speech_file):
    em_start = 0
    for result in recog_text:
        alternative = result.alternatives[0]

        for word_info in alternative.words:
            word = word_info.word
            if "攻撃。" in word:
                print("攻撃。")
                mp3f = "sound/attack"
                #RunAudio(mp3)
                em_start = 0
                break
            elif "攻撃" in word:
                print("攻撃")
                mp3f = "sound/attack"
                #RunAudio(mp3)
                em_start = 0
                break
            elif "攻撃|コーゲキ" in word:
                print("攻撃|コーゲキ")
                mp3f = "sound/attack"
                #RunAudio(mp3)
                em_start = 0
                break
            else:
                print(word)
                em_start = 1
        else:
            continue
        break
    if em_start==1:                    
        scor = Empath(speech_file)
        print(scor["calm"])
        max_v = max(scor.values())
        print(max_v)
        max_k = max(scor, key=scor.get)
        print(max_k)
        
        mp3f = "sound/%s" % (max_k)
        
    return mp3f

def Empath(speech_file):
    url ='https://api.webempath.net/v2/analyzeWav'
    apikey = 'ry8XIuja_lBgvdxM9Ruh0m_aCqsXiDet5DDd0R7rUkg'
    payload = {'apikey': apikey}
    
    data = open(speech_file, 'rb')
    file = {'wav': data}
    
    res = requests.post(url, params=payload, files=file)
        
    scor = res.json()
    print(scor)

    return scor    
    

# [END speech_transcribe_sync]

if __name__ == "__main__":
    
    run_server()