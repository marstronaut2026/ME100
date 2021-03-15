from mqttclient import MQTTClient
import network
from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import machine
import sys
import time

"""
Send measurement results from microphyton board to host computer.
Use in combination with mqtt_plot_host.py.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

def foo(x,y): #stoopid proofing
        try:
            return x/y
        except ZeroDivisionError:
            return 0

# where to send nudes
session = 'AustinJT/ESP32/helloworld'
BROKER = 'broker.mqttdashboard.com'

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no internet, gib WiFi")
    sys.exit()
else:
    print("WiFi aquired at numbers: ", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port='1883')
print("Connected!")


i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

print("scanning I2C bus ...")
print("I2C:", i2c.scan())

SHUNT_RESISTOR_OHMS = 0.1
ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
ina.configure()

while True: #get the solar cell data
    amps = ina.current()
    volts = ina.voltage()
    power = ina.power()
    resist = foo(volts,amps)*1000
    if resist >= 800:
        break
   
    topic = "{}/data".format(session) #where to write data
    data = "{},{},{},{}".format(amps, volts,power,resist) 
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data) #send data to internet
    time.sleep(0.3) 

# do the plotting (on host)
print("tell host to do the plotting ...") 
mqtt.publish("{}/plot".format(session), "create the plot")
time.sleep(0.5)
# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect() #ends program
# machine.reset() #resets data aquisition