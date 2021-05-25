import asyncio
from anseo import keyinterface


async def listen_keys(queue):
    ki = keyinterface.KeyInterface(keyinterface.Implementation.SIMULATED)

    script = [
        'sleep 1',
        'down 1',
        'sleep 2',
        'up 1',
        'down 0'
    ]

    ki.setup(script=script)

    while True:
        keypress = await ki.async_wait()
        ki.show()
        await queue.put(keypress)


async def print_keys(queue):
    while True:
        keypress = await queue.get()
        if keypress:
            print('Key %d %s' % (keypress[0], 'down' if keypress[1] else 'up'))


async def main():
    q = asyncio.Queue()
    await asyncio.gather(listen_keys(q), print_keys(q))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
