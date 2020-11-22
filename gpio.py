#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO # RPi.GPIOモジュールを使用
import time

# GPIO番号
touch_back = 5
touch_neck = 6
touch_head = 13

power_back = 16
power_neck = 20
power_head = 21

gnd_back = 19
gnd_neck =26
#gnd_head =  もともとGNDのピン

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

# スイッチの状態を取得
sw_back = GPIO.input(touch_back)
sw_neck = GPIO.input(touch_neck)
sw_head = GPIO.input(touch_head)

#　power3.3V出力
GPIO.output(power_back,GPIO.HIGH)
GPIO.output(power_neck,GPIO.HIGH)
GPIO.output(power_head,GPIO.HIGH)
GPIO.output(gnd_back,GPIO.LOW)
GPIO.output(gnd_neck,GPIO.LOW)


# スイッチが押されていた場合(ON)
if sw_back==0:
    backflag=1

# スイッチが離されていた場合(OFF)
else:
    backflag=0

# 後処理 GPIOを解放
"""
GPIO.cleanup(touch_back)
GPIO.cleanup(touch_neck)
GPIO.cleanup(touch_head)

GPIO.cleanup(power_back)
GPIO.cleanup(power_neck)
GPIO.cleanup(power_head)

GPIO.cleanup(gnd_back)
GPIO.cleanup(gnd_neck)
"""
