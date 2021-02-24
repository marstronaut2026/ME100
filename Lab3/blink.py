from board import LED
from machine import Pin
import time

#Initialize build in LED Pin
led = Pin(14, mode=Pin.OUT)

t = 0
while True:
    if t == 3000:
        break
    led(1)
    time.sleep(0.002)
    led(0)
    time.sleep(0.002)
    t+=1

