# -*- coding: utf-8 -*-
import socket
import threading
from datetime import datetime
import time

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
                # データ受信したデータをそのままクライアントへ送信
                client_socket.send(rcv_data)
                print('[{0}] recv date : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data.decode('utf-8')) )
            else:
                break

    print('[{0}] disconnect client -> address : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), address) )

if __name__ == "__main__":
    
    run_server()