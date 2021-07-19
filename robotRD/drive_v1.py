from machine import Pin
import time
import move
from move import Bot

# drive_v1 provides basic control functionality of
# [INSERT NAME] bot. Allows user to drive forward/backward
# and turn with simple inputs.

pins = [14, 32, 15, 33,
        21, 17, 16, 19]

b = Bot(pins, 0.040, .12)
b.rpm = 25

while True:
    print('Enter command: ')
    com = input()
    args = com.split(' ')
    if args[0] == 'd':
        if float(args[1]) > 0:
            b.move_frd(float(args[1]))
        elif float(args[1]) < 0:
            b.move_bkd(abs(float(args[1])))
        else:
            pass
    elif args[0] == 't':
        b.turn(float(args[1]))
    else:
        print('Invalid command.')
    time.sleep(1)


# pinsR = [14, 32, 15, 33]
# pinsL = [21, 17, 16, 19]

# mR = Motor(pinsR,1,'r',0.040)
# mR.rpm = 10
# mL = Motor(pinsL,1,'l',0.040)
# mL.rpm = 10

# # print('{}, {}, {}'.format(mR.deg_per_step, mR.steps_per_rev, mR._T))

# mR.move_frd(0.1)
# mL.move_frd(0.1)


# b.move_frd(.10)
# time.sleep(1)
# b.move_bkd(.10)
# time.sleep(1)
# b.turn(90)
# time.sleep(1)
# b.turn(-90)
