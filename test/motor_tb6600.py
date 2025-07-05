#coding:utf-8

import RPi.GPIO as GPIO
import time
import keyboard


import inspect
import sys
def debug_print(variable):
    # 呼び出し元のフレームを取得
    frame = inspect.currentframe().f_back
    # 変数名を検索
    for name, val in frame.f_locals.items():
        if val is variable:
            print(f"{name} : {variable}")
            return
    print(f"variable : {variable}")  # 名前が見つからない場合

GPIO.setmode(GPIO.BOARD)
PUL=8
DIR=10
ENA=12

GPIO.setup(PUL, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DIR, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)

#DIR=HIGH:cw, DIR=LOW:ccw
#ENA=HIGH:enable(exciting), ENA=LOW:disable(non-exciting)

dir_flag = 1
ena_flag = 1

#パルスの幅を指定。値を小さくする程高速で回転する。
wid = 0.0005

#回転角度を指定
ang = 180

#倍率
rate=8

#減速比を設定
#1軸CNCルータの場合は4を設定
#モータ単体の場合は1を設定
ratio = 1

#回転角度をパルス数に換算
cnt = int(ratio*(ang / (360/200)) * rate) 
debug_print(cnt)

GPIO.output(ENA, 1)
try:
    while True:

        GPIO.output(DIR,dir_flag)
        for j in range(0,cnt):
            
            GPIO.output(PUL,0)
            time.sleep(wid)
            GPIO.output(PUL,1)
            time.sleep(wid)

        time.sleep(0.5)
        
        dir_flag = (dir_flag+1)%2

except:
    pass

GPIO.output(PUL,0)
GPIO.output(ENA, 0)
GPIO.output(PUL,0)
print("finished.")
GPIO.cleanup()


