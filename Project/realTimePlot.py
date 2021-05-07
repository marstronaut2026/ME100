import paho.mqtt.client as paho
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

session = "SEB/RegulatorDemo"
BROKER = "broker.mqttdashboard.com"
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

# initialize data vectors
t = []
s = []
p = []
ii = 0

datRecord = open("data2.txt","w")

# mqtt callbacks
def data(c, u, message):
    # extract data from MQTT message
    
    global ii
    ii = ii+1
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    # print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    s.append(f[1])
    p.append(f[2])
    
    if (ii%5 == 0):
        print("{}, {}, {}\n".format(t[-1], s[-1], p[-1]))
        datRecord.write("{}, {}, {}\n".format(t[-1], s[-1], p[-1]))
        plt.cla()
        plt.subplot(2,1,1)
        plt.plot(t,p)
        plt.xlabel('Time (s)')
        plt.ylabel('Pressure (psi)')
        plt.subplot(2,1,2)
        plt.plot(t,s)
        plt.xlabel('Time (s)')
        plt.ylabel('Valve Position (deg)')
        plt.draw()
        plt.pause(0.05)    

# subscribe to topics
data_topic = "{}/data".format(session, qos)
set_topic = "{}/set".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.message_callback_add(data_topic, data)

# Send requested set pressure over mqtt
setPressure = input("Enter desired tank pressure: ")
mqtt.publish(set_topic, setPressure)

# wait for MQTT messages
# this function never returns

try:
    mqtt.loop_forever()

except KeyboardInterrupt:
    kill = "close"
    mqtt.publish(set_topic, kill)
    plt.cla()
    print("\nSaving data...")
    datRecord.close()
    mqtt.disconnect()
    print("\nGoodbye.\n")