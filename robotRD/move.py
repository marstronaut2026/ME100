from machine import Pin
import time
from math import pi

class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Motor:
    def __init__(self,pins,mode,dir,size = 1):
        self.p1 = Pin(pins[0], Pin.OUT)
        self.p2 = Pin(pins[1], Pin.OUT)
        self.p3 = Pin(pins[2], Pin.OUT)
        self.p4 = Pin(pins[3], Pin.OUT)
        self.mode = mode
        self.dir = dir
        if self.dir != 'l' and self.dir != 'r':
            raise InputError("You\'re lost",\
                           "{}: invalid wheel orientation".format(self.dir))
        if self.mode == 1: # Full Step
            self.deg_per_step = 5.625 / 32
        elif self.mode == 2: # Half Step
            self.deg_per_step = 5.625 / 64
        else:
            raise InputError("cat.exe has failed", "{}: invalid mode".format(self.mode))

        self.steps_per_rev = int(360/self.deg_per_step)
        self.step_angle = 0
        self.wheel_diameter = size
    
    def _set_rpm(self, rpm):
        self._rpm = rpm
        self._T = (60.0 / rpm)/self.steps_per_rev

    rpm = property(lambda self: self._rpm, _set_rpm)

    def move_deg(self, angle):
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle
        steps = (steps % self.steps_per_rev)
        if self.dir == 'l':
            steps = -steps
        if steps > self.steps_per_rev / 2:
            steps -= self.steps_per_rev
            # print("moving " + str(steps) + " steps")
            if self.mode == 1:
                self._move_acw_1(-steps / 4)
            else:
                self._move_acw_2(-steps / 8)
        else:
            # print("moving " + str(steps) + " steps")
            if self.mode == 1:
                self._move_cw_1(steps / 4)
            else:
                self._move_cw_2(steps / 8)
        self.step_angle = target_step_angle

    def move_frd(self, distance):
        angle = distance/(pi*self.wheel_diameter)*360
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle
        # print("moving " + str(steps) + " steps")
        if self.mode == 1:
            if self.dir == 'r':
                self._move_cw_1(steps / 4)
            else: 
                self._move_acw_1(steps / 4)
        else:
            self._move_cw_2(steps / 8)
        self.step_angle = target_step_angle

    def __clear(self):
        self.p1.value(0)
        self.p2.value(0)
        self.p3.value(0)
        self.p4.value(0)

    def _move_acw_1(self, big_step):
        self.__clear()
        driveSeq = [
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1],
            [1,0,0,1]
        ]
        for i in range(big_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p2.value(j[1])
                self.p3.value(j[2])
                self.p4.value(j[3])
                time.sleep(self._T*2)
        self.__clear()
        

    def _move_cw_1(self, big_step):
        self.__clear()
        driveSeq = [
            [1,1,0,0],
            [1,0,0,1],
            [0,0,1,1],
            [0,1,1,0]
        ]
        for i in range(big_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p2.value(j[1])
                self.p3.value(j[2])
                self.p4.value(j[3])
                time.sleep(self._T*2)
        self.__clear()
        

    def _move_acw_2(self, big_step):
        pass

    def _move_cw_2(self, big_step):
        pass

class Bot:
    def __init__(self,pins,size = 1):
        self.p1 = Pin(pins[0], Pin.OUT)
        self.p2 = Pin(pins[1], Pin.OUT)
        self.p3 = Pin(pins[2], Pin.OUT)
        self.p4 = Pin(pins[3], Pin.OUT)
        self.p5 = Pin(pins[4], Pin.OUT)
        self.p6 = Pin(pins[5], Pin.OUT)
        self.p7 = Pin(pins[6], Pin.OUT)
        self.p8 = Pin(pins[7], Pin.OUT)

        self.deg_per_step = 5.625 / 32
        self.steps_per_rev = int(360/self.deg_per_step)
        self.step_angle = 0
        self.wheel_diameter = size
    
    def _set_rpm(self, rpm):
        self._rpm = rpm
        self._T = (60.0 / rpm)/self.steps_per_rev

    rpm = property(lambda self: self._rpm, _set_rpm)

    def move_frd(self, distance):
        angle = distance/(pi*self.wheel_diameter)*360
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle
        # print("moving " + str(steps) + " steps")

        self._move_fw(steps / 4)

        self.step_angle = 0
    
    def move_bkd(self, distance):
        angle = distance/(pi*self.wheel_diameter)*360
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle
        # print("moving " + str(steps) + " steps")

        self._move_bk(steps / 4)

        self.step_angle = 0
        

    def __clear(self):
        self.p1.value(0)
        self.p2.value(0)
        self.p3.value(0)
        self.p4.value(0)
        self.p5.value(0)
        self.p6.value(0)
        self.p7.value(0)
        self.p8.value(0)

    def _move_fw(self, big_step):
        self.__clear()
        driveSeq = [
            [1,1,0,0],
            [1,0,0,1],
            [0,0,1,1],
            [0,1,1,0]
        ]
        for i in range(big_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p5.value(j[3])
                self.p2.value(j[1])
                self.p6.value(j[2])
                self.p3.value(j[2])
                self.p7.value(j[1])
                self.p4.value(j[3])
                self.p8.value(j[0])
                time.sleep(self._T*2)
        self.__clear()

    def _move_bk(self, big_step):
        self.__clear()
        driveSeq = [
            [1,1,0,0],
            [0,1,1,0],
            [0,0,1,1],
            [1,0,0,1]
        ]
        for i in range(big_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p5.value(j[3])
                self.p2.value(j[1])
                self.p6.value(j[2])
                self.p3.value(j[2])
                self.p7.value(j[1])
                self.p4.value(j[3])
                self.p8.value(j[0])
                time.sleep(self._T*2)
        self.__clear()