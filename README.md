[![Flake8 linter Actions Status](https://github.com/gerrowadat/mqttbow/workflows/Flake8%20linter/badge.svg)](https://github.com/gerrowadat/mqttbow/actions)
# mqttbow
An MQTT client for the pimoroni keybow.

Shopping list:
  - Raspberry Pi Model Zero (the last hassle is getting the WH model which has wifi and headers already on).
  - Pimoroni [Keybow](https://shop.pimoroni.com/products/keybow) or Keybow MINI (I'm using a Mini but will aim to have it work for both).

## Usage

Connect the Pi 0 to the back of the keybow, get a woring linux install on it, and log in.

First, install the pimoroni libraries, plus the dependencies they don't install :-/


```
pip install keybow-python RPi.GPIO spidev

```

Then install mqttbow itself:


```
pip install mqttbow
```

After this, hopefully things are self-explanatory:

```
usage: mqttbow.py [-h] [--implementation IMPLEMENTATION]
                  [--mqtt_broker MQTT_BROKER] [--mqtt_topic MQTT_TOPIC]
                  [--mqtt_user MQTT_USER] [--mqtt_pass MQTT_PASS]

optional arguments:
  -h, --help            show this help message and exit
  --implementation IMPLEMENTATION
                        Keyboard implementation. [keybow|simulated]
  --mqtt_broker MQTT_BROKER
                        MQTT broker host:port
  --mqtt_topic MQTT_TOPIC
                        MQTT base topic
  --mqtt_user MQTT_USER
                        MQTT user
  --mqtt_pass MQTT_PASS
                        MQTT password
```

If you don't have a keybow yet, you can use --implementation=simulated and it'll simulate a short and then long press.

As of 0.0.2 all this does is publish mqtt messages to the supplied topic, and read them back -- you can of course use other code to consume these messages.
