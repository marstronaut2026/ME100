from board import LED
from machine import Pin
import time

#Initialize build in LED Pin
led = Pin(LED, mode=Pin.OUT)

def blink(t):
    t = 0
    while True:
        led(1)
        time.sleep(0.1)
        led(0)
        time.sleep(0.1)
        t+=1
        if t == 10:
            break
