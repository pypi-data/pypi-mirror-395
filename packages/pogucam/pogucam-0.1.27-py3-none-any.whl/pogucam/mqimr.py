#!/usr/bin/env python3

print("""
RECEIVE IMAGE

uv run --with paho-mqtt --with=numpy --with=opencv-python --script ./mqimr.py

show an image received from mqtt
""")


import struct
import paho.mqtt.client as mqtt
import numpy as np
import datetime as dt
import cv2

broker = "10.10.104.17"
broker = "127.0.0.1"
topic = "image/raw8000"

def decode_payload(data):
    header_size = struct.calcsize('!HHQddIfff')
    width, height, framenumber, timestamp_ts, recording_started_ts, _, exposition, gain, gamma = struct.unpack('!HHQddIfff', data[:header_size])
    image = np.frombuffer(data[header_size:], dtype=np.uint8).reshape((height, width, 3))
    timestamp = dt.datetime.fromtimestamp(timestamp_ts)
    recording_started = dt.datetime.fromtimestamp(recording_started_ts)
    return {
        'width': width,
        'height': height,
        'framenumber': framenumber,
        'timestamp': timestamp,
        'recording_started': recording_started,
        'exposition': exposition,
        'gain': gain,
        'gamma': gamma,
        'image': image
    }


def on_message(client, userdata, msg):
    data = msg.payload

    data_block = decode_payload(data)
    image = data_block['image']
    #
    #width, height = struct.unpack('!HH', data[:4])
    #image = np.frombuffer(data[4:], dtype=np.uint8).reshape((height, width, 3))
    #####image = np.frombuffer(data, dtype=np.uint8).reshape((480, 640, 3))
    print("Received image shape:", image.shape, dt.datetime.now() )
    print( flush=True)

    cv2.imshow("Received Image", image)
    cv2.waitKey(10)  # Needed to refresh window

client = mqtt.Client()
client.on_message = on_message

client.connect(broker, 1883, 60)
client.subscribe(topic)
client.loop_forever()
