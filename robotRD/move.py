from machine import Pin
import time
from math import pi

author: nuclearwalrus
credit: Stephen C. Philips http://scphillips.com 
This code is my own, however some functions were inspired by the above. 
Feel free to use as you please. Credit would be appreciated. 

Classes for defining motors and bots using 6-pin stepper motors. 



#custom error handling just because
class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Motor:
    def __init__(self, pins, mode, dir, wheel_diameter=1):
        # pins = list of pin numbers from microcontroller used for stepper control
        # mode: 
        #       1: Full step - high torque + high power
        #       2: Half step - low torque + low power (NOT YET FULLY OPERATIONAL)
        #       3: Microstep - very low torque + high accuracy (DO AT SOME POINT)
        # dir: bot attribute, 'r' = right side motor, 'l' = left side motor
        # wheel_diameter: bot attribute, wheel diameter (in m - default=1m because why not)

        self.p1 = Pin(pins[0], Pin.OUT)
        self.p2 = Pin(pins[1], Pin.OUT)
        self.p3 = Pin(pins[2], Pin.OUT)
        self.p4 = Pin(pins[3], Pin.OUT)
        self.mode = mode
        self.dir = dir
        if self.dir != 'l' and self.dir != 'r':
            raise InputError("You\'re lost",
                             "{}: invalid wheel orientation".format(self.dir))
        if self.mode == 1:
            self.deg_per_step = 5.625 / 32
        elif self.mode == 2:
            self.deg_per_step = 5.625 / 64
        else:
            raise InputError("cat.exe has failed",
                             "{}: invalid mode".format(self.mode))

        self.steps_per_rev = int(360/self.deg_per_step)
        self.step_angle = 0
        self.wheel_diameter = wheel_diameter

    def _set_rpm(self, rpm):
        self._rpm = rpm
        self._T = (60.0 / rpm)/self.steps_per_rev

    rpm = property(lambda self: self._rpm, _set_rpm)

    def move_deg(self, angle):
        # move motor to a specific orientation (in deg) 
        # 0 deg is always motor's original position

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

    # def move_frd(self, distance):
    #     angle = distance/(pi*self.wheel_diameter)*360
    #     target_step_angle = 8*(int(angle/self.deg_per_step)/8)
    #     steps = target_step_angle-self.step_angle
    #     # print("moving " + str(steps) + " steps")
    #     if self.mode == 1:
    #         if self.dir == 'r':
    #             self._move_cw_1(steps / 4)
    #         else:
    #             self._move_acw_1(steps / 4)
    #     else:
    #         self._move_cw_2(steps / 8)
    #     self.step_angle = target_step_angle

    def __clear(self):
        self.p1.value(0)
        self.p2.value(0)
        self.p3.value(0)
        self.p4.value(0)

    def _move_acw_1(self, big_step):
        self.__clear()
        driveSeq = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
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
            [1, 1, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 0]
        ]
        for i in range(big_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p2.value(j[1])
                self.p3.value(j[2])
                self.p4.value(j[3])
                time.sleep(self._T*2)
        self.__clear()

    # INTERNAL FUNCTIONS FOR HALF STEPPING AND MICROSTEPPING TBD
    def _move_acw_2(self, big_step):
        pass

    def _move_cw_2(self, big_step):
        pass


class Bot:
    def __init__(self, pins, wheel_diameter=1, width=1):
        # currently set up for 2 wheeled bots driven by 6-pin stepper motors
        # motors currently only run in full stepping mode (i liek tawwk)
        # pins must be formatted as:
        # [right, side, motor, pins, left, side, motor, pins]
        # order 
        # wheel_diameter = wheel diameter
        # width = distance between bot wheels

        # right side motor pins
        self.p1 = Pin(pins[0], Pin.OUT)
        self.p2 = Pin(pins[1], Pin.OUT)
        self.p3 = Pin(pins[2], Pin.OUT)
        self.p4 = Pin(pins[3], Pin.OUT)

        # left side motor pins
        self.p5 = Pin(pins[4], Pin.OUT)
        self.p6 = Pin(pins[5], Pin.OUT)
        self.p7 = Pin(pins[6], Pin.OUT)
        self.p8 = Pin(pins[7], Pin.OUT)

        # Possibility of adding individual motor control at some point
        # rPins = pins[0:3]
        # lPins = pins[4:7]

        # mR = Motor(rPins,1,'r',wheel_diameter)
        # mL = Motor(lPins,1,'l',wheel_diameter)

        self.deg_per_step = 5.625 / 32  # full stepping
        self.steps_per_rev = int(360/self.deg_per_step)
        self.step_angle = 0  # current angle based off initial position of motors
        self.last_step_angle = 0  # motor positions after last action - use for
        # position control at some point
        self.wheel_diameter = wheel_diameter
        self._botRad = width / 2

    def _set_rpm(self, rpm):
        self._rpm = rpm
        self._T = (60.0 / rpm)/self.steps_per_rev

    # allows for changing rpm speed
    rpm = property(lambda self: self._rpm, _set_rpm)

    def move_frd(self, distance):
        # robot drives forward a certain distance (in m) specified by user.
        # ie: distance = 1 means robot will drive forward 1 meter.
        angle = distance/(pi*self.wheel_diameter)*360
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle
        # print("moving " + str(steps) + " steps")

        self._move_fw(steps / 4)  # divide by 4 because full stepping motors

        self.step_angle = 0

    def move_bkd(self, distance):
        # robot drives backward a certain distance (in m) specified by user.
        # ie: distance = 1 means robot will drive forward 1 meter.
        angle = distance/(pi*self.wheel_diameter)*360
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle
        # print("moving " + str(steps) + " steps")

        self._move_bk(steps / 4)  # divide by 4 because full stepping motors

        self.step_angle = 0

    def turn(self, theta):
        # turns robot an angle (in deg) specified by user

        distance = self._botRad*abs(theta*pi/180)
        angle = distance/(pi*self.wheel_diameter)*360
        target_step_angle = 8*(int(angle/self.deg_per_step)/8)
        steps = target_step_angle-self.step_angle

        if theta > 0:
            self._turn_r(steps / 4)  # divide by 4 because full stepping motors
        elif theta < 0:
            self._turn_l(steps / 4)  # divide by 4 because full stepping motors
        else:
            pass

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
        driveSeq = [  # pin activation cycle for full stepping motor
            [1, 1, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 0]
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
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
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

    def _turn_r(self, r_step):
        self.__clear()
        driveSeq = [
            [1, 1, 0, 0],
            [1, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 0]
        ]
        for i in range(r_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p5.value(j[0])
                self.p2.value(j[1])
                self.p6.value(j[1])
                self.p3.value(j[2])
                self.p7.value(j[2])
                self.p4.value(j[3])
                self.p8.value(j[3])
                time.sleep(self._T*2)
        self.__clear()

    def _turn_l(self, l_step):
        self.__clear()
        driveSeq = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
        ]
        for i in range(l_step):
            for j in driveSeq:
                self.p1.value(j[0])
                self.p5.value(j[0])
                self.p2.value(j[1])
                self.p6.value(j[1])
                self.p3.value(j[2])
                self.p7.value(j[2])
                self.p4.value(j[3])
                self.p8.value(j[3])
                time.sleep(self._T*2)
        self.__clear()
