# -*- coding: utf-8 -*-
#!/usr/bin/python

from __future__ import division
import time
import signal
import sys
import random
import multiprocessing
from multiprocessing import Process, Manager
import Adafruit_PCA9685               #Import the PCA9685 module
from Adafruit_ADS1x15 import ADS1x15  #Import the ADS1x15 module
from current_sensor import currentsensor
from thermister import thermister
from servo import servo
import gpio

#======================================
# initialize
#======================================
# サーボ範囲定義
servo_min = 150  # Min pulse length out of 4096
servo_centor = 400
servo_max = 600  # Max pulse length out of 4096
#　maxが外側 

kata_init  = 100
kata_max = 180

#  足サーボインスタンス生成
leg=[0,0,0,0]
leg[0]=servo(0)
leg[1]=servo(1)
leg[2]=servo(2)
leg[3]=servo(3)

for i in range(4):
    leg[i].move(kata_init)


#  くびサーボインスタンス生成
neck=[0]
neck[0]=servo(4)

#  あたまサーボインスタンス生成
head=[0]
head[0]=servo(5)



#　電流センサインスタンス生成
current=[0,0,0,0]
current[0]=currentsensor(0)
current[1]=currentsensor(1)
current[2]=currentsensor(2)
current[3]=currentsensor(3)


print('initialize')

#======================================
# 関数
#======================================

def data(d,l):
    d['status']='sleep'
    d['touch_back_fl']=0


# 肩幅設定用にすこし広げる関数
def initialize_katahaba(sw):
    for i in range(4):
            leg[i].position=servo_centor
            leg[i].move(kata_init)

#  肩チェック関数
def check_katahaba(sw):
    while True:
        for i in range(4):
            current[i].voltage()
            if current[i].volt > current[i].initvolt - 0.1:
                leg[i].move(-1)
            
            else:
                leg[i].move(0)
                leg[i].katahaba = leg[i].position
                
            if leg[i].position > servo_max:
                leg[i].position = servo_max
            elif leg[i].position < servo_min:
                leg[i].position = servo_min

        if leg[0].katahaba and leg[1].katahaba and leg[2].katahaba and leg[3].katahaba :
            print ('check done')
            break
            sw==0


# ずっとくっつく関数
def zutto_katahaba(sw):
    while sw==1:
        for i in range(4):
            current[i].voltage()
            if current[i].volt > current[i].initvolt - 0.2:
                leg[i].move(-1)
            
            if current[i].volt < current[i].initvolt - 0.5:
                leg[i].move(1)

            if leg[i].position > servo_max: 
                leg[i].position = servo_max
            elif leg[i].position < servo_min:
                leg[i].position = servo_min

# ぎゅっとする関数
def gyutto_katahaba(sw):
    while sw==1:
        for i in range(4):
            current[i].voltage()
            if current[i].volt > current[i].initvolt - 0.5:
                leg[i].move(-1)
            
            if current[i].volt < current[i].initvolt - 0.8:
                leg[i].move(1)

            if leg[i].position > servo_max: 
                leg[i].position = servo_max
            elif leg[i].position < servo_min:
                leg[i].position = servo_min

# むぎゅむぎゅする関数
def mugyumugyu(sw):
    while sw>0:
        count=0
        while count<20:
            zutto_katahaba(1)
            count+=1
        count=0
        while count<20:
            gyutto_katahaba(1)
            count+=1
        count=0
        sw-=1

        

#======================================
#  メインループ
#======================================
def main_control():
    print('control start')
    time.sleep(1)
    for i in range(4):
        current[i].voltage()
        current[i].initvolt=current[i].volt
        print(current[i].initvolt)
    initialize_katahaba(1)
    print('initialize done')
    time.sleep(5)
    print('katahaba check start')
    check_katahaba(1)
    print('katahaba check done')


    while True:
        val = input('enter command: ')
        if val == '0':
            print('status 0')
            print('イニシャル肩幅')
            initialize_katahaba(1)

        if val == '1':
            print('肩幅チェック')
            check_katahaba(1)

        if val == '2':
            print('ずっと肩幅')
            zutto_katahaba(1)
        
        if val == '3':
            print(' ぎゅっと肩幅')
            gyutto_katahaba(1)

        if val == '4':
            print('ムギュムギュ')
            mugyumugyu(5)
        
        if val == '5':
            print('hidari')
            atama_hidari(1)
        if val == '6':
            print('iyaiya')
            iyaiya(1)
        
        else:
            print('1-4')


if __name__== "__main__":
    main_control()
