from board import LED
from machine import Pin, PWM, Timer
import time, math

L1 = PWM(LED,freq=500,duty=50,timer=0)
