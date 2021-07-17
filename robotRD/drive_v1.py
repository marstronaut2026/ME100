from machine import Pin
import time
import move
from move import Bot

# pinsR = [14, 32, 15, 33]
# pinsL = [21, 17, 16, 19]

# mR = Motor(pinsR,1,'r',0.040)
# mR.rpm = 10
# mL = Motor(pinsL,1,'l',0.040)
# mL.rpm = 10

# # print('{}, {}, {}'.format(mR.deg_per_step, mR.steps_per_rev, mR._T))

# mR.move_frd(0.1)
# mL.move_frd(0.1)

pins = [14,32,15,33,
        21,17,16,19]

b = Bot(pins,0.040)
b.rpm = 10

b.move_frd(0.05)
time.sleep(1)
b.move_bkd(0.05)