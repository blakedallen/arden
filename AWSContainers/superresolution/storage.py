import base64
import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt
import os
import boto3
import time
from PIL import Image
import io


from super import super_res

MQTT_BROKER = "mqtt"
MQTT_RECEIVE = "cloud"

frame = np.zeros((240, 320, 3), np.uint8)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_RECEIVE)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg, bucket="blakedallen-mids/w251/arden/"):
    global frame
    print("Received msg")
    # Decoding the message
    img = base64.b64decode(msg.payload)
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Decode to Original Frame
    frame = cv.imdecode(npimg, 1)

    img_id = time.time()

    cli.put_object(
       Body=img,
       Bucket='blakedallen-mids/w251/arden/low_res/',
       Key='{}.jpg'.format(img_id))

    #create a super resolution version
    arr = super_res_arr(npimg)
    pil_image = Image.fromarray(arr)
    # Save the image to an in-memory file
    in_mem_file = io.BytesIO()
    pil_image.save(in_mem_file, format=pil_image.format)
    in_mem_file.seek(0)
    cli.put_object(
       Body=img,
       Bucket='blakedallen-mids/w251/arden/super_res/',
       Key='{}.jpg'.format(img_id))


cli = boto3.client('s3')
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


