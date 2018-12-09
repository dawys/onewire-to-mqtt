import sys;
import os;
import xml.etree.ElementTree as et;

from loggingConfig import LoggingConfig;
from mqttConfig import MqttConfig;
from onewireConfig import OnewireConfig;

class Config:
    __logging = None;
    __mqtt = None;
    __onewire = None;
    
    def __init__(self):
	
      path = os.path.dirname(sys.argv[0]);
    
      # parse xml
      tree = et.parse(os.path.join (path, "config.xml"));
      
      root = tree.getroot();
      
      LoggingConfig(root);
	  
      self.setMqtt(MqttConfig(root));
      self.setOnewire(OnewireConfig(root));
      
    def getMqtt(self):
      return self.__mqtt;
        
    def setMqtt(self, mqtt):
      self.__mqtt = mqtt;
      
    def getOnewire(self):
      return self.__onewire;
      
    def setOnewire(self, onewire):
      self.__onewire = onewire;