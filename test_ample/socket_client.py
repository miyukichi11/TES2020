# -*- coding: utf-8 -*-
import socket
from datetime import datetime
import time

HOST = '127.0.0.1'   # サーバーのIPアドレス
PORT = 10500         # サーバーの待ち受けポート
DATESIZE = 1024     # 受信データバイト数

def send_recv(input_data):
        
    # sockインスタンスを生成
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # ソケットをオープンにして、サーバーに接続
        sock.connect((HOST, PORT))
        print('[{0}] input data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), input_data) )
        # 入力データをサーバーへ送信
        sock.send(input_data.encode('utf-8'))
        # サーバーからのデータを受信
        rcv_data = sock.recv(DATESIZE)            
        rcv_data = rcv_data.decode('utf-8')
        print('[{0}] recv data : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data) )

if __name__ == "__main__":

    while True:
        input_data = input("send data:") # ターミナルから入力された文字を取得
        send_recv(input_data)