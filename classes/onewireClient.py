import logging;
import ow;
import time;
import threading;

from classes.topic import Type;
from device import Device;

class OnewireClient:

  __config = None;
  __mqttClient = None;
  __devices = {};

  def __init__(self, config, mqttClient):
    self.__setConfig(config);
    self.__setMqttClient(mqttClient);
    self.__setDevices({});
    
  def __getConfig(self):
    return self.__config;
	
  def __setConfig(self, config):
    self.__config = config;
	
  def __getMqttClient(self):
    return self.__mqttClient;
	
  def __setMqttClient(self, mqttClient):
    self.__mqttClient = mqttClient;

  def __getDevices(self):
	return self.__devices;
	
  def __setDevices(self, devices):
    self.__devices = devices;
	
  def start(self):
    if (self.__login()):
      while True:
        self.__readDevices();
	
  def __login(self):
    if (self.__getConfig().getOnewire().getHostname() != None and self.__getConfig().getOnewire().getPort() != None):
	
      ow.init(("%s:%s") % (self.__getConfig().getOnewire().getHostname(), str(self.__getConfig().getOnewire().getPort())));
      ow.error_level(ow.error_level.fatal);
      ow.error_print(ow.error_print.stderr);
	  
      for path, value in self.__getConfig().getOnewire().getInitDevices().items():
        try:
          ow._put(path, value);
        except ow.exUnknownSensor:
          logging.error("unknown sensor for deviceId \"%s\" and topic \"%s\"", temp.getId(), temp.getPath());
	
      return True;
	  
    return False;
		  
  def writeDevice(self, topic, value):
  
    if (topic == "init" and value.lower() == "true"):
	  self.__setDevices({});
	  logging.warning("inited devices!");
	  return;
  
    temp = self.__getConfig().getMqtt().getTopicByTopic(topic);
	
    if (temp != None):
      if (temp.getType() == Type.INTEGER):
        value = int(value);
      elif (temp.getType() == Type.LONG):
        value = long(value);
      elif (temp.getType() == Type.FLOAT):
        value = float(value);
      elif (temp.getType() == Type.ON_OFF):
        if (value == "0" or value.lower() == "off"):
          value = "0";
        else:
          value = "1";
		  
      if (temp.getType() == Type.ON_OFF and temp.getInvert()):
        if (value == "1"):
          value = "0";
        elif (value == "0"):
          value = "1";
  
      self.__publishDevice(temp, value, True);	
	  
      thread = threading.Thread(target=self.__writeDevice, args=[temp.getId(), temp.getProperty(), value]);
      thread.start();
		
  def __writeDevice(self, id, property, value):
    try:
      ow._put("/%s/%s" % (id, property), value);	
      logging.info("did update device \"%s\" with value \"%s\"", id, value);
		
    except ow.exUnknownSensor:
      logging.error("unknown sensor for deviceId \"%s\" and topic \"%s\"", temp.getId(), temp.getPath());

  def __readDevices(self):

    for topic in self.__getConfig().getMqtt().getTopics().values():

      now = int(time.time() * 100);
	  
      key = topic.getPath() + "/" + topic.getProperty();
	  
      update = False;
      if (key in self.__getDevices()):
        if (now - self.__getDevices()[key].getRefreshTime() > topic.getRefreshInterval() * 100):
          update = True;
      else:
        update = True;
		
      if (update):
        value = None;
        try:
          value = ow._get("/%s/%s" % (topic.getId(), topic.getProperty()));
        except ow.exUnknownSensor:
          logging.error("unknown sensor for deviceId \"%s\" and topic \"%s\"", topic.getId(), topic.getPath());
		
        self.__publishDevice(topic, value, False);
		
      time.sleep(0.1);
	  
  def __publishDevice(self, topic, value, force):
  
    if (value != None):
      if (topic.getType() == Type.INTEGER):
        value = int(value);
      elif (topic.getType() == Type.LONG):
        value = long(value);
      elif (topic.getType() == Type.FLOAT):
        value = float(value);
      elif (topic.getType() == Type.ON_OFF):
		if (value == "0"):
		  value = "OFF";
		else:
		  value = "ON";
			  
      if (topic.getType() == Type.ON_OFF and topic.getInvert()):
        if (value == "ON"):
          value = "OFF";
        elif (value == "OFF"):
          value = "ON";
			   
      update = False;

      refreshTime = int(time.time() * 100);
	  
      key = topic.getPath() + "/" + topic.getProperty();
				  
      if (key in self.__getDevices()):
        device = self.__getDevices()[key];

        if (value != device.getValue()):
          if (force or not device.getForce()):
            device.setRefreshTime(refreshTime);
            device.setValue(value);
            if (force):
              logging.info("set force to \"" + key + "\" and value \"" + str(value) + "\"");
              device.setForce(True);
            update = True;
        elif (not force and device.getForce()):
          logging.info("remove force from \"" + key + "\" and value \"" + str(value) + "\"");
          device.setForce(False);
      else:
        device = Device(value, refreshTime, None);
        if (force):
          logging.info("set force to \"" + key + "\" and value \"" + str(value) + "\"");
          device.setForce(True);	
        self.__getDevices()[key] = device;
        update = True;
					
      if (update):
        self.__getMqttClient().publish(topic.getPath(), str(device.getValue()));