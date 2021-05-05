from machine import Pin, PWM
from servo_pwm import ctrl_remote
import time
import math as m
from mqttclient import MQTTClient
import sys

pres = 0

#mqtt pressure call back
def setPres(pressure):
    global pres
    pres = pressure.payload.decode('ascii')

#set MQTT session
session = 'SEB/RegulatorDemo'
BROKER = 'broker.mqttdashboard.com'

# connect to MQTT broker
# print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port='1883')
# print("Connected!")
set_topic = "{}/set".format(session, 0)
mqtt.set_callback(setPres)
mqtt.subscribe(set_topic)

#initialize servo PWM pin
servo = PWM(Pin(14),freq=50,duty=7)
time.sleep(1)

print("Waiting for set pressure...")
mqtt.wait_msg()
    # if pres != 0:
        # break
mqtt.publish(set_topic, pres)

try:
    t0 = time.time()
    while True:
        #import required position data from PID controller
        #
        #
        #
        #
        #
        # setPos = #value from 0-90 degrees

        #testing position values
        f = open("test.txt","r")

        for i in f:
            if (i == ''):
                continue
            setPos = float(i) #testing position values

            if (setPos < 0):
                # print("Invalid position: {}".format(setPos))
                setPos = 0            
            elif (setPos > 90):
                # print("Invalid position: {}".format(setPos))
                setPos = 90
            else:
                pass

            ctrl_remote(setPos, servo)
            topic = "{}/data".format(session)
            data = "{},{}".format(time.time()-t0, setPos)
            mqtt.publish(topic, data)
            # txt = "Time: {0}, Position: {1}"
            # print(txt.format(time.time()-t0,setPos))
        f.close()
except KeyboardInterrupt:     
    print("\nReturning to sleep position...")
    servo.duty(7)
    time.sleep(1)
    servo.deinit()

    print("Telling host to plot data ...") #figure out how to plot real time
    mqtt.publish("{}/plot".format(session), "do plot")
    mqtt.disconnect()

    print("\nGoodbye.")