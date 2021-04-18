from board import LED
from machine import Pin, PWM, Timer
from time import sleep
import math

#Notes
C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
F3 = 175
FS3 = 185
G3 = 196
GS3 = 208
A3 = 220
AS3 = 233
B3 = 247
C4 = 262
CS4 = 277
D4 = 294
DS4 = 311
E4 = 330
F4 = 349
FS4 = 370
G4 = 392
GS4 = 415
A4 = 440
AS4 = 466
B4 = 494
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
F5 = 698
FS5 = 740
G5 = 784
GS5 = 831
A5_ = 880
AS5 = 932
B5 = 988
C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
##########


fork = Pin(27, mode=Pin.OUT)
power = 80
#notes for Ode to Joy opening
notes = [B4, B4, C5, D5, D5, C5, B4, A4, G4, G4, A4, B4, B4, A4, A4, B4, B4, C5, D5, D5, C5, B4, A4]
N1 = PWM(fork, freq=notes[0], duty=power, timer=0)
i = 0

def tcb(timer):
    global notes
    global i
    global power
    if i < len(notes)-1:
        i += 1
    else:
        i = 0

    # print("{}, {}".format(i, notes[i]))
    N1.freq(notes[i])
    for j in range(8): #used to make individual notes audibly differentiable 
        N1.duty(power-10*j)
        sleep(.002)
        
    
    

t1 = Timer(1)
t1.init(period=350, mode=t1.PERIODIC, callback=tcb) #play song