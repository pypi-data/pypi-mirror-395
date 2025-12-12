#!/usr/bin/env python3


print(""" SEND IMAGE via MQTT

 uv run --with paho-mqtt --with=numpy --with=opencv-python --script   ./mqims.py

""")
#  connect to local MQTT
broker = "127.0.0.1"
topic = "image/raw8000"

import struct
import paho.mqtt.client as mqtt
import numpy as np
import datetime as dt
import time
import click

# ================================================================================
#
# --------------------------------------------------------------------------------

def create_mqtt_payload(image, framenumber, timestamp, recording_started, exposition, gain, gamma):
    height, width = image.shape[:2]
    header = struct.pack(
        '!HHQddIfff',
        width,
        height,
        int(framenumber),
        timestamp.timestamp(),
        recording_started.timestamp(),
        0,  # padding for alignment if needed
        float(exposition),
        float(gain),
        float(gamma)
    )
    payload = header + image.tobytes()
    return payload


# ================================================================================
#
# --------------------------------------------------------------------------------


def provide_image(width, height):
    # Add random noise element
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    #return image # 1ms for just black
    noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
    #image = np.clip(image + noise, 0, 255).astype(np.uint8)
    #return image # 6.6ms  image+noise
    #---------------------------------------
    # Create colorful structured image with gradients and sinusoidal patterns
    x = np.linspace(0, 4 * np.pi, width)
    y = np.linspace(0, 4 * np.pi, height)
    X, Y = np.meshgrid(x, y)
    r = ((np.sin(X) + 1) * 127).astype(np.uint8)
    g = ((np.cos(Y) + 1) * 127).astype(np.uint8)
    b = ((np.sin(X + Y) + 1) * 127).astype(np.uint8)

    # Randomize grid frequency and color amplitude
    freq_x = np.random.uniform(2, 6)
    freq_y = np.random.uniform(2, 6)
    amp = np.random.uniform(80, 150)
    x = np.linspace(0, freq_x * np.pi, width)
    y = np.linspace(0, freq_y * np.pi, height)
    X, Y = np.meshgrid(x, y)
    r = ((np.sin(X) + 1) * amp / 2).clip(0, 255).astype(np.uint8 )
    g = ((np.cos(Y) + 1) * amp / 2).clip(0, 255).astype(np.uint8)
    b = ((np.sin(X + Y) + 1) * amp / 2).clip(0, 255).astype(np.uint8)
    image = np.stack((r, g, b), axis=2)
    image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return image # alltogether 35 ms


# *********************************************************************
# ================================================================================
#
# --------------------------------------------------------------------------------


@click.command()
@click.argument("port", default=8000)
def main(port):
    global topic, broker
    topic = topic.replace("8000", str(port))
    client = mqtt.Client()
    client.connect(broker, 1883, 10)

    recording_started = dt.datetime.now()
    framenumber = 0
    for i in range(1000):
        # Create dummy image
        #image = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
        height,width=1080,1920
        #
        height,width=480,640
        #header = struct.pack('!HH', width, height)  # Network byte order
        timestamp = dt.datetime.now()
        framenumber += 1
        #recording_started  ...   also timestamp
        image=provide_image(width, height) # create image elsewhere
        exposition, gain, gamma = 0.5, 0.5, 0.5
        payload = create_mqtt_payload(image, framenumber, timestamp, recording_started, exposition, gain, gamma)
        #payload = header + image.tobytes()
        # Send raw bytes
        result=client.publish(topic, payload )
        print(timestamp, end="\r")
        #result.wait_for_publish()  # Ensure message is sent before continuing
        #print(dt.datetime.now())

        #
        time.sleep(0.095) # 10fps
        time.sleep(0.095) #

    delta = dt.datetime.now() - recording_started
    print(f"{delta}, {delta.total_seconds() / 1000} per frame             ")
    client.disconnect()

# ================================================================================
#
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
