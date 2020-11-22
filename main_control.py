# -*- coding: utf-8 -*-
#!/usr/bin/python

from __future__ import division
import time
import signal
import sys
import Adafruit_PCA9685               #Import the PCA9685 module
from Adafruit_ADS1x15 import ADS1x15  #Import the ADS1x15 module
from current_sensor import currentsensor
from thermister import thermister
from servo import servo

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

# 肩幅設定用にすこし広げる関数
def initialize_katahaba():
    for i in range(4):
            leg[i].position=servo_centor
            leg[i].move(kata_init)

#  肩チェック関数
def check_katahaba():
    while True:
        for i in range(4):
            current[i].voltage()
            if current[i].volt > 2.1 :
                leg[i].move(-1)
            
            else:
                leg[i].move(0)
                leg[i].katahaba = leg[i].position
        if leg[i].position > servo_max or leg[i].position < servo_min:
            break

        if leg[0].katahaba and leg[1].katahaba and leg[2].katahaba and leg[3].katahaba :
            print ('check done')
            break


# ずっとくっつく関数
def zutto_katahaba():
    while True:
        for i in range(4):
            current[i].voltage()
            if current[i].volt > 2.1 :
                leg[i].move(-1)
            
            else:
                leg[i].move(0)
                leg[i].katahaba = leg[i].position

        if leg[i].position > servo_max or leg[i].position < servo_min:
            break    

# ぎゅっとする関数
def gyutto_katahaba():
    while True:
        for i in range(4):
            current[i].voltage()
            if current[i].volt > 1.9 :
                leg[i].move(-1)
            
            elif current[i].volt < 1.7 :
                leg[i].move(1)
        if leg[i].position > servo_max or leg[i].position < servo_min:
            break

# むぎゅむぎゅする関数
def mugyumugyu():
    while True:
        count=0
        while count<20:
            zutto_katahaba()
            count+=1
        count=0
        while count<20:
            gyutto_katahaba()
            count+=1
        count=0

#======================================
#  メインループ
#======================================
while True:
    val = input('enter command: ')
    if val == '0':
        print('イニシャル肩幅')
        initialize_katahaba()

    if val == '1':
        print('肩幅チェック')
        check_katahaba()

    if val == '2':
        print('ずっと肩幅')
        zutto_katahaba()
    
    if val == '3':
        print(' ぎゅっと肩幅')
        gyutto_katahaba()

    if val == '4':
        print('ムギュムギュ')
        mugyumugyu()
    
    else:
        print('1-4')

