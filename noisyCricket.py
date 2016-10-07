#!/usr/bin/python

#Python traffic generator by YoNotHim

#takes the xml output of an nmap scan filename is set with input file.
#trys to connect to any common network services it is given by the nmap report
#makes a looooot of threads so if that is a problem for you keep that in mind
#may add support for masscan at some point but mehs


from libnmap.parser import NmapParser #for parsing nmap for generating the host list
from bs4 import BeautifulSoup # for parsing the receved html for the spider because im lazy
from pydhcplib.dhcp_packet import * # for DHCP
from pydhcplib.dhcp_network import * # for DHCP
from ftplib import FTP #for FTP
from email.mime.text import MIMEText
from smb.SMBConnection import SMBConnection
#import json #for parsing mascan use the -oJ <filename> to generate the output file
import socket #for generic requests
import telnetlib #telnet
import paramiko, base64 #SSH
import requests #for HTTP
import smtplib, imaplib, poplib #for SMTP IMAP and POP3, basicly all email
import tftpy #for TFTP
import dns.resolver as dnsResolver # for DNS
import pysftp # for SFTP
import threading
import random, string
import time
import email.utils
import sys
import argparse
import cPickle
import tempfile


#actual globaly scoped varables
hostlist = []

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Creates "cover traffic" for red teams during capture the flag events events')
	parser.add_argument('-f', type=str, default='nmap.xml', help="The name the file containing XML output from nmap, uses nmap.xml by default")
	parser.add_argument('-D', action='store_true', default=False, help="Enables Debugging, will cause strange things to hapen with the UI")
	parser.add_argument('-r', action='store_true', default=False, help='Tells the script to wait for input from a command and controll server.')
	parser.add_argument('-l', type=int, default=3, help="Sets how deep the spider will go.")
	parser.add_argument('-d', type=int, default=10, help="Sets the highest posable delay between the sending of packets")
	parser.add_argument('-c', action='store_true', default=False, help='force the program to atempt to connect to filtered and closed connections')

	args=parser.parse_args()

	#config
	atemptFilteredAndClosedConnections = args.c
	inputFile = args.f
	debug = args.D
	delayFactor = args.d #the value time is modded by
	maxLinksFollowed = args.l
	underRemoteControll = args.r

listenPort = 12407

def boilerPlate(servName):
	def realDec(opener):
		def newOpen(*args, **kwargs):
			print(servName)
			while not TheEndOfTime:
				try:
					opener(*args, **kwargs)
				except Exception, e:
					if debug:
						print servName
						print e
					else:
						pass
				delay()
		return newOpen
	return realDec


def get_urls_from_response(r):
	soup = BeautifulSoup(r.text, 'html.parser')
	urls = [link.get('href') for link in soup.find_all('a')]
	return urls

def randomword(length=6):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def rand():
	return random.SystemRandom().random()*1000000000000000000 # ignore the magic number

def delay(addtionalDelay=0):
	time.sleep((int(rand())%delayFactor)+addtionalDelay)

class Client(DhcpClient):
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

class telnet(object):
	"""docstring for telnet"""
	def __init__(self):
		super(telnet, self).__init__()
	def run(self, ipaddr, port=23):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		tn = telnetlib.Telnet(ipaddr, port)

		tn.read_until("login: ", 2)
		tn.write("le" + randomword(2).lower() + "gi" + randomword(2).lower() + "tU" + randomword(2).lower() + "se" + "r" + "\n") #type some random junk for the username
		tn.read_until("Password: ", 2)
		tn.write(randomword() + "DontBanPlx\n") #type some random junk for the password

		#these should never ever ever execute but if the do it does an ls and exits
		tn.write("ls\n")
		delay(-1)
		tn.write("exit\n")
		delay(-1)


class ftp(object):
	"""docstring for ftp"""
	def __init__(self):
		super(ftp, self).__init__()
	def run(self, ipaddr, port=21):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		ftpClient = FTP()
		ftpClient.connect(ipaddr, port)
		ftpClient.login() #anon login
		ftpClient.retrlines('list') #do a thing
		ftp.quit() #gtfo

class sftp(object):
	"""docstring for sftp"""
	def __init__(self):
		super(sftp, self).__init__()
	def run(self, ipaddr, port=115):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		connection = pysftp.Connection(ipaddr, port, username='notABruteForce'+randomword(), password='seriouslyThisIsLegit' + randomword())
		connection.close()

class tftp(object):
	"""docstring for tftp"""
	def __init__(self):
		super(tftp, self).__init__()
	def run(self, ipaddr, port=69):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		client = tftpy.TftpClient(ipaddr, port)
		tftpFileName = 'tftp.tmp'
		fp = file(tftpFileName, 'w')
		fp.write(randomword(256))
		client.upload(tftpFileName, tftpFileName)
		client.download('exists', 'downloaded.dat')

class http(object):
	"""docstring for http"""
	def __init__(self):
		super(http, self).__init__()
		self.depth = 0
	def run(self, ipaddr, port=80):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port): #this also spiders the site
		self.depth = 0
		url = 'http://' + str(ipaddr)
		r=requests.get(url)
		while True:
			links = get_urls_from_response(r)
			if len(links) == 0 or self.depth <= maxLinksFollowed:
				break
			r= requests.get(random.choice(set(links)))
			delay(2)
			self.depth += 1

class https(object):
	"""docstring for https"""
	def __init__(self):
		super(https, self).__init__()
		self.depth = 0
	def run(self, ipaddr, port=443):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		self.depth = 0
		url = 'https://' + str(ipaddr)
		r=requests.get(url, verify=True)

		while True:
			links = get_urls_from_response(r)
			if len(links) == 0 or self.depth <= maxLinksFollowed:
				break
			r= requests.get(random.choice(set(links)), verify=True)
			delay(2)
			self.depth += 1

class httpProxy(object):
	"""docstring for httpProxy"""
	def __init__(self):
		super(httpProxy, self).__init__()
		self.depth =0
	def run(self, ipaddr, port):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		self.depth = 0
		url = 'http://' + str(ipaddr)
		try:
			r=requests.get(url)
		except Exception, e:
			if debug:
				print 'http-proxy'
				print e
			try:
				url = 'https://' + str(ipaddr)
				r=requests.get(url, verify=True)
			except Exception, e:
				if debug:
					print 'http-proxy'
					raise e
				else:
					pass
		try:
			while True:
				links = get_urls_from_response(r)
				if len(links) == 0 or self.depth <= maxLinksFollowed:
					break
				r= requests.get(random.choice(set(links)))
				delay(2)


class ssh(object):
	"""docstring for ssh"""
	def __init__(self):
		super(ssh, self).__init__()
	def run(self, ipaddr, port=22):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		sshC = paramiko.SSHClient()
		sshC.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		sshC.connect(hostname=ipaddr, port=port username=randomword(), password=randomword(8))
		stdin, stdout, stderr = ssh.exec_command('ls')
		ssh.close()

class pop(object):
	"""docstring for pop3"""
	def __init__(self):
		super(pop, self).__init__()
	def run(self, ipaddr, port=110):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		M = poplib.POP3(ipaddr, port)
		M.user("le" + randomword(2).lower() + "gi" + randomword(2).lower() + "tU" + randomword(2).lower() + "se" + "r" + "\n")
		M.pass_(randomword(6))
		numMessages = len(M.list()[1])
		for i in range(numMessages):
			for j in M.retr(i+1)[1]:
				pass
class smtp(object):
	"""docstring for smtp"""
	def __init__(self):
		super(smtp, self).__init__()
		self.msg = MIMEText('This is the body of the message.')
		self.msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
		self.msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
		self.msg['Subject'] = 'Simple test message'
	def run(self, ipaddr, port=25): #smtp runs on port 25
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		server = smtplib.SMTP(ipaddr, port)
		server.sendmail('author@example.com', ['recipient@example.com'], self.msg.as_string())

class imap(object):
	"""docstring for imap"""
	def __init__(self):
		super(imap, self).__init__()
	def run(self, ipaddr, port=143):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		M = imaplib.IMAP4(ipaddr, port)
		M.login(getpass.getuser(), getpass.getpass())
		M.select()
		typ, data = M.search(None, 'ALL')
		#for num in data[0].split():
		#	typ, data = M.fetch(num, '(RFC822)')
		typ, data = map(lambda x: M.fetch(x, '(RFC822)'), data[0].split())
		M.logout()
		M.close()


class dhcp(object):
	"""docstring for dhcp"""
	def __init__(self):
		super(dhcp, self).__init__()

	def run(self, ipaddr='255.255.255.255', port=67):
		self.netopt = {'client_listen_port':68,
					   'server_listen_port':port,
					   'listen_address':str(ipaddr)}
		self.client = Client(self.netopt)
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		self.client.BindToAddress()
		self.client.GetNextDhcpPacket()

class dns(object):
	"""docstring for dns"""
	def __init__(self):
		super(dns, self).__init__()
	def run(self, ipaddr='8.8.8.8', port=22):
		self.resolver = dnsResolver.Resolver()
		self.resolver.nameservers = [str(ipaddr)] #specify the ip address of the nameserver
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		answers = dns.resolver.query( randomword() + "." + randomword() + ".com", dns.rdtypes.ANY)

class smb(object):
	"""docstring for smb"""
	def __init__(self):
		super(smb, self).__init__()
	def run(self, ipaddr, port=22):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		conn = SMBConnection(randomword(), randomword, randomword, ipaddr, use_ntlm_v2 = True)

class daytime(object):
	"""docstring for daytime"""
	def __init__(self):
		super(daytime, self).__init__()
	def run(self, ipaddr, port=13):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	@boilerPlate(self.__class__.__name__)
	def open(self, ipaddr, port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ipaddr,port))
		while True:
			data = s.recv(10000)
			if data:
				pass
			else:
				break
		s.close()

class generaric(object):
	"""docstring for generaric"""
	def __init__(self):
		super(generaric, self).__init__()
	def run(self, ipaddr, port, protocol, packetSize=64):
		t = threading.Thread(target=self.open, args=(ipaddr, port, protocol, packetSize))
		t.start()
		return t
	#weird eough case not to get boiler plate
	def open(self, ipaddr, port, protocol, packetSize):
		print '*'
		print protocol
		if protocol == 'tcp':
			while not TheEndOfTime:
				try:
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect((ipaddr,port))
					sock.send(randomword(packetSize))
					sock.close()
				except Exception, e:
					sock.close()
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					if debug:
						print 'TCP'
						print e
				delay()
		else:
			while not TheEndOfTime:
				try:
					sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					sock.sendto(randomword(packetSize), (ipaddr, port))
				except Exception, e:
					if debug:
						print 'UDP'
						print e
				delay()


#translates a service name into an object
serviceDict = {
	'telnet':telnet(), #done? like it should be working but again, no telnet setup...
	'http':http(), #done
	'https':https(), #done
	'http-proxy':httpProxy(), #done
	'ftp':ftp(), #in progress needs more testing
	'sftp':sftp(), #done needs more testing (srsly, like i don't have an sftp server...)
	'tftp':tftp(), #should be done
	'dhcp':dhcp(), #done needs more testing
	'ssh':ssh(), 
	'pop3':pop(), #works?
	'imap':imap(), #done(?)
	'smtp':smtp(), #done(?)
	'dns':dns(), #done it is generating traffic (i think... kinda hard to tell tbh...) but needs more testing
	'smb':smb(),
	'daytime':daytime()
	#generic done just opens a socket(TCP/UDP dependent on the nmap results) and send random ASCII data to the service
}

class host(object):
	"""
	represents a host
	ipaddr: the ip address of the host
	port: the port number of the service"""
	def __init__(self, host):
		self.host = host
		self.address = self.host.address
		self.serviceThreads = []
		print host.get_open_ports()
		print host.hostnames
		
	def startTraffic(self):
		
		for serv in self.host.services:
			temp = None
			if atemptFilteredAndClosedConnections or 'filtered' not in serv.state and 'closed' not in serv.state:
				temp = serviceDict.get(serv.service, None)
				if temp != None:
					self.serviceThreads.append(temp.run(self.address, serv.port))
				else:
					temp = generaric() 
					self.serviceThreads.append(temp.run(self.address, serv.port, serv.protocol))


def localControll():
	global TheEndOfTime
	TheEndOfTime = False
	try:
		report = NmapParser.parse_fromfile(inputFile)
		hostlist = [host(node) for node in report.hosts]
		for targetHost in hostlist:
			targetHost.startTraffic()
	except Exception, e:
		if debug:
			print e
	try:
		while not TheEndOfTime:
			selection = raw_input("Remaining Threads: " + str(threading.activeCount()) + "\n0.) Exit\n->")
			if selection == 0:
				TheEndOfTime = True
				while threading.activeCount() > 10:
					if debug:
						print 'Threads remaining: ' +  str(threading.activeCount()) + ': ' + str(threading.enumerate())
					else:
						print 'Threads remaining: ' +  str(threading.activeCount())
					time.sleep(10)
				sys.exit()
	except KeyboardInterrupt:
		print '\033cworking, things should close out eventualy...\n may get stuck on the last coupple threads depending on what you have running'
		TheEndOfTime = True
		while threading.activeCount() > 10:
			if debug:
				print 'Threads remaining: ' +  str(threading.activeCount()) + ': ' + str(threading.enumerate())
			else:
				print 'Threads remaining: ' +  str(threading.activeCount())
			time.sleep(10)
		sys.exit()

def remoteControll():
	global TheEndOfTime
	TheEndOfTime = False
	nmapXml = ''

	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('', listenPort))
		serversocket.listen(4)
		conn, remoteAddr = serversocket.accept()
		recvBuffer = str(conn.recv(1024))
		while recvBuffer:
			nmapXml += recvBuffer
			recvBuffer = str(conn.recv(1024))
	except Exception, e:
		if debug:
			raise e
	try:
		report = NmapParser.parse(nmapXml)
		hostlist = [host(node) for node in report.hosts]
		for targetHost in hostlist:
			targetHost.startTraffic()
	except Exception, e:
		if debug:
			print e
	try:
		while not TheEndOfTime:
			time.sleep(500);
	except KeyboardInterrupt:
		print '\033cworking, things should close out eventualy...\n may get stuck on the last coupple threads depending on what you have running'
		TheEndOfTime = True
		while threading.activeCount() > 5:
			if debug:
				print 'Threads remaining: ' +  str(threading.activeCount()) + ': ' + str(threading.enumerate())
			else:
				print 'Threads remaining: ' +  str(threading.activeCount())
			time.sleep(10)
		sys.exit()

def main():
	if underRemoteControll:
		remoteControll()
	else:
		localControll()

if __name__ == '__main__':
	main()
