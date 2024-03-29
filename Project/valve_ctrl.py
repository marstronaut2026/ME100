import math as m
import sys
import time

from machine import ADC, PWM, Pin
from mqttclient import MQTTClient

from servo_pwm import ctrl_remote

# Initialize global pressure variable
pres = 0
sabotage = 0

# Set MQTT session
session = 'SEB/RegulatorDemo'
BROKER = 'broker.mqttdashboard.com'

# Connect to MQTT broker
mqtt = MQTTClient(BROKER, port='1883')
data_topic = "{}/data".format(session)
set_topic = "{}/set".format(session, 0)

def mqtt_callback(topic, msg):
    global pres
    global sabotage
    if msg.decode('utf-8') == "close":
        print("\nInterrupt detected...\n")
        sabotage = 1 # breaks main loop and closes valve
    else:
        pres = float(msg.decode('utf-8'))
        print("Received set pressure: {} psi".format(pres))
    

# Set callback function
mqtt.set_callback(mqtt_callback)
mqtt.subscribe(set_topic)

# Initialize servo PWM pin
servo = PWM(Pin(14),freq=50,duty=7)
time.sleep(1)

print("Waiting for set pressure...")
mqtt.wait_msg()

# Initialize PT ADC pin
pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)
diff = [] # difference between current and previous pressure reading
tim = [] # time
intdiff = [0.0]
derdiff = 0.0

#PID CONSTANTS
ki = 0.50
kp = 2.0
kd = 0.0
kf = 30.0

# Initialize PT reading cache
for i in range(5):
    tim.append(time.time())
    pot_value = pot.read()*3.3/4095.0
    curpres = (pot_value-.5)*1000.0/4.0
    diff.append(pres-curpres)

    if i != 0:
        intdiff.append(intdiff[-1]+(tim[-1]-tim[-2])*diff[-1])
    else:
        pass

print("Regulating...\n")


t0 = time.time() # initial time for plotting

#CONTROL LOOP
while True:
    mqtt.check_msg()
    if sabotage == 1:
        break # end loop when plotting scipt is killed
    pot_value = pot.read()*3.3/4095.0 # read PT value
    curpres = (pot_value-.5)*1000.0/4.0 # convert to pressure
    tim.append(time.time())
    tim.pop(0)
    diff.append(pres-curpres)
    diff.pop(0)

    # Anti-windup
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
    
    # Valve position in degrees
    setPos = ki*intdiff[-1]+kp*diff[-1]+kd*derdiff+kf

    # Set limits on valve position
    if (setPos < 30):
        setPos = 0            
    elif (setPos > 90):
        setPos = 90
    else:
        pass

    # Command servo to move to position
    ctrl_remote(setPos, servo)

    # Store time, valve pos, and pressure data
    data = "{}, {}, {}\n".format(time.time()-t0, setPos, curpres)
    
    # Send data over mqtt
    mqtt.publish(data_topic, data)

   
print("\nReturning to closed position...")
servo.duty(7) # closes valve
time.sleep(1)

servo.deinit() #kill servo :(
mqtt.disconnect()

print("\nGoodbye.") 
