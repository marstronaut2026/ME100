from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import time

def foo(x,y):
        try:
            return x/y
        except ZeroDivisionError:
            return 0

i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

print("scanning I2C bus ...")
print("I2C:", i2c.scan())

SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()

while True:
    ''' Insert your code here to read and print voltage, current, and power from ina219. '''
    amps = ina.current()
    volts = ina.voltage()
    power = ina.power()
    resist = foo(volts,amps)*1000
    print('{:.2f} mA {:.2f} V {:.2f} mW {:.2f} Ohms'.format(amps,volts,power,resist))
    time.sleep(0.5)

    