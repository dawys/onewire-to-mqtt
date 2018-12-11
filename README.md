# onewireToMqtt.py

onewireToMqtt.py is intended to run as a service, it connects to [owserver] and pushes the defined devices to MQTT

A running [owserver](http://owfs.org/index.php?page=owserver) and a mqtt-broker (e.g: [mosquitto](https://mosquitto.org)) are required to use this deamon.

## Usage

- install a broker like mosquitto
```
apt-get install mosquitto
```

- install software
```
apt-get install python-ow python-pip python-enum
pip install paho-mqtt

cd /usr/local/src

git clone https://github.com/dawys/onewire-to-mqtt onewireToMqtt

cd onewireToMqtt

cp config.xml.sample config.xml

cp onewire-to-mqtt.service /etc/systemd/system/

systemctl enable onewire-to-mqtt.service

vi config.xml

systemctl start onewire-to-mqtt.service
```
- edit config to your needs
```
<mqtt>
  <hostname>localhost</hostname>
  <port>1883</port>
  <username>username</username>
  <password>password</password>
</mqtt>

<onewire>
  <hostname>localhost</hostname>
  <port>4304</port>
</onewire>
```
- map your onewire devices to topics
```
<mqtt>
  <topics>
    <topic id="28.53111A000000" property="PIO.0" type="ON_OFF">heating/requestSwitch</topic>
    <topic id="21.00CDA0050000" property="temperature" type="FLOAT">heating/returnTemperature</topic>
    <topic id="15.A10066000000" property="counter.A" type="INTEGER">basement/totalElectricMeterPuls</topic>
  </topics>
</mqtt>
```
- if you want init some devices with defined values on startup
```
<onewire>
  <init>
    <device id="simultaneous" property="temperature">1</device>
    <device id="21.46A781000003" property="power">1</device>
  </init>
</onewire>
```

## Example
check if ist is working
```
mosquitto_sub -h localhost -u username -P password -v -t '#'

onewire/get/heating/requestSwitch ON
onewire/get/heating/returnTemperature 23.55
onewire/get/basement/totalElectricMeterPuls 5436
```
if you want to set values
```
mosquitto_pub -h localhost -u username -P password -t onewire/set/heating/requestSwitch -m OFF
mosquitto_pub -h localhost -u username -P password -t onewire/set/heating/returnTemperature -m 22.5
mosquitto_pub -h localhost -u username -P password -t onewire/set/basement/totalElectricMeterPuls -m 54355
```
if you want to init all devices
```
mosquitto_pub -h localhost -u username -P password -t onewire/set/inith -m true
```

if you are usinf openhab2 to read and write values
- install binding mqtt and edit services/mqtt.cfg
- define items
```
Item itemheatingRequestSwitch {mqtt=">[broker:onewire/set/heating/requestSwitch:*:default], <[broker:onewire/get/heating/requestSwitch:*:default]"}
Item itemheatingReturnTemperature {mqtt="<[broker:onewire/get/heating/requestSwitch:*:default]"}
```

## Configuration file

a self explaining sample configuration file is included 
copy config.xml.sample to config.xml

## Libs required
the following libraries are required by onewireToMqtt.py
- python-ow
- python-pip
- python-enum
- paho-mqtt

install with
```
apt-get install python-ow python-pip python-enum
pip install paho-mqtt
```
