# -*- coding: utf-8 -*-
#!/usr/bin/python

from __future__ import division
import time
import signal
import sys
import random
from servo import servo

#======================================
# initialize
#======================================
# サーボ範囲定義
servo_min = 150  # Min pulse length out of 4096
servo_centor = 400
servo_max = 600  # Max pulse length out of 4096
#　maxが外側 

katahaba=0
kata_init  = 100
kata_max = 180

#  くびサーボインスタンス生成
neck=[0]
neck[0]=servo(4)

#  あたまサーボインスタンス生成
head=[0]
head[0]=servo(5)


#======================================
# 関数
#======================================

def motion(sw):
    neck[0].nowp=neck[0].position
    head[0].nowp=head[0].position

    if sw==0:
        neck[0].goto(servo_centor,1)
        print(neck[0].position)
        head[0].goto(servo_centor,1)
        print(head[0].position)
        time.sleep(0.1)
        sw=0

    #左を向く    
    if sw==1:
        neck[0].goto(600,1)
        print(neck[0].position)
        head[0].goto(servo_min,1)
        print(head[0].position)
        time.sleep(0.1)
        sw=0

    #右を向く
    if sw==2:
        neck[0].goto(200,1)
        print(neck[0].position)
        head[0].goto(servo_min,1)
        print(head[0].position)
        time.sleep(0.1)
        sw=0

    #うなづき
    if sw==3:
        head[0].goto(400,1)
        head[0].goto(250,1)
        head[0].goto(400,1)
        head[0].goto(250,1)
        time.sleep(0.1)
        sw=0

    #いやいや
    if sw==4:
        for j in range(5):
            r=int(random.uniform(80,100))
            for i in range(r):
                neck[0].move(-1)
                i+=1
            time.sleep(random.uniform(0.05,0.1))
            for i in range(r):
                neck[0].move(1)
                i+=1
            time.sleep(random.uniform(0.05,0.1))
            j+=1

def main():
    motion(3)
    motion(2)
    motion(1)
    motion(0)

if __name__ == '__main__':
    main()
