import asyncio
import logging
from anseo import config
from anseo import keyinterface


async def process_keystrokes(cf, ki, key_q):
    while True:
        keypress = await key_q.get()
        if keypress:
            (hook_class, hook_args) = cf.get_hook(keypress[0], keypress[1].name)
            if hook_class:
                hook_obj = hook_class()
                await hook_obj.run(ki, hook_args)


async def main():
    logging.basicConfig(level=logging.DEBUG)
    key_q = asyncio.Queue()
    ki = keyinterface.KeyInterface(keyinterface.Implementation.SIMULATED)
    cf = config.Config()
    cf.Load(filename="example_config.cf")

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

    await asyncio.gather(seq_l.produce(key_q), process_keystrokes(cf, ki, key_q))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
