import math as m
import sys
import time

from ina219 import INA219
from board import SDA, SCL

import network
from machine import PWM, Pin, ADC, I2C
from mqttclient import MQTTClient

from servo_pwm import ctrl_remote

#initialize global pressure variable
pres = 0
sabotage = 0

#set MQTT session
session = 'SEB/RegulatorDemo'
BROKER = 'broker.mqttdashboard.com'

# connect to MQTT broker
mqtt = MQTTClient(BROKER, port='1883')
set_topic = "{}/set".format(session, 0)
# flood_topic = "{}/flood".format(session, 0)

def mqtt_callback(topic, msg):
    global pres
    global sabotage
    if msg.decode('utf-8') == "close":
        print("\nInterrupt detected...\n")
        sabotage = 1
    else:
        pres = float(msg.decode('utf-8'))
        print("Received set pressure: {} psi".format(pres))
    

# Set callback function
mqtt.set_callback(mqtt_callback)
mqtt.subscribe(set_topic)

#initialize servo PWM pin
servo = PWM(Pin(14),freq=50,duty=7)
time.sleep(1)

print("Waiting for set pressure...")
mqtt.wait_msg()
    # if pres != 0:
        # break
# mqtt.publish(set_topic, pres)

# #ina219 voltage readings
# i2c = I2C(id=0, scl=Pin(SCL),sda=Pin(SDA),freq=100000)
# SHUNT_RESISTOR_OHMS = 0.1
# ina = INA219(SHUNT_RESISTOR_OHMS,i2c)
# ina.configure()

#initialize PT reading cache

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)
diff = [] #difference between current and previous pressure reading
tim = [] #time
intdiff = [0.0]
derdiff = 0.0
ki = 0.50
kp = 2.0
kd = 0.0
kf = 30.0
storeData = []
for i in range(5):
    tim.append(time.time())
    pot_value = pot.read()*3.3/4095.0
    # pot_value = ina.voltage()
    curpres = (pot_value-.5)*1000.0/4.0
    diff.append(pres-curpres)
    # time.sleep(0.1)
    if i != 0:
        intdiff.append(intdiff[-1]+(tim[-1]-tim[-2])*diff[-1])
    else:
        pass

print("Regulating...\n")

t0 = time.time()
while True:
    mqtt.check_msg()
    if sabotage == 1:
        break
    #control loop
    pot_value = pot.read()*3.3/4095.0
    # pot_value = ina.voltage()
    curpres = (pot_value-.5)*1000.0/4.0
    tim.append(time.time())
    tim.pop(0)
    diff.append(pres-curpres)
    diff.pop(0)
    if ki*intdiff[-1]+kp*diff[-1]+kd*derdiff+kf < 90 and ki*intdiff[-1]+kp*diff[-1]+kd*derdiff+kf > 30:
        intdiff.append(intdiff[-1]+(tim[-1]-tim[-2])*diff[-1])
        intdiff.pop(0)
    elif ki*intdiff[-1]+kp*diff[-1]+kd*derdiff+kf > 90 and diff[-1] < 0:
        intdiff.append(intdiff[-1]+(tim[-1]-tim[-2])*diff[-1])
        intdiff.pop(0)
    elif ki*intdiff[-1]+kp*diff[-1]+kd*derdiff+kf < 30 and diff[-1] > 0:
        intdiff.append(intdiff[-1]+(tim[-1]-tim[-2])*diff[-1])
        intdiff.pop(0)
    else:
        pass
    derdiff = ((diff[-1]+diff[-2]+diff[-3]+diff[-4])/4-(diff[-2]\
                +diff[-3]+diff[-4]+diff[-5])/4)/(tim[-1]-tim[-2])
    setPos = ki*intdiff[-1]+kp*diff[-1]+kd*derdiff+kf
    
    # #testing position values
    # f = open("test.txt","r")
    # for i in f:
    #     if (i == ''):
    #         continue
    #     setPos = float(i) #testing position values

    if (setPos < 30):
        # print("Invalid position: {}".format(setPos))
        setPos = 0            
    elif (setPos > 90):
        # print("Invalid position: {}".format(setPos))
        setPos = 90
    else:
        pass

    ctrl_remote(setPos, servo)
    data = "{}, {}, {}\n".format(time.time()-t0, setPos, curpres)
    # #Requires board with more storage than esp32
    # storeData.append("{}, {}, {}\n".format(time.time()-t0,\
    #                              setPos, curpres))
    topic = "{}/data".format(session)
    mqtt.publish(topic, data)
    # txt = "{}, {}, {}, {}\n".format(time.time()-t0, setPos, curpres, pot_value)
    # print(txt)
    # f.close()
   
print("\nReturning to closed position...")
servo.duty(7)
time.sleep(1)

# #Requires board with more storage than esp32
# for dat in storeData:
#     mqtt.publish(flood_topic, dat)
#     time.sleep(0.1)

servo.deinit()
mqtt.disconnect()
# i2c.deinit

print("\nGoodbye.")
