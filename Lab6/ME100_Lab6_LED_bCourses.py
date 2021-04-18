from board import LED
from machine import Pin, PWM, Timer
from time import sleep
import math

#led = Pin(LED, mode=Pin.OUT)
led_ext = Pin(27, mode=Pin.OUT)

brightness = 0
L1 = PWM(led_ext,freq=200,duty=brightness,timer=0)

def tcb(timer):
    global brightness
    if brightness < 100: #tried making light blink "linearly", works ok
        brightness += 1
    # elif brightness >= 20 and brightness < 40:
    #     brightness += 5
    # elif brightness >= 40 and brightness < 100:
    #     brightness += 10
    else:
        brightness = 0

    print(brightness)
    L1.duty(brightness)

t1 = Timer(1)
t1.init(period=5, mode=t1.PERIODIC, callback=tcb)



#led_ext = Pin(LED, mode=Pin.OUT)
