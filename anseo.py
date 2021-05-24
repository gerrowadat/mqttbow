import time
from anseo import keyinterface


def key_handler(idx, state):
    print("{}: Key {} has been {}".format(
        time.time(),
        idx,
        'pressed' if state else 'released'))


def main():
    ki = keyinterface.KeyInterface(keyinterface.Implementation.KEYBOW)
    ki.setup()
    # keybow mini so 3 keys
    for k in range(3):
        ki.set_handler(k,key_handler)

    while True:
        ki.show()
        time.sleep(1.0 / 60.0)


if __name__ == '__main__':
    main()
