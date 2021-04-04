import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import os
import boto3

MQTT_BROKER = "mqtt"
MQTT_RECEIVE = "cloud"
ACCESS_KEY = os.environ["ACCESS_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]


frame = np.zeros((240, 320, 3), np.uint8)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_RECEIVE)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global frame
    print("Received msg")
    # Decoding the message
    img = base64.b64decode(msg.payload)
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv.imdecode(npimg, 1)
    cli.put_object(
       Body=img,
       Bucket='ardenraw',
       Key='raw.jpg')

cli = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
client = mqtt.Client("p1")
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER)

# Starting thread which will receive the frames
client.loop_start()

while True:
    #cv.imshow("Stream", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the Thread
client.loop_stop()


