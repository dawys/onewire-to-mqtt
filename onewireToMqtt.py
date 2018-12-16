#!/usr/bin/env python

import logging;
import sys;

from classes.config import Config;
from classes.mqttClient import MqttClient;
from classes.onewireClient import OnewireClient;

class OnewireToMqtt:

	def __init__(self):

		config = Config();

		mqttClient = MqttClient(config);
		onewireClient = OnewireClient(config, mqttClient);
		mqttClient.subscribe(onewireClient.writeDevice);
		onewireClient.start();
 
if __name__ == "__main__":
	OnewireToMqtt();