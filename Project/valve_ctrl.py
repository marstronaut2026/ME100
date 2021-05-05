import math as m
import sys
import time

import network
from machine import PWM, Pin, ADC
from mqttclient import MQTTClient

from servo_pwm import ctrl_remote

#initialize global pressure variable
pres = 0

#mqtt pressure call back
def setPres(pressure):
    global pres
    pres = pressure.payload.decode('utf-8')

#set MQTT session
session = 'SEB/RegulatorDemo'
BROKER = 'broker.mqttdashboard.com'

# connect to MQTT broker
mqtt = MQTTClient(BROKER, port='1883')
set_topic = "{}/set".format(session, 0)

def mqtt_callback(topic, msg):
    print("Received set pressure: {} psi".format(msg.decode('utf-8')))

# Set callback function
mqtt.set_callback(mqtt_callback)

# Set a topic you will subscribe too. Publish to this topic via web client and watch microcontroller recieve messages.
mqtt.subscribe(set_topic)

#initialize servo PWM pin
servo = PWM(Pin(14),freq=50,duty=7)
time.sleep(1)

print("Waiting for set pressure...")
mqtt.wait_msg()
    # if pres != 0:
        # break
# mqtt.publish(set_topic, pres)

#initialize PT reading cache
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)
diff = [] #difference between current and previous pressure reading
tim = [] #time
for i in range(5):
    tim.append(time.time())
    pot_value = pot.read()*3.3/4096
    curpres = (pot_value-.5)*1000/4.5
    diff.append(pres-curpres)
    time.sleep(0.1) $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
intdiff = integrate.cumtrapz(diff,tim) $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

print(diff)
print("Ready to Regulate")

try:
    t0 = time.time()
    while True:

        #control loop
        tim.append(time.time())
        tim.pop(0)
        diff.append(pres-curpres)
        diff.pop(0)
        intdiff.append(intdiff[-1]+(tim[-1]-tim[-2])*diff[-1])
        intdiff.pop(0)
        derdiff = ((diff[-1]+diff[-2]+diff[-3]+diff[-4])/4-(diff[-2]\
                  +diff[-3]+diff[-4]+diff[-5])/4)/(tim[-1]-tim[-2])
        setPos = 2*intdiff[-1]+5*diff[-1]+0*derdiff+0
        # #testing position values
        # f = open("test.txt","r")

        # for i in f:
        #     if (i == ''):
        #         continue
        #     setPos = float(i) #testing position values

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
        t1 = time.time()
        # txt = "Time: {0}, Position: {1}"
        # print(txt.format(time.time()-t0,setPos))
    # f.close()
except KeyboardInterrupt:     
    print("\nReturning to sleep position...")
    servo.duty(7)
    time.sleep(1)
    servo.deinit()
    mqtt.disconnect()

    print("\nGoodbye.")
