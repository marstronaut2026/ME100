import paho.mqtt.client as paho
import matplotlib.pyplot as plt

session = "SEB/RegulatorDemo"
BROKER = "broker.mqttdashboard.com"
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

datRecord = open("data.txt","w")

def data(c, u, message):
    # extract data from MQTT message

    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [float(x) for x in msg.split(',')]
    # print("received", f)
    # append to data vectors, add more as needed
    datRecord.write("{}, {}, {}\n".format(f[0], f[1], f[2]))


data_topic = "{}/data".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.message_callback_add(data_topic, data)

print("Waiting for data...\n")

try:
    mqtt.loop_forever()

except KeyboardInterrupt:
    datRecord.close()
    mqtt.disconnect()
    print("Goodbye.")