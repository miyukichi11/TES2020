import RPi.GPIO as GPIO
import time

touch_back = 5
touch_neck = 6
touch_head = 13

power_back = 16
power_neck = 20
power_head = 21

gnd_back = 19
gnd_neck =26
#gnd_head =  もともとGNDのピン

touch_sw_back=0
touch_sw_neck=0
touch_sw_head=0

def switch_callback_back(gpio_pin):
    print(gpio_pin)
    touch_sw_back=1

def switch_callback_neck(gpio_pin):
    print(gpio_pin)
    touch_sw_neck=1

def switch_callback_head(gpio_pin):
    print(gpio_pin)
    touch_sw_head=1

def touch_main():
    touch_sw_back=0
    touch_sw_neck=0
    touch_sw_head=0
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

#　power3.3V出力
    GPIO.output(power_back,GPIO.HIGH)
    GPIO.output(power_neck,GPIO.HIGH)
    GPIO.output(power_head,GPIO.HIGH)

#　gnd 0V出力
    GPIO.output(gnd_back,GPIO.LOW)
    GPIO.output(gnd_neck,GPIO.LOW)

# スイッチの状態を取得

    GPIO.add_event_detect(touch_back, GPIO.RISING,bouncetime=100)
    GPIO.add_event_callback(touch_back, switch_callback_back) 
    
    GPIO.add_event_detect(touch_neck, GPIO.RISING,bouncetime=100)
    GPIO.add_event_callback(touch_neck, switch_callback_neck) 
    
    GPIO.add_event_detect(touch_head, GPIO.RISING,bouncetime=100)
    GPIO.add_event_callback(touch_head, switch_callback_head) 


    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("break")
        GPIO.cleanup()

if __name__ == "__main__":
    touch_main()
