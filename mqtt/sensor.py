#!/usr/bin/env python
import time
import random

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

client = mqtt.Client()
client.on_connect = on_connect

client.connect("localhost", 1883, 60)

client.loop_start()

while True:
    time.sleep(2)
    client.publish("test/temperature", 
        '{\n"value": '+str(random.uniform(0, 100))+'\n,"timestamp": 2016-09-23 10:00:00}')
