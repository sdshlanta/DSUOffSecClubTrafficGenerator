# .___.__  ._______.______  ._______     ._______ ._______     .______  .______  .______  ._____  ._______  .______  .________
# :   |  \ : .____/: __   \ : .____/     : __   / : .____/     :_ _   \ : __   \ :      \ :_ ___\ : .___  \ :      \ |    ___/
# |   :   || : _/\ |  \____|| : _/\      |  |>  \ | : _/\      |   |   ||  \____||   .   ||   |___| :   |  ||       ||___    \
# |   .   ||   /  \|   :  \ |   /  \     |  |>   \|   /  \     | . |   ||   :  \ |   :   ||   /  ||     :  ||   |   ||       /
# |___|   ||_.: __/|   |___\|_.: __/     |_______/|_.: __/     |. ____/ |   |___\|___|   ||. __  | \_. ___/ |___|   ||__:___/ 
#     |___|   :/   |___|       :/                    :/         :/      |___|        |___| :/ |. |   :/         |___|   :     
#                                                               :                          :   :/    :                        
#                                                                                              :                              

#you have been warned
                                                                                                                        
#network
import socket #generic+daytime
from ftplib import FTP #ftp
import requests #http, https, http-proxy
import pysftp #sftp
import telnetlib #telnet
import paramiko, base64 #ssh
import tftpy #tftp
import smtplib, imaplib, poplib #for smtp imap and pop3, basicly all email
from pydhcplib.dhcp_packet import * #dhcp
from pydhcplib.dhcp_network import * #dhcp
from smb.SMBConnection import SMBConnection
import dns.resolver as dnsResolver # for DNS
#util
from email.mime.text import MIMEText
import email.utils
import random
import threading
import warnings
from noisyCricketUtil import *

class telnet(ncThread): #ncThread is defined in noisyCricketUtil
	"""docstring for telnet"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try: #start non-boilerplate
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
				except Exception, e : #end non-boilerplae
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class ftp(ncThread):
	"""docstring for ftp"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:
					ftpClient = FTP()
					ftpClient.connect(ipaddr, port)
					ftpClient.login() #anon login
					ftpClient.retrlines('list') #do a thing
					ftpClient.quit() #gtfo
				except Exception, e:
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class sftp(ncThread):
	"""docstring for sftp"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					connection = pysftp.Connection(ipaddr, port, username='notABruteForce'+randomword(), password='seriouslyThisIsLegit' + randomword())
					connection.close()
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)
		connection = pysftp.Connection(ipaddr, port, username='notABruteForce'+randomword(), password='seriouslyThisIsLegit' + randomword())
		connection.close()

class tftp(ncThread):
	"""docstring for tftp"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					client = tftpy.TftpClient(ipaddr, port)
					tftpFileName = 'tftp.tmp'
					fp = file(tftpFileName, 'w')
					fp.write(randomword(256))
					client.upload(tftpFileName, tftpFileName)
					client.download('exists', 'downloaded.dat')
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class http(ncThread):
	"""docstring for http"""
	def open(self, ipaddr, port=80): 
		self.depth = 0
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				#because I was sick of the SSL errors that kept popping up.
				with warnings.catch_warnings():
					warnings.simplefilter('ignore')
					try:
						delay(self.hostState.delayFactor)
						#fun fact the code between the ------ marks is a spider(however it has been gimped to make sure that it doesn't spider the site too much)
						#------
						self.depth = 0
						url = 'http://' + str(ipaddr)
						r=requests.get(url, verify=False)
						while True:
							links = get_urls_from_response(r)
							if len(links) == 0 or self.depth <= random.randint(0,10): #to make it spider everything 
								break
							r= requests.get(random.choice(set(links)))
							delay(self.hostState.delayFactor, 2)
							self.depth += 1
						#------
					except Exception, e:
						if self.hostState.debug:
							print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
						
				delay(self.hostState.delayFactor)

class https(ncThread):
	def open(self, ipaddr, port):
		self.depth = 0
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				with warnings.catch_warnings():
					warnings.simplefilter('ignore')
					try:
						self.depth = 0
						url = 'https://' + str(ipaddr)
						r=requests.get(url, verify=False)

						while True:
							links = get_urls_from_response(r)
							if len(links) == 0 or self.depth <= random.randint(0,10):
								break
							url = random.choice(set(links))
							r= requests.get(url, verify=False)
							delay(2)
							self.depth += 1
					except Exception, e:
						if self.hostState.debug:
							print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
						
				delay(self.hostState.delayFactor)

class httpProxy(ncThread):
	def open(self, ipaddr, port):
		self.depth = 0
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				with warnings.catch_warnings():
					warnings.simplefilter('ignore')
					try:#start non-boilerplate
						self.depth = 0
						url = 'http://' + str(ipaddr)
						try:
							r=requests.get(url)
						except Exception, e:
							if debug:
								print 'http-proxy'
								print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
							try:
								url = 'https://' + str(ipaddr)
								r=requests.get(url, verify=False)
							except Exception, e:
								if debug:
									print 'http-proxy'
								
							while True:
								links = get_urls_from_response(r)
								if len(links) == 0 or self.depth <= random.randint(0,10):
									break
								r = requests.get(random.choice(set(links)))
								delay(2)
					except Exception, e:#end non-boilerpla
						if self.hostState.debug:
							print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
						
		delay(self.hostState.delayFactor)


class ssh(ncThread):
	"""docstring for ssh"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					sshC = paramiko.SSHClient()
					sshC.set_missing_host_key_policy(paramiko.AutoAddPolicy())
					sshC.connect(hostname=ipaddr, port=port, username=randomword(), password=randomword(8))
					stdin, stdout, stderr = ssh.exec_command('ls')
					ssh.close()
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)
		
class pop3(ncThread):
	"""docstring for pop3"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					M = poplib.POP3(ipaddr, port)
					M.user("le" + randomword(2).lower() + "gi" + randomword(2).lower() + "tU" + randomword(2).lower() + "se" + "r" + "\n")
					M.pass_(randomword(6))
					numMessages = len(M.list()[1])
					for i in range(numMessages):
						for j in M.retr(i+1)[1]:
							pass
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

				
class smtp(object):
	"""docstring for smtp"""
	def __init__(self):
		super(smtp, self).__init__()
		self.msg = MIMEText('This is the body of the message.')
		self.msg['To'] = email.utils.formataddr(('Recipient', 'recipient@example.com'))
		self.msg['From'] = email.utils.formataddr(('Author', 'author@example.com'))
		self.msg['Subject'] = 'Simple test message'
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					server = smtplib.SMTP(ipaddr, port)
					server.sendmail('author@example.com', ['recipient@example.com'], self.msg.as_string())
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)
		

class imap(object):
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					M = imaplib.IMAP4(ipaddr, port)
					M.login(getpass.getuser(), getpass.getpass())
					M.select()
					typ, data = M.search(None, 'ALL')
					#for num in data[0].split():
					#	typ, data = M.fetch(num, '(RFC822)')
					typ, data = map(lambda x: M.fetch(x, '(RFC822)'), data[0].split())
					M.logout()
					M.close()
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class dns(ncThread):
	"""docstring for dns"""
	def run(self, ipaddr='8.8.8.8', port=22):
		self.resolver = dnsResolver.Resolver()
		self.resolver.nameservers = [str(ipaddr)] #specify the ip address of the nameserver
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t	
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					answers = dns.resolver.query( randomword() + "." + randomword() + ".com", dns.rdtypes.ANY)
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class dhcp(ncThread):
	"""docstring for dhcp"""
	def run(self, ipaddr='255.255.255.255', port=67):
		self.netopt = {'client_listen_port':68,
					   'server_listen_port':port,
					   'listen_address':str(ipaddr)}
		self.client = Client(self.netopt)
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t

	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					self.client.BindToAddress()
					self.client.GetNextDhcpPacket()
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class smb(object):
	"""docstring for smb"""
	def __init__(self):
		super(smb, self).__init__()
	def run(self, ipaddr, port=22):
		t = threading.Thread(target=self.open, args=(ipaddr, port))
		t.start()
		return t
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate
					conn = SMBConnection(randomword(), randomword(), randomword(), ipaddr, use_ntlm_v2 = True)
				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class daytime(ncThread):
	"""docstring for daytime"""
	def open(self, ipaddr, port):
		print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.connect((ipaddr,port))
					while True:
						data = s.recv(10000)
						if data:
							pass
						else:
							break
					s.close()
				except Exception, e:
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)

class generic(ncThread):
	"""docstring for generic"""
	def run(self, ipaddr, port, protocol, packetSize=64):
		t = threading.Thread(target=self.open, args=(ipaddr, port, protocol, packetSize))
		t.start()
		return t
	#weird eough case not to get boiler plate
	def open(self, ipaddr, port, protocol, packetSize):
		#print '*'
		print 'protocol ' + str(protocol)
		if protocol == 'tcp':
			while self.hostState.running:
				if not self.hostState.paused:
					try:
						sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						sock.connect((ipaddr,port))
						sock.send(randomword(packetSize))
						sock.close()
					except Exception, e:
						sock.close()
						sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						if self.hostState.debug:
							print('%s, %s: %s' % (ipaddr, 'TCP', e))
				delay(self.hostState.delayFactor)
		elif protocol == 'udp':
			while self.hostState.running:
				if not self.hostState.paused:
					try:
						sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
						sock.sendto(randomword(packetSize), (ipaddr, port))
					except Exception, e:
						if self.hostState.debug:
							print 'UDP'
							print('%s, %s: %s' % (ipaddr, 'UDP', e))
				delay(self.hostState.delayFactor)

#translates a service name into an object
serviceDict = {

	'telnet':telnet, #done? like it should be working but again, no telnet setup...
	'http':http, #done
	'https':https, #done
	'http-proxy':httpProxy, #done
	'ftp':ftp, #in progress needs more testing
	'sftp':sftp, #done needs more testing (srsly, like i don't have an sftp server...)
	'tftp':tftp, #should be done
	'dhcp':dhcp, #done needs more testing
	'ssh':ssh, #done
	'pop3':pop3, #works?
	'smtp':smtp, #done(?)
	'imap':imap, #done(?)
	'dns':dns, #done it is generating traffic (i think... kinda hard to tell tbh...) but needs more testing
	'smb':smb, 
	'daytime':daytime, #done
	'generic':generic #done
}

#just Ignore this only here because I'm lazy -_-
"""
print(self.__class__.__name__)
		while self.hostState.running:
			if self.hostState.paused:
				if self.hostState.debug:
					print('%s %s paused' % (ipaddr, self.__class__.__name__))
				delay(self.hostState.delayFactor)
			else:
				try:#start non-boilerplate

				except Exception, e:#end non-boilerpla
					if self.hostState.debug:
						print('%s, %s: %s' % (ipaddr, self.__class__.__name__, e))
					
			delay(self.hostState.delayFactor)
"""
