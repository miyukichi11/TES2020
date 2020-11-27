import time
import board
import busio
import adafruit_mpu6050
import numpy as np
from average_filter import AverageFilter

    
i2c = busio.I2C(board.SCL, board.SDA)
mpu = adafruit_mpu6050.MPU6050(i2c)

mpu.init_a=mpu.acceleration
mpu.init_g=mpu.gyro

num=10
axer_data=[0,0,0]
gyro_data=[0,0,0]
axer_data[0]=AverageFilter(num)
axer_data[1]=AverageFilter(num)
axer_data[2]=AverageFilter(num)
gyro_data[0]=AverageFilter(num)
gyro_data[1]=AverageFilter(num)
gyro_data[2]=AverageFilter(num)
#data_a=np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0],[0,0,0]])
#data_g=np.array([[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]])
#ave=np.convolve(data_a,np.ones(num)/float(num),'valid')

i=0
while i<=num:
    axer_data[0].update(mpu.acceleration[0])
    axer_data[1].update(mpu.acceleration[1])
    axer_data[2].update(mpu.acceleration[2])
    gyro_data[0].update(mpu.acceleration[0])
    gyro_data[1].update(mpu.acceleration[1])
    gyro_data[2].update(mpu.acceleration[2])
    i+=1

print("Acceleration init: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.init_a))
print("Gyro init: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.init_g))

while True:
    axer_data[0].update(mpu.acceleration[0])
    axer_data[1].update(mpu.acceleration[1])
    axer_data[2].update(mpu.acceleration[2])
    gyro_data[0].update(mpu.gyro[0])
    gyro_data[1].update(mpu.gyro[1])
    gyro_data[2].update(mpu.gyro[2])

    mpu.avg_a=(axer_data[0]._filtered_value, axer_data[1]._filtered_value, axer_data[2]._filtered_value)
    mpu.avg_g=(gyro_data[0]._filtered_value, gyro_data[1]._filtered_value, gyro_data[2]._filtered_value)
    print('axer avg:x=%.2f, y=%.2f, z=%.2f m/s^2'%(mpu.avg_a))
    print("gyro avg:x=%.2f, y=%.2f, z=%.2f degrees/s"%(mpu.avg_g))
    time.sleep(0.1)
