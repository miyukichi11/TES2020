# -*- coding: utf-8 -*-
#!/usr/bin/python

from __future__ import division
import time
import signal
import sys
import random
import board
import busio
import numpy as np
import multiprocessing
from multiprocessing import Process, Value, Array, Manager
import Adafruit_PCA9685               #Import the PCA9685 module
from Adafruit_ADS1x15 import ADS1x15  #Import the ADS1x15 module
import adafruit_mpu6050
from current_sensor import CurrentSensor
from thermister import thermister
from servo import servo
from average_filter import AverageFilter
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
current[0]=CurrentSensor(0)
current[1]=CurrentSensor(1)
current[2]=CurrentSensor(2)
current[3]=CurrentSensor(3)

for i in range(4):
    current[i].voltage()
    current[i].initvolt=current[i].volt
    print(current[i].initvolt)



# ジャイロセンサ
def gyro(c_axer,c_gyro,c_sw):
    i2c = busio.I2C(board.SCL, board.SDA)
    mpu = adafruit_mpu6050.MPU6050(i2c)

    time.sleep(1)
    mpu.init_a=mpu.acceleration
    mpu.init_g=mpu.gyro
    print("Acceleration init: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.init_a))
    print("Gyro init: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.init_g))

    num=10
    axer_data=[0,0,0]
    gyro_data=[0,0,0]
    axer_data[0]=AverageFilter(num)
    axer_data[1]=AverageFilter(num)
    axer_data[2]=AverageFilter(num)
    gyro_data[0]=AverageFilter(num)
    gyro_data[1]=AverageFilter(num)
    gyro_data[2]=AverageFilter(num)

    i=0
    while i<=num:
        axer_data[0].update(mpu.acceleration[0])
        axer_data[1].update(mpu.acceleration[1])
        axer_data[2].update(mpu.acceleration[2])
        gyro_data[0].update(mpu.acceleration[0])
        gyro_data[1].update(mpu.acceleration[1])
        gyro_data[2].update(mpu.acceleration[2])
        i+=1

    while True:
        axer_data[0].update(mpu.acceleration[0])
        axer_data[1].update(mpu.acceleration[1])
        axer_data[2].update(mpu.acceleration[2])
        gyro_data[0].update(mpu.gyro[0])
        gyro_data[1].update(mpu.gyro[1])
        gyro_data[2].update(mpu.gyro[2])

        c_axer=(axer_data[0]._filtered_value, axer_data[1]._filtered_value, axer_data[2]._filtered_value)
        c_gyro=(gyro_data[0]._filtered_value, gyro_data[1]._filtered_value, gyro_data[2]._filtered_value)
        time.sleep(0.01)

        if abs(c_axer[0] - mpu.init_a[0])>1.5 or abs(c_axer[1] - mpu.init_a[1])>1.5 or abs(c_axer[2] - mpu.init_a[2])>1.5:
            print('run!')
            c_sw.value=4
            time.sleep(0.5)
        else:
            c_sw.value=3


#======================================
# 関数
#======================================


def control_output(c_sw):
    for i in range(4):
        leg[i].position=servo_centor
        leg[i].move(kata_init)
    
    print('initialize done')
    c_sw.value=2

    while True:
        # 肩幅設定用にすこし広げる関数
        if c_sw.value==1:
            for i in range(4):
                    leg[i].position=servo_centor
                    leg[i].move(kata_init)

        #  肩チェック関数
        if c_sw.value==2:
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
                    c_sw.value==3
                    break


        # ずっとくっつく関数
        if c_sw.value==3:
            print('zutto!')
            for i in range(4):
                leg[i].position=leg[i].katahaba
                leg[i].move(0)
            while True:
                for i in range(4):
                    current[i].voltage()
                    if current[i].volt > current[i].initvolt - 0.2:
                        leg[i].move(-1)
                    
                    if current[i].volt < current[i].initvolt - 0.3:
                        leg[i].move(1)

                    if leg[i].position > servo_max: 
                        leg[i].position = servo_max
                    elif leg[i].position < servo_min:
                        leg[i].position = servo_min
                if c_sw.value!=3:
                    break

        # ぎゅっとする関数
        if c_sw.value==4:
            print('gyutto!')
            while True:
                for i in range(4):
                    current[i].voltage()
                    if current[i].volt > current[i].initvolt - 0.4:
                        leg[i].move(-1)
                    
                    if current[i].volt < current[i].initvolt - 0.7:
                        leg[i].move(1)

                    if leg[i].position > servo_max: 
                        leg[i].position = servo_max
                    elif leg[i].position < servo_min:
                        leg[i].position = servo_min
                if c_sw.value!=4:
                    break

        
        # むぎゅむぎゅする関数
        if c_sw.value==5:
            while True:
                count=0
                while count<20:
                    zutto_katahaba(1)
                    count+=1
                count=0
                while count<20:
                    gyutto_katahaba(1)
                    count+=1
                count=0

        

#======================================
#  メインループ
#======================================
def main_control():
    print('control start')
    time.sleep(1)

    # 共有メモリ生成
    c_axer = Array('i',range(3))
    c_gyro = Array('i',range(3))
    c_current = Array('i',range(4))
    c_sw = Value('i',0)

    process_1 = Process(target=gyro, args=([c_axer, c_gyro,c_sw]))
    print ("process_1")
    process_1.start()
    print ("process_1 start")

    process_2 = Process(target=control_output, args=([c_sw]))
    print ("process_2")
    process_2.start()
    print ("process_2 start")

    process_1.join()
    process_3.join()

if __name__== "__main__":
    main_control()
