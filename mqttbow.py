import asyncio
import logging
import asynckeybow


async def process_keystrokes(ki, key_q):
    while True:
        keypress = await key_q.get()
        if keypress:
            print('Key Press: %s' % (keypress, ))


async def main():
    logging.basicConfig(level=logging.DEBUG)
    key_q = asyncio.Queue()

    # ki = asynckeybow.KeyInterface(asynckeybow.Implementation.KEYBOW)
    ki = asynckeybow.KeyInterface(asynckeybow.Implementation.SIMULATED)

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

    await asyncio.gather(seq_l.produce(key_q), process_keystrokes(ki, key_q))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
