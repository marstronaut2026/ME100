from mqttclient import MQTTClient
import network
from ina219 import INA219
from machine import I2C, Pin
from board import SDA, SCL
import sys
import time

"""
Send measurement results from microphyton board to host computer.
Use in combination with mqtt_plot_host.py.

'print' statements throughout the code are for testing and can be removed once
verification is complete.
"""

def foo(x,y):
        try:
            return x/y
        except ZeroDivisionError:
            return 0

# Important: change the line below to a unique string,
# e.g. your name & make corresponding change in mqtt_plot_host.py
session = 'AustinJT/ESP32/helloworld'
BROKER = 'mqtt.thingspeak.com'

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port='1883')
print("Connected!")

# send data
# In this sample, we send "fake" data. Replace this code to send useful data,
# e.g. measurement results.

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
    if resist >= 800:
        break
    # add additional values as required by application
    topic = "channels/1328214/publish/ZM28RITPYIAUQWHX"
    data="field1={}&field2={}".format(volts,amps)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)
    time.sleep(15)

# do the plotting (on host)
print("tell host to do the plotting ...")
mqtt.publish("{}/plot".format(session), "create the plot")

# free up resources
# alternatively reset the microphyton board before executing this program again
mqtt.disconnect()