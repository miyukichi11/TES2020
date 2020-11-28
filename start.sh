#!/bin/bash

cd ~/home/pi/TES2020

##GPIO23を入力に設定
#if [ ! -e /sys/class/gpio/gpio13 ]; then
#  echo 13 > /sys/class/gpio/export
  echo in > /sys/class/gpio/gpio23/direction
#fi
#SWICTH=1
##ボタンが押されたらWebブラウザーを起動
#while [ $SWICTH = "1" ]
#do
#  SWICTH=$(cat /sys/class/gpio/gpio13/value)
#done

PORT1=12


export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/TESkatanori-40bef20265fa.json"

sleep 2

x-terminal-emulator -e python3 socket_server.py
sleep 2  
x-terminal-emulator -e python3 main_modal.py
sleep 5 
x-terminal-emulator -e python3 main_control.py

  sleep 0.2

