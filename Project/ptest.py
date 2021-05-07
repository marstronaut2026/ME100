import math as m
import sys
import time


pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

pot_value = pot.read()*3.3/4096
curpres = (pot_value-.5)*1000/4

