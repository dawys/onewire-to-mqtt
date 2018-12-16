import logging;

class OnewireConfig:

	__hostname = "localhost";	
	__port = 4304;
	__initDevices = None;
	
	def __init__(self, root):
	
		self.setInitDevices({});

		hostname = root.find("onewire/hostname");
		if (hostname != None and hostname.text.strip() != ""):
			self.setHostname(hostname.text.strip());
			
		port = root.find("onewire/port");
		if (port != None and port.text.strip() != ""):
			self.setPort(int(port.text.strip()));
		
		logging.info("Init devices configured:");
		devices = root.findall("onewire/init/device");
		if (devices != None):
			for entry in devices:
				attributes = entry.attrib;
		
				if (entry.text != None and len(entry.text.strip()) > 0 and "id" in attributes and "property" in attributes and attributes["id"] != None and len(attributes["id"].strip()) > 0 and attributes["property"] != None and len(attributes["property"].strip()) > 0):
			
					self.getInitDevices()["/" + attributes["id"].strip() + "/" + attributes["property"].strip()] = entry.text.strip();
			
					logging.info("/" + attributes["id"].strip() + "/" + attributes["property"].strip() + " > " + entry.text.strip());

	def getHostname(self):
		return self.__hostname;

	def setHostname(self, hostname):
		self.__hostname = hostname;

	def getPort(self):
		return self.__port;

	def setPort(self, port):
		self.__port = port;
	
	def getInitDevices(self):
		return self.__initDevices;

	def setInitDevices(self, initDevices):
		self.__initDevices = initDevices;