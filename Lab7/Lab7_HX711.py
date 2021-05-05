import machine
from machine import freq
from hx711 import HX711
driver = HX711(d_out=4,pd_sck=5)

driver
#HX711 on channel A, gain=128

def pvalues(Timer):
    global driver
    print(driver.read())

tm = machine.Timer(1)
tm.init(period=100, mode=tm.PERIODIC, callback=pvalues)
