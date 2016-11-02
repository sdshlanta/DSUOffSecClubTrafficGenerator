import random
from bs4 import BeautifulSoup
import time
import threading
import os
from pydhcplib.dhcp_network import * # for DHCP
import string

class host(object):
	"""
	represents a host
	ipaddr: the ip address of the host
	port: the port number of the service"""
	def __init__(self, host, serviceDict, tryFandCConn = False, delayFactor = 10, debug = False):
		self.host = host
		self.serviceDict = serviceDict
		self.address = self.host.address
		self.hostState = HostState(delayFactor, tryFandCConn, debug)
		self._serviceThreads = []
		self.services = [(serv.service, serv.port, serv.state) for serv in host.services if self.hostState.tryFandCConn or 'ed' not in serv.state ]
		
	def startTraffic(self):
		for serv in self.host.services:
			temp = None
			if self.hostState.tryFandCConn or 'ed' not in serv.state:
				temp = self.serviceDict.get(serv.service, None)
				# temp = self.serviceDict.get('', None)
				if temp != None:
					obj = temp(self.hostState)
					self._serviceThreads.append(obj.run(self.address, serv.port))
				else:
					temp = self.serviceDict['generic'](self.hostState)  
					self._serviceThreads.append(temp.run(self.address, serv.port, serv.protocol))
	
	def pauseTraffic(self):
		self.hostState.paused = True
	def resumeTraffic(self):
		self.hostState.paused = False
	def killTraffic(self):
		self.hostState.running = False

class ncThread(object):
	"""docstring for ncThread"""
	def __init__(self, hostState):
		super(ncThread, self).__init__()
		self.hostState = hostState
	def run(self, ipaddr, port):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t

class HostState(object):
	"""docstring for HostState"""
	def __init__(self, delayFactor, tryFandCConn = False, debug = False):
		super(HostState, self).__init__()
		self.paused = False
		self.running = True
		self.debug = debug
		self.delayFactor = delayFactor
		self.tryFandCConn = tryFandCConn

class ncDhcplient(DhcpClient):
	"""implmented for the dhcp client"""
	def __init__(self, options):
		DhcpClient.__init__(self,options["listen_address"],
							options["client_listen_port"],
							options["server_listen_port"])
	def HandleDhcpOffer(self, packet):
		print packet.str()
	def HandleDhcpAck(self, packet):
		print packet.str()
	def HandleDhcpNack(self, packet):
		print packet.str()

def delay(delayFactor, addtionalDelay=0):
	time.sleep((int(random.randint(0, delayFactor)))+addtionalDelay)

def get_urls_from_response(r):
	soup = BeautifulSoup(r.text, 'html.parser')
	urls = [link.get('href') for link in soup.find_all('a')]
	return urls

def randomword(length=6):
	return ''.join(random.SystemRandom().choice('%s%s' % (string.ascii_uppercase, string.digits)) for _ in range(length))

def justFuckingDie():
	killCmd = 'kill -9 %s;'
	killString = ''
	x = os.popen('ps ag | grep python').read().split('\n')
	for s in x:
		s=s[1:].strip()
		try:
			killString += killCmd % s[:s.index(' ')]
		except:
			continue
	os.system(killString)

