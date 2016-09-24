import time
import random

import paho.mqtt.client as mqtt

url='io/cybus/energie-campus/rfid/14470220/command/color'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #client.subscribe('io/cybus/energie-campus/signallampe/on/set')
    client.subscribe(url)

def send_morse_code():
    client = mqtt.Client()
    client.username_pw_set('codingagents', password='C4fEGso7TD')
    client.on_connect = on_connect

    client.connect('energie-campus.cybus.io', 1883, 1)

    client.loop_start()

    l = 1
    s = 0.5
    end =3
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

    #client.publish('io/cybus/energie-campus/signallampe/on/set', False)
    client.publish(url, 'blue')

    time.sleep(2)
    counter=0
    while counter<3:
        print('Start')
        counter=counter+1
        for m in morse:
            print('Start publishing')
            #client.publish('io/cybus/energie-campus/signallampe/on/set', '1')
            client.publish(url, 'red')
            print('End publishing')
            time.sleep(m)
            #client.publish('io/cybus/energie-campus/signallampe/on/set', False)
            client.publish(url, 'blue')
            time.sleep(s)
        print(counter)

    client.loop_stop()

if __name__ == '__main__':
    send_morse_code()
