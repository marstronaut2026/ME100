from machine import Pin, PWM, I2C
from ina219 import INA219
from board import SDA, SCL
import time
import math as m
from mqttclient import MQTTClient
import network
import sys


def ctrl_remote(setPos, servo):
          
    du = float(4/90*setPos+7)
    servo.duty(du)
 

##################################################################################################
def ctrl_filter():
    #initialize I2C
    i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

    SHUNT_RESISTOR_OHMS = 0.1
    ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
    ina.configure()

    # #set MQTT session
    # session = 'AustinJT/ESP32/servo_position'
    # BROKER = 'broker.mqttdashboard.com'

    # # connect to MQTT broker
    # print("Connecting to MQTT broker", BROKER, "...", end="")
    # mqtt = MQTTClient(BROKER, port='1883')
    # print("Connected!")


    servo = PWM(Pin(14),freq=50,duty=7)
    time.sleep(1) #give time to get to center position

    try:
        t0 = time.time()
        while True:
            amps = []
            for j in range(15):
                amps.append(ina.current()) #current through potentiometer
                time.sleep_ms(1)
            
            pos = (abs(sum(amps)/len(amps))-1.09756097560976)*30
            # du = float(m.sin(pos/30*m.pi)*4+7)
            du = float(-8/60*pos+11)
            servo.duty(du)
            valvePos = 90/8*du-33.75 #Valve position in degrees
            txt = "{0} , {1}, {2}, {3}"
            print(txt.format(time.time()-t0,du,pos,amps))
            # topic = "{}/data".format(session)
            # data = "{},{}".format(time.time()-t0, valvePos)
            # mqtt.publish(topic, data)
    
    except KeyboardInterrupt:
        print("\nReturning to sleep position...")
        servo.duty(3)
        time.sleep(1)
        servo.deinit()

        i2c.deinit()
        # print("Telling host to plot data ...")
        # mqtt.publish("{}/plot".format(session), "create the plot")
        # mqtt.disconnect()

        # f.close() 

        print("\nGoodbye.")

#############################################################################################
def ctrl():
    #initialize I2C
    i2c = I2C(id=0, scl=Pin(SCL), sda=Pin(SDA), freq=100000)

    SHUNT_RESISTOR_OHMS = 0.1
    ina = INA219(SHUNT_RESISTOR_OHMS, i2c)
    ina.configure()

    # #set MQTT session
    # session = 'AustinJT/ESP32/servo_position'
    # BROKER = 'broker.mqttdashboard.com'

    # # connect to MQTT broker
    # print("Connecting to MQTT broker", BROKER, "...", end="")
    # mqtt = MQTTClient(BROKER, port='1883')
    # print("Connected!")


    servo = PWM(Pin(14),freq=50,duty=7)
    time.sleep(1) #give time to get to center position

    try:
        t0 = time.time()
        while True:
            amps = ina.current() #current through potentiometer
            pos = (abs(amps)-1.09756097560976)*30
            # du = float(m.sin(pos/30*m.pi)*4+7)
            du = float(-8/60*pos+11)
            servo.duty(du)
            valvePos = 90/8*du-33.75 #Valve position in degrees
            txt = "{0} , {1}, {2}, {3}"
            print(txt.format(time.time()-t0,du,pos,amps))
            # topic = "{}/data".format(session)
            # data = "{},{}".format(time.time()-t0, valvePos)
            # mqtt.publish(topic, data)
    
    except KeyboardInterrupt:
        print("\nReturning to sleep position...")
        servo.duty(3)
        time.sleep(1)
        servo.deinit()

        i2c.deinit()
        # print("Telling host to plot data ...")
        # mqtt.publish("{}/plot".format(session), "create the plot")
        # mqtt.disconnect()

        # f.close() 

        print("\nGoodbye.")

###############################################################################################
def manual():
    servo = PWM(Pin(14),freq=50,duty=7)
    # duty_cycle = arr.array('i',[3,7,11]) #enable for 3 pos movement
    time.sleep(1) #give time to get to center position

    try:
        t0 = time.time()
        # f=open("pos.txt","w+")
        while True:
            #Allows for input position for servo
            val = float(input("Enter servo position (0 to 90 deg): "))
            setPos = float(4/90*val+7)
            servo.duty(setPos)
            # time.sleep(5)
            # for i in range(3):
            #     servo.duty(duty_cycle[i])
            #     time.sleep(2)
            
            # #Sine wave continuous motion
            # for i in range(60):
            #     du = float(m.sin(i/30*m.pi)*4+7)
            #     servo.duty(du)
            #     txt = "{0} , {1}"
            #     print(txt.format(time.time()-t0,du)) 
            #     # f.write(txt.format(time.time()-t0,du)) #output position data as text file

            #     # topic = "{}/data".format(session)
            #     # data = "{},{}".format(time.time()-t0, du)
            #     # mqtt.publish(topic, data)

            #     time.sleep_ms(25) #control speed of rotation
            

    except KeyboardInterrupt:
        print("\nReturning to sleep position...")
        servo.duty(7)
        time.sleep(1)
        servo.deinit()

        # print("Telling host to plot data ...")
        # mqtt.publish("{}/plot".format(session), "create the plot")
        # mqtt.disconnect()

        # f.close() 

        print("\nGoodbye.")