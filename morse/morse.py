import time
import random

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def send_morse_code():
    client = mqtt.Client()
    client.username_pw_set('codingagents', password='C4fEGso7TD')
    client.on_connect = on_connect

    client.connect('energie-campus.cybus.io', 1883, 60)

    client.loop_start()

    l = 1
    s = 0.5
    end = 1.5
    morse = [
        l, s, l, s, end,  # c
        l, l, l, end,     # o
        l, s, s, end,     # d
        s, s, end,        # i
        l, s, end,        # n
        l, l, s, end,     # g
        end, end,
        s, l, end,        # a
        l, l, s, end,     # g
        s, end,           # e
        l, s, end,        # n
        l, end,           # t
        s, s, s             # s
    ]

    counter=0
    while counter<50:
        counter=counter+1
        for m in morse:
            client.publish('io/cybus/energie-campus/signallampe/signallampe/on/set', 'true')
            time.sleep(m)
            client.publish('io/cybus/energie-campus/signallampe/signallampe/on/set', 'false')

    client.loop_stop()

if __name__ == '__main__':
    send_morse_code()
