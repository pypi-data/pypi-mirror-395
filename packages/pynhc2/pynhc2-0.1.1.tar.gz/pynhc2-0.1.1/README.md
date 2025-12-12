# pynhc2

version = 0.1.1

Lightweight Python wrapper library to interact with Niko Home Control 2 systems built on top of paho-mqtt. Includes functionality to read NHC2 config files for better device readability. The library is primary built for home use.

<!--[![PyPI version](https://badge.fury.io/py/pynhc2.svg)](https://badge.fury.io/py/pynhc2)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)-->

## Installation

```bash
pip install pynhc2
```

## Quick Start

```python
from pynhc2 import MQTTConnector, Lamp

# Connect to Niko Home Control
conn = MQTTConnector(
    broker="192.168.1.10",
    jwt="your-jwt-token",
    ca_cert="path/to/ca.pem"
)
conn.connect()

# Control a lamp
lamp = Lamp(mqttconnector=conn, device_uuid="lamp-uuid")
lamp.switch_on()
lamp.set_brightness("75")
```

## Documentation

The Device and Lamp classes are used to easily control individual devices. Using the NHC2FileReader, it is possible to loop through all devices in your home installation and create Device or Lamp objects that are easily human readable.

The MessageHandler and MultiMessageHandler make it possible to use incoming messages for specific devices to trigger certain output actions; this can be methods for existing Device or Lamp objects, but also actions that have nothing to do with NHC, allowing devices like Shelly to be controlled through NHC.

Under the _hobby/control/devices/evt_ topic, the NHC Connected Controller - which also acts as MQTT message broker - does not publish events for button-type devices (e.g. 'button pressed') but it does this for the devices these buttons command (e.g. "Properties":[{"Status":"Off"}, {"Brightness": "50"}] when a button connected to a lamp is pressed).

The MessageHandler and MultiMessageHandler circumvent this setup by using the devices whose properties have changed to trigger the actions.

<!--
Full documentation is available at [ReadTheDocs](https://pynhc2.readthedocs.io/). 

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.
-->

## License

MIT License - see [LICENSE](LICENSE) file for details.
