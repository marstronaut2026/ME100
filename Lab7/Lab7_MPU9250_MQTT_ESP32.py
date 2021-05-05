import machine
import time
from mpu9250_new import MPU9250
from machine import I2C, Pin
from board import SDA, SCL
from board import LED
from mqttclient import MQTTClient
import network
import sys

session = "CHANGE ME"
topic = "{}/data".format(session)
BROKER = "mqtt.eclipse.org"

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
mqtt = MQTTClient(BROKER)
print("Connected!")

MPU9250._chip_id = 115
# 115, 113, 104
i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=400000)
imu = MPU9250(i2c)

def pvalues(Timer):
    topic = "{}/data".format(session)
    data = "{},{},{},{},{},{},{}".format(time.ticks_ms(),imu.accel.x, imu.accel.y, imu.accel.z, imu.gyro.x, imu.gyro.y, imu.gyro.z)
    mqtt.publish(topic, data)

tm = machine.Timer(1)
tm.init(period=1, mode=tm.PERIODIC, callback=pvalues)
