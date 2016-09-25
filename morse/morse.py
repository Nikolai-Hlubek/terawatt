import time
import random
import logging

import paho.mqtt.client as mqtt

logging.basicConfig(format='%(asctime)s %(message)s', filename='morse.log', level=logging.DEBUG)
logger = logging.getLogger('morse')

placeholder='##id##'
url='io/cybus/energie-campus/rfid/'+placeholder+'/command/color'
ids=[14470220, 16290112, 12350008, 15400140]

def replace_url(id):
    return url.replace(placeholder, str(id))

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    #client.subscribe('io/cybus/energie-campus/signallampe/on/set')
    for i in ids:
        client.subscribe(replace_url(i))

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
    for i in ids:
        client.publish(replace_url(i), 'blue')

    time.sleep(2)
    counter=0
    while counter<3:
        logger.info('Start')
        counter=counter+1
        for m in morse:
            logger.info('Start publishing')
            #client.publish('io/cybus/energie-campus/signallampe/on/set', '1')
            for i in ids:
                client.publish(replace_url(i), 'red')
            logger.info('End publishing')
            time.sleep(m)
            #client.publish('io/cybus/energie-campus/signallampe/on/set', False)
            for i in ids:
                client.publish(replace_url(i), 'blue')
            time.sleep(s)
        print(counter)

    client.loop_stop()

if __name__ == '__main__':
    send_morse_code()
