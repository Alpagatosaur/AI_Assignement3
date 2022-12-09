# -*- coding: utf-8 -*-
import time
import datetime
import numpy as np

from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
topic = "teds22/group05/pressure"

# generate client ID with pub prefix randomly
client_id = 'python-mqtt-05'


client = mqtt_client.Client(client_id)


print("connect to broker ", broker)
client.connect(broker)

mu, sigma = 1200.00, 1.0
msg_count = 0

# Start msg loop
client.loop_start()

while msg_count < 10:
    # Make sure the msg is delivered
    time.sleep(1)
    reading = f'{round(np.random.normal(mu, sigma), 2):.2f}'
    dt = datetime.datetime.now()
    dt = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    message = f'{reading}|{dt}'

    result = client.publish(topic, message, qos=2)
    print(f"Send `{message}` ")
    msg_count += 1

# Wait 4 s
time.sleep(4)

# Stop loop
client.loop_stop()

# Disconnect
client.disconnect()