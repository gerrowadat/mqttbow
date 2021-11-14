import time
import asyncio
import logging
import argparse
import asynckeybow
from hbmqtt.client import MQTTClient, ConnectException
from hbmqtt.mqtt.constants import QOS_1


async def process_keystrokes(ki, mqtt, base_topic, key_q):
    while True:
        keypress = await key_q.get()
        if keypress:
            topic = base_topic + str(keypress[0]) + '/%s' % (keypress[1].name)
            payload = str(time.time())
            logging.debug('MQTT Publish: [%s]: %s' % (topic, payload))
            await mqtt.publish(topic, payload.encode('ascii'))


async def process_mqtt(ki, mqtt):
    while True:
        mqtt_msg = await mqtt.deliver_message()
        pkt = mqtt_msg.publish_packet
        print("%s => %s" % (pkt.variable_header.topic_name, str(pkt.payload.data)))


async def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--implementation', default='keybow', help='Keyboard implementation. [keybow|simulated]')
    parser.add_argument('--mqtt_broker', default='mqtt:1883', help='MQTT broker host:port')
    parser.add_argument('--mqtt_topic', default='keybow/press/', help='MQTT base topic')
    parser.add_argument('--mqtt_user', default=None, help='MQTT user')
    parser.add_argument('--mqtt_pass', default=None, help='MQTT password')
    args = parser.parse_args()

    # Setup the keybow interface (or simulation).
    if args.implementation == 'keybow':
        ki = asynckeybow.KeyInterface(asynckeybow.Implementation.KEYBOW)
    elif args.implementation == 'simulated':
        ki = asynckeybow.KeyInterface(asynckeybow.Implementation.SIMULATED)
    else:
        logging.error('--implementation must be [keybow|simulated]')
        return

    script = [
        'down 1',
        'sleep 0.2',
        'up 1',
        'down 0',
        'sleep 0.6',
        'up 0'
    ]

    ki.setup(script=script)

    seq_l = asynckeybow.KeySequenceListener(ki, listen_for=[asynckeybow.KeySequence.SINGLE, asynckeybow.KeySequence.HOLD])

    # Set up the MQTT Publisher
    mqtt = MQTTClient()

    if args.mqtt_user:
        mqtt_url = 'mqtt://%s:%s@%s' % (args.mqtt_user, args.mqtt_pass, args.mqtt_broker)
        logging.debug('Connecting to MQTT broker at %s with username %s' % (args.mqtt_broker, args.mqtt_user))
    else:
        mqtt_url = 'mqtt://%s' % (args.mqtt_broker)
        logging.debug('Connecting Anonymously to MQTT broker at %s' % (args.mqtt_broker))

    try:
        await mqtt.connect(mqtt_url)
    except ConnectException as e:
        logging.error('Error connecting to MQTT broker: %s' % str(e))
        return

    await mqtt.subscribe([('%s#' % (args.mqtt_topic), QOS_1)])

    key_q = asyncio.Queue()

    await asyncio.gather(seq_l.produce(key_q), process_keystrokes(ki, mqtt, args.mqtt_topic, key_q), process_mqtt(ki, mqtt))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
