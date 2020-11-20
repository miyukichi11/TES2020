from __future__ import division
import time
import signal
import sys
import Adafruit_PCA9685               #Import the PCA9685 module
from Adafruit_ADS1x15 import ADS1x15  #Import the ADS1x15 module

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

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_centor = 400
servo_max = 600  # Max pulse length out of 4096

kata  = 50
kata_max = 180

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
now=[0,0,0,0]

#======================================
# ADS1x15 settings
#======================================
ADS1115 = 0x01	# 16-bit ADC

# Select the gain
gain = 4096  # +/- 4.096V

# Select the sample late
sps = 250 # 250 samples per second

# Initialise the ADC using the default mode (use default I2C address)
adc = ADS1x15(ic=ADS1115)


#======================================
# checking ADC read voltage
#======================================

def checking_voltage(num):
    # Read channel 0 in single-ended mode using the settings above
    volts = adc.readADCSingleEnded(num, gain, sps)
    return volts

#======================================
# servo reverse
#======================================
def changer(num, current, change):
    if num==0 or num==3:
        current-=change
    else:
        current+=change
    return current

#======================================
# servo moving
#======================================

print('Moving servo on channel 0-3, press Ctrl-C to quit...')
print('command 1:init, 2:move, 3:move slow, 0:stop')
while True:
    val = input('enter command: ')

    if val == 1:
        print('initialize centor')
        for i in range(4):
            now[i]=servo_centor
            pwm.set_pwm(i,0,now[i])
            print(i, now[i])

    if val == 2:
        print(' kata narrow')
        for i in range(4):
            now[i]=changer(i,now[i],kata)
            pwm.set_pwm(i,0,now[i])
            print(i, now[i])
    
    if val == 3:
        print(' kata wide')
        for i in range(4):
            now[i]=changer(i,now[i],-kata)
            pwm.set_pwm(i,0,now[i])
            print(i, now[i])

    if val == 4:
        print(' moving ')
        count=0
        while (servo_min < now[0])and (now[0] < servo_max):
            if 0 < checking_voltage(0) < 1500:
                now[0]+=3
                pwm.set_pwm(0,0,now[0])
                print(checking_voltage(0),  now[0])

            elif checking_voltage(0) >2000 :
                now[0]-=1
                pwm.set_pwm(0,0,now[0])
                print(checking_voltage(0),  now[0])

            else:
                pwm.set_pwm(0,0,now[0])
                count=count+1
                if count == 10:
                    break

    if val == 5:
 
        for i in range(servo_centor,servo_centor-100,-1):
            pwm.set_pwm(2, 0, i)
            time.sleep(0.005)

        for j in range(servo_centor2,servo_centor2-100,-1):
            pwm.set_pwm(3, 0, j)
            time.sleep(0.001)
    
        current2=servo_centor-100
        current3=servo_centor2-100


    if val == 0:
        pwm.set_pwm(0,0,servo_min)
        pwm.set_pwm(1,0,servo_min)
        #pwm.set_pwm(2,0,servo_centor)
        #pwm.set_pwm(3,0,servo_centor)
        break
