import paho.mqtt.client as paho
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

session = "SEB/RegulatorDemo"
BROKER = "broker.mqttdashboard.com"
qos = 0

# Connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

# Initialize data vectors
t = []
s = []
p = []
ii = 0 #loop counter

# Set file for writing data
datRecord = open("data2.txt","w")

# Handles incoming data over mqtt, 
# live plotting and writing to file for analysis
def data(c, u, message):
    
    global ii
    ii += 1

    # Decode and split data into separate vectors
    msg = message.payload.decode('ascii')
    f = [ float(x) for x in msg.split(',') ]
    
    t.append(f[0]) # time
    s.append(f[1]) # valve position
    p.append(f[2]) # pressure
    
    if (ii%5 == 0):
        # Data to console
        print("{}, {}, {}\n".format(t[-1], s[-1], p[-1]))
        # Data to file
        datRecord.write("{}, {}, {}\n".format(t[-1], s[-1], p[-1]))

        ##LIVE PLOTTING
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

# Subscribe to topics
data_topic = "{}/data".format(session, qos)
set_topic = "{}/set".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.message_callback_add(data_topic, data)

# Send requested set pressure over mqtt
setPressure = input("Enter desired tank pressure: ")
mqtt.publish(set_topic, setPressure)

try:
    mqtt.loop_forever()

# Ends PID loop script and saves data to text file
# CTRL-C for interrupt
except KeyboardInterrupt:
    kill = "close"
    mqtt.publish(set_topic, kill)
    plt.cla()
    print("\nSaving data...")
    datRecord.close()
    mqtt.disconnect()
    print("\nGoodbye.\n")