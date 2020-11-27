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

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

#======================================
# PCA9685 settings
#======================================

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

#======================================
# サーボ範囲定義
#======================================
servo_min = 150  # Min pulse length out of 4096
servo_centor = 400
servo_max = 600  # Max pulse length out of 4096
#　maxが外側 

katahana  = 500
kata_max = 180

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
now=[0,0,0,0]

class servo:

    def __init__(self, pin):
        self.position = servo_centor
        self.pin=pin
        self.katahaba=0
        pwm.set_pwm(self.pin,0,servo_centor)


#======================================
# サーボモータを指定変位分動かす（+で外側に開く）
#======================================
    def move(self, change):
        if self.pin==1 or self.pin==2:
            self.position-=change
            pwm.set_pwm(self.pin,0,self.position)
        else:
            self.position+=change
            pwm.set_pwm(self.pin,0,self.position)


#======================================
# サーボモータを指定位置まで動かす
#======================================
    def goto(self, position, time):
        count=0
        self.nowp=self.position
        while count < abs(self.nowp-position):
            if self.nowp < position:
                self.move(1)
                #self.position=+time
                #pwm.set_pwm(self.pin,0,self.position)
            if self.nowp >= position:
                self.move(-1)
                #self.position=+time
                #pwm.set_pwm(self.pin,0,self.position)
            count+=1
