# -*- coding: utf-8 -*-
#!/usr/bin/python

import time, signal, sys
from Adafruit_ADS1x15 import ADS1x15


def signal_handler(signal, frame):
        print ('You pressed Ctrl+C!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'

#======================================
# 初期設定（ライブラリ通り）
#======================================

ADS1015 = 0x00  # 12-bit ADC
ADS1115 = 0x01	# 16-bit ADC

##### Select the gain #####
gain = 4096  # +/- 4.096V

##### Select the sample rate #####
sps = 250  # 250 samples per second

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115, address=0x49)


#======================================
# サーミスタクラス
#======================================

class thermister:

#======================================
# サーミスタスペック
#======================================

    '''
製品型番：AYN-MF59-104F-3950FB
B値と精度B25/85：3950K±1%
抵抗値と精度R25：100kΩ±1%(at25℃)
定格出力：2.5mW(at25℃)
使用温度：-40～250℃
    '''
    thermister_r = 100000 #100k
    pull_up_r  = 10000 #10k
    voltage = 5



    def voltage(self, pin):
        self.volt = adc.readADCSingleEnded(pin, gain, sps) / 1000

    def temperature(self, pin):
        volt = self.volt(pin)
