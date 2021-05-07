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
# in this example we plot only 1 value, add more as needed
t = []
s = []
p = []
ii = 0

# mqtt callbacks
def data(c, u, message):
    # extract data from MQTT message
    # datRecord = open("data.txt","w")
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
        print("{}, {}, {}\n".format(f[0],f[1],f[2]))
        # datRecord.write("{}, {}, {}\n".format(f[0],f[1],f[2]))
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

def plot(client, userdata, message):
    # customize this to match your data
    # print("plotting ...")
    (ax1,ax2) = plt.subplot(2,1,sharex = True)
    ax1.plot(t, s)
    ax1.xlabel('Time (s)')
    ax1.ylabel('Valve Position (degrees)')
    ax2.plot(t, p)
    # ax2.xlabel('Time (s)')
    ax2.ylabel('Pressure (psi)')
    # print("show plot ...")
    # show plot on screen
    plt.show()

    t = []
    s = []
    p = []
    msg = message.payload.decode('ascii')
    f = [ float(x) for x in msg.split(',') ]
    t = f[0]
    

# subscribe to topics
data_topic = "{}/data".format(session, qos)
plot_topic = "{}/plot".format(session, qos)
set_topic = "{}/set".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.subscribe(plot_topic)
mqtt.message_callback_add(data_topic, data)
mqtt.message_callback_add(plot_topic, plot)

# Send requested set pressure over mqtt
setPressure = input("Enter desired tank pressure: ")
mqtt.publish(set_topic, setPressure)

# wait for MQTT messages
# this function never returns

mqtt.loop_forever()