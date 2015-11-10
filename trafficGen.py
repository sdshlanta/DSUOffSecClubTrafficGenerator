#Python traffic generator by YoNotHim
 
#takes the xml output of an nmap scan filename is set with input file.
#trys to connect to any common network services it is given by the nmap report
#makes a looooot of threads so if that is a problem for you keep that in mind
#may add support for masscan at some point but mehs


from libnmap.parser import NmapParser #for parsing nmap for generating the host list
from datetime import datetime
from bs4 import BeautifulSoup # for parsing the receved html for the spider because im lazy
from pydhcplib.dhcp_packet import * # for DHCP
from pydhcplib.dhcp_network import * # for DHCP
from ftplib import FTP #for FTP
from email.mime.text import MIMEText
#import json #for parsing mascan use the -oJ <filename> to generate the output file
import socket #for generic requests
import telnetlib #telnet
import paramiko, base64 #SSH
import requests #for HTTP
import smtplib, imaplib, poplib #for SMTP IMAP and POP3, basicly all email
import tftpy #for TFTP
import dns.resolver as dnsResolver # for DNS
import pysftp # for SFTP
import argparse
import threading
import random, string
import time
import email.utils

inputFile = "test.xml"
debug = True
delayFactor = 1024 #the value time is modded by
hostlist = []
maxLinksFollowed = 3 
TheEndOfTime = False


def get_urls_from_response(r):
	soup = BeautifulSoup(r.text, 'html.parser')
	urls = [link.get('href') for link in soup.find_all('a')]
	return urls

def print_url(args):
	print args['url']

def randomword(length=6):
	return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def rand():
	return int(random.SystemRandom().random()*1000000000000000000) #just making it an int ignore the magic number

def delay(addtionalDelay=0):
	time.sleep((rand()%delayFactor)+addtionalDelay)

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
		self.arguments = (port, ipaddr)
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		while not TheEndOfTime:
			try:
				tn = telnetlib.Telnet(ipaddr, port)

				tn.read_until("login: ")
				tn.write("le" + randomword(2).lower() + "gi" + randomword(2).lower() + "tU" + randomword(2).lower() + "se" + "r" + "\n") #type some random junk for the username
				if password:
					tn.read_until("Password: ")
					tn.write(randomword() + "DontBanPlx\n") #type some random junk for the password

				#these should never ever ever execute but if the do it does an ls and exits
				tn.write("ls\n")
				delay(-1)
				tn.write("exit\n")
				delay(-1)
			except Exception, e:
				if debug:
					print e
			delay()


class ftp(object):
	"""docstring for ftp"""
	def __init__(self):
		super(ftp, self).__init__()
	def run(self, ipaddr, port=21):
		t = threading.Thread(target=self.open, args=(port, ipaddr))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		while not TheEndOfTime:
			try:
				ftpClient = FTP()
				ftpClient.connect(ipaddr, port)
				ftpClient.login() #anon login
				ftpClient.retrlines('list') #do a thing
				ftp.quit() #gtfo
			except Exception, e:
				if debug:
					print e
			delay()

class sftp(object):
	"""docstring for sftp"""
	def __init__(self):
		super(sftp, self).__init__()
	def run(self, ipaddr, port=115):
		t = threading.Thread(target=self.open, args=(port, ipaddr))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):

		while not TheEndOfTime:
			try:
				connection = pysftp.Connection(ipaddr, port, username='notABruteForce'+randomword(), password='seriouslyThisIsLegit' + randomword())
				connection.close()
			except Exception, e:
				if debug:
					print e
			delay()
		
class tftp(object):
	"""docstring for tftp"""
	def __init__(self):
		super(tftp, self).__init__()
	def run(self, ipaddr, port=69):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		print "tftp"
		while not TheEndOfTime:
			try:
				client = tftpy.TftpClient(ipaddr, port)
				tftpFileName = 'tftp.tmp'
				fp = file(tftpFileName, 'w')
				fp.write(randomword(256))
				client.upload(tftpFileName, tftpFileName)
				client.download('exists', 'downloaded.dat')
			except Exception, e:
				if debug:
					raise e
			delay()
						
class http(object):
	"""docstring for http"""
	def __init__(self):
		super(http, self).__init__()
		self.depth = 0
	def run(self, ipaddr, port=80):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(False)
		t.start()
		return t	

	def open(self, ipaddr, port): #this also spiders the site
		print 'http'
		while not TheEndOfTime:
			try:
				url = 'http://' + str(ipaddr)
				r=requests.get(url, verify=False)

				while True:
					links = get_urls_from_response(r)
					if len(links) == 0 or self.depth <= maxLinksFollowed:
						break
					r= requests.get(random.choice(set(links)))
					delay(2)
					self.depth += 1
			except Exception, e:
				if debug:
					print str(ipaddr) + ':' + str(port)
					print e
			delay()

class https(object):
	"""docstring for https"""
	def __init__(self):
		super(https, self).__init__()
		self.depth = 0
	def run(self, ipaddr, port=443):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		print 'https'
		while not TheEndOfTime:
			try:
				url = 'https://' + str(ipaddr)
				r=requests.get(url, verify=True)

				while True:
					links = get_urls_from_response(r)
					if len(links) == 0 or self.depth <= maxLinksFollowed:
						break
					r= requests.get(random.choice(set(links)))
					delay(2)
					self.depth += 1
			except Exception, e:
				if debug:
					print str(ipaddr) + ':' + str(port)
					print e
			delay()

class httpProxy(object):
	"""docstring for httpProxy"""
	def __init__(self):
		super(httpProxy, self).__init__()
	def run(self, ipaddr, port):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(False)
		t.start()
		return t
	def open(self, ipaddr, port):
		print 'http-proxy: ' + str(port)
		while not TheEndOfTime:
			
			url = 'http://' + str(ipaddr)
			try:
				r=requests.get(url)
			except Exception, e:
				try:
					url = 'https://' + str(ipaddr)
					r=requests.get(url, verify=True)
				except Exception, e:
					if debug:
						raise e
			try:		
				while True:
					links = get_urls_from_response(r)
					if len(links) == 0 or self.depth <= maxLinksFollowed:
						break
					r= requests.get(random.choice(set(links)))
					delay(2)
					self.depth += 1
			except Exception, e:
				if debug:
					print str(ipaddr) + ':' + str(port)
					print e
			delay()

class ssh(object):
	"""docstring for ssh"""
	def __init__(self):
		super(ssh, self).__init__()
	def run(self, ipaddr, port=22):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		print "ssh"

class pop(object):
	"""docstring for pop3"""
	def __init__(self):
		super(pop, self).__init__()
	def run(self, ipaddr, port=110):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		print "pop3"
		while not TheEndOfTime:
			M = poplib.POP3(ipaddr, port)
			M.user("le" + randomword(2).lower() + "gi" + randomword(2).lower() + "tU" + randomword(2).lower() + "se" + "r" + "\n")
			M.pass_(randomword(6))
			numMessages = len(M.list()[1])
			for i in range(numMessages):
				for j in M.retr(i+1)[1]:
					pass
			delay()

class smtp(object):
	"""docstring for smtp"""
	def __init__(self):
		super(smtp, self).__init__()
	def run(self, ipaddr, port=25): #smtp runs on port 25
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		print "smtp"
		msg = MIMEText('This is the body of the message.')
		msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
		msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
		msg['Subject'] = 'Simple test message'
		while not TheEndOfTime:
			try:
				server = smtplib.SMTP(ipaddr, port)
				server.sendmail('author@example.com', ['recipient@example.com'], msg.as_string())
			except Exception, e:
				if debug:
					raise e
			delay()

class imap(object):
	"""docstring for imap"""
	def __init__(self):
		super(imap, self).__init__()
	def run(self, ipaddr, port=143):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		while not TheEndOfTime:
			try:
				M = imaplib.IMAP4(ipaddr, port)
				M.login(getpass.getuser(), getpass.getpass())
				M.select()
				typ, data = M.search(None, 'ALL')
				for num in data[0].split():
				    typ, data = M.fetch(num, '(RFC822)')
				    print 'Message %s\n%s\n' % (num, data[0][1])
				M.close()
				M.logout()
			except Exception, e:
				if debug:
					raise e

class dhcp(object):
	"""docstring for dhcp"""
	def __init__(self):
		super(dhcp, self).__init__()
	def run(self, ipaddr='0.0.0.0', port=67):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		print "dhcp"
		self.netopt = {'client_listen_port':68,
					   'server_listen_port':port,
					   'listen_address':str(ipaddr)}
		self.client = Client(self.netopt)
		try:
			self.client.BindToAddress()
		except Exception, e:
			raise e
			while not TheEndOfTime:
				try:
					self.client.GetNextDhcpPacket()
				except Exception, e:
					if debug:
						raise e
				delay()

class dns(object):
	"""docstring for dns"""
	def __init__(self):
		super(dns, self).__init__()
	def run(self, ipaddr='8.8.8.8', port=22):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port):
		resolver = dnsResolver.Resolver()
		resolver.nameservers = [str(ipaddr)] #specify the ip address of the nameserver
		while not TheEndOfTime:
			answers = dns.resolver.query( randomword() + "." + randomword() + ".com", dns.rdtypes.ANY)
			delay()

class generaric(object):
	"""docstring for generaric"""
	def __init__(self):
		super(generaric, self).__init__()
	def run(self, ipaddr, port, protocol):
		t = threading.Thread(target=self.open, args=(ipaddr,port,protocol))
		t.setDaemon(True)
		t.start()
		return t
	def open(self, ipaddr, port, protocol):
		print '*'
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
	'imap':imap(), 
	'smtp':smtp(),
	'dns':dns() #done it is generating traffic (i think... kinda hard to tell tbh...) but needs more testing
	#generic needs to be done which should just open a socket(TCP/UDP dependent on the nmap results) and send random ASCII data to the service
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
			temp = serviceDict.get(serv.service, None)
			#if str(temp) == 'hurp':
			if temp != None:
				self.serviceThreads.append(temp.run(self.address, serv.port))
			else:
				temp = generaric() 
				self.serviceThreads.append(temp.run(self.address, serv.port, serv.protocol))
	def getServiceThreads(self):
		return self.serviceThreads


def main():
	hostlist = []
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
			delay(9999)
	except KeyboardInterrupt:
		print 'working, things should close out in the worst case after there last command plus whatever delay you have set up'
		TheEndOfTime = True
#		for hostlet in hostlist:
#			for service in hostlet.getServiceThreads():
#				service.join()
#				print 'close'
if __name__ == '__main__':
	main()