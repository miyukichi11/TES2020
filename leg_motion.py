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

#  足サーボインスタンス生成
leg=[0,0,0,0]
leg[0]=servo(0)
leg[1]=servo(1)
leg[2]=servo(2)
leg[3]=servo(3)

for i in range(4):
    leg[i].move(kata_init)


#======================================
# 関数
#======================================

def motion(sw):
    for i in range(4):
        leg[i].nowp=leg[i].position

    if sw==0:
        for i in range(4):
            leg[i].goto(servo_centor,1)
        time.sleep(0.1)
        sw=0

    if sw==1:
        leg[0].goto(300,1)
        time.sleep(1)
        leg[1].goto(300,1)
        time.sleep(1)



def main():
    time.sleep(1)
    motion(0)
    print(0)
    time.sleep(1)
    motion(1)

if __name__ == '__main__':
    main()
