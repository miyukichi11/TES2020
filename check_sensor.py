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
# gain = 6144  # +/- 6.144V#
gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

##### Select the sample rate #####
# sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
sps = 250  # 250 samples per second
# sps = 475  # 475 samples per second
# sps = 860  # 860 samples per second

# Initialise the ADC using the default mode (use default I2C address)
# Set this to ADS1015 or ADS1115 depending on the ADC you are using!
adc = ADS1x15(ic=ADS1115)
adc2 = ADS1x15(ic=ADS1115, address=0x49)

while True:
    volts0 = adc.readADCSingleEnded(0, gain, sps) / 1000
    volts1 = adc.readADCSingleEnded(1, gain, sps) / 1000
    volts2 = adc.readADCSingleEnded(2, gain, sps) / 1000
    volts3 = adc.readADCSingleEnded(3, gain, sps) / 1000
 
    temp0 = adc2.readADCSingleEnded(0, gain, sps) / 1000
    temp1 = adc2.readADCSingleEnded(1, gain, sps) / 1000
    temp2 = adc2.readADCSingleEnded(2, gain, sps) / 1000
    temp3 = adc2.readADCSingleEnded(3, gain, sps) / 1000

    #print "%.6f" %(volts0)

    print ('\r%.3f, %.3f, %.3f, %.3f' % (volts0,volts1,volts2,volts3),)
    print ('%.3f, %.3f, %.3f, %.3f' % (temp0,temp1,temp2,temp3),)
