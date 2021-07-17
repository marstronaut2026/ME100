  
from machine import Pin
import time

p0 = Pin(12, Pin.OUT)
p1 = Pin(13, Pin.OUT)
p2 = Pin(14, Pin.OUT)
p3 = Pin(15, Pin.OUT)

driveSeq = [
      [1,1,0,0],
      [0,1,1,0],
      [0,0,1,1],
      [1,0,0,1]
]

try:
    while True:
        for step in driveSeq:
            p0.value(step[0])
            p1.value(step[1])
            p2.value(step[2])
            p3.value(step[3])
            # print("{}".format(time))
            time.sleep_ms(10)
except KeyboardInterrupt:
    print('Goodbye.')
