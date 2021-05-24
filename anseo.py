import time
from anseo import keyinterface


def main():
    ki = keyinterface.KeyInterface(keyinterface.Implementation.KEYBOW)
    ki.setup(keycount=3)

    while True:
        ki.show()
        time.sleep(1.0 / 60.0)


if __name__ == '__main__':
    main()
