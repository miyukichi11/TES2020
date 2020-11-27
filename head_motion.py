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

# 左をむく関数

def motion(sw):
    if sw==1:
        count=0
        while count<50:
            neck[0].move(1)
            count+=1
        count=0
        while count<100:
            head[0].move(-1)
            count+=1
        count=0
        sw=0

    if sw==2:
        for j in range(5):
            r=int(random.uniform(50,100))
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
    motion(1)


if __name__ == '__main__':
    main()
