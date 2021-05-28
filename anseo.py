import asyncio
from anseo import keyinterface


async def light_keys(ki, led_q):
    while True:
        action = await led_q.get()
        print('setting led: %s' % (str(action)))
        ki.set_led(*action)
        ki.show()


async def process_keystrokes(key_q, led_q):
    while True:
        keypress = await key_q.get()
        if keypress:
            print('Key %d %s' % (keypress))
            if keypress[1] == keyinterface.KeySequence.SINGLE:
                await led_q.put((keypress[0], 255, 0, 0), )
            elif keypress[1] == keyinterface.KeySequence.HOLD:
                await led_q.put((keypress[0], 0, 255, 0), )
            await asyncio.sleep(0.2)
            await led_q.put((keypress[0], 0, 0, 0), )


async def main():
    key_q = asyncio.Queue()
    led_q = asyncio.Queue()
    ki = keyinterface.KeyInterface(keyinterface.Implementation.SIMULATED)

    script = [
        'down 1',
        'sleep 0.2',
        'up 1',
        'down 0',
        'sleep 0.6',
        'up 0'
    ]

    ki.setup(script=script)

    seq_l = keyinterface.KeySequenceListener(ki, listen_for=[keyinterface.KeySequence.SINGLE, keyinterface.KeySequence.HOLD])

    await asyncio.gather(seq_l.produce(key_q), light_keys(ki, led_q), process_keystrokes(key_q, led_q))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
