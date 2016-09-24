import time
import random

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe('io/cybus/energie-campus/signallampe/on/set')

def send_morse_code():
    client = mqtt.Client()
    client.username_pw_set('codingagents', password='C4fEGso7TD')
    client.on_connect = on_connect

    client.connect('energie-campus.cybus.io', 1883, 1)

    client.loop_start()

    l = 3
    s = 1
    end =4
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

    client.publish('io/cybus/energie-campus/signallampe/on/set', False)

    time.sleep(10)
    counter=0
    while counter<1:
        print('Start')
        counter=counter+1
        for m in morse:
            print('Start publishing')
            client.publish('io/cybus/energie-campus/signallampe/on/set', '1')
            print('End publishing')
            time.sleep(m)
            client.publish('io/cybus/energie-campus/signallampe/on/set', False)
            time.sleep(s)
        print(counter)

    client.loop_end()

if __name__ == '__main__':
    send_morse_code()
