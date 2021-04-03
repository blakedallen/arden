import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import os

MQTT_BROKER = 'brokercontainer'
MQTT_RECEIVE = "image"

#MQTT_BROKER_AWS = "ec2-3-101-26-64.us-west-1.compute.amazonaws.com" #IP of AWS EC2 Instance Broker
MQTT_BROKER_AWS = "3.101.26.64" #IP of AWS EC2 Instance Broker




frame = np.zeros((240, 320, 3), np.uint8)
data = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_RECEIVE)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global frame
    # Decoding the message
    img = base64.b64decode(msg.payload)
    clientAWS.publish("cloud", msg.payload)#publish
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv.imdecode(npimg, 1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)

clientAWS = mqtt.Client("P2") #create new instance
clientAWS.connect(MQTT_BROKER_AWS) #connect to broker

# Starting thread which will receive the frames
client.loop_start()

while True:
    cv.imshow("Stream", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the Thread
client.loop_stop()
