# onewireToMqtt.py

onewireToMqtt.py is intended to run as a service, it connects to [owserver] and pushes the defined devices to MQTT

## Usage

## Example

## Configuration file

a self explaining sample configuration file is included 
copy config.xml.sample to config.xml

## Libs required
the following libraries are required by onewireToMqtt.py
- python-ow
- python-pip
- python-enum
- paho-mqt

install with
```
apt-get install python-ow python-pip python-enum
pip install paho-mqt
```