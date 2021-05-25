import asyncio
from anseo import keyinterface


async def listen_keys(ki, key_q):
    while True:
        keypress = await ki.async_wait()
        ki.show()
        await key_q.put(keypress)


async def light_keys(ki, led_q):
    while True:
        action = await led_q.get()
        print ('setting led: %s' % (str(action)))
        ki.set_led(*action)
        ki.show()

async def process_keystrokes(key_q, led_q):
    while True:
        keypress = await key_q.get()
        if keypress:
            print('Key %d %s' % (keypress[0], 'down' if keypress[1] else 'up'))
            if keypress[1]:
                await led_q.put((keypress[0], 255, 0, 0), )
            else:
                await led_q.put((keypress[0], 0, 0, 0), )


async def main():
    key_q = asyncio.Queue()
    led_q = asyncio.Queue()
    ki = keyinterface.KeyInterface(keyinterface.Implementation.SIMULATED)


    script = [
        'sleep 1',
        'down 1',
        'sleep 2',
        'up 1',
        'down 0'
    ]

    ki.setup(script=script)

    await asyncio.gather(listen_keys(ki, key_q), light_keys(ki, led_q), process_keystrokes(key_q, led_q))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
