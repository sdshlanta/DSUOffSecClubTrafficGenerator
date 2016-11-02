#!/usr/bin/python

#Python traffic generator by YoNotHim

#takes the xml output of an nmap scan filename is set with input file.
#trys to connect to any common network services it is given by the nmap report
#may add support for masscan at some point but mehs


import argparse
parser = argparse.ArgumentParser(description='Creates "cover traffic" for red teams during capture the flag events events')
parser.add_argument('-f', type=str, default='nmap.xml', help="The name the file containing XML output from nmap, uses nmap.xml by default")
parser.add_argument('-D', action='store_true', default=False, help="Enables debugging output")
parser.add_argument('-d', type=int, default=10, help="Sets the value for the highest posable delay between the sending of packets")
parser.add_argument('-c', action='store_true', default=False, help='Force the program to atempt to connect to filtered and closed connections')

<<<<<<< HEAD
args = parser.parse_args()
=======
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
>>>>>>> origin/master

from flask import Flask, render_template, request, session, escape, redirect, url_for, abort
from libnmap.parser import NmapParser #for parsing nmap for generating the host list
import threading
from services import *
from noisyCricketUtil import HostState
import threading
from multiprocessing import Process
import socket



app = Flask(__name__)
hosts = {}
@app.route('/', methods=['GET'])
def home():
	error = None
	return render_template('index.html', error=error, context={'hosts':hosts})

@app.route('/api/pauseHost', methods=['GET'])
def pauseHost():
	error = None
	try:
		ipaddr = escape(str(request.args.get('ipaddr')))
		hosts[ipaddr].pauseTraffic()
		return redirect(url_for('home'))
	except Exception as e:
		raise e

@app.route('/api/resumeHost', methods=['GET'])
def resumeHost():
	error = None
	try:
		ipaddr = escape(str(request.args.get('ipaddr')))
		hosts[ipaddr].resumeTraffic()
		return redirect(url_for('home'))
	except Exception as e:
		raise e

@app.route('/api/pauseAll', methods=['GET'])
def pauseAll():
	for targetHost in hosts.itervalues():
		targetHost.pauseTraffic()
	return redirect(url_for('home'))

@app.route('/api/resumeAll', methods=['GET'])
def resumeAll():
	for targetHost in hosts.itervalues():
		targetHost.resumeTraffic()
	return redirect(url_for('home'))


def main():
	try:
		localhost = socket.gethostbyname(socket.gethostname())
		report = NmapParser.parse_fromfile(args.f)
		for node in report.hosts:
				if node.address != localhost:
					hosts[node.address] = host(host=node, serviceDict=serviceDict, tryFandCConn=args.c, delayFactor=args.d, debug=args.D)
		for targetHost in hosts.itervalues():
			targetHost.startTraffic()
		app.secret_key = 'Th1S1s@v3ry53cUr3K3y~XHH!jmN'
		app.run(port=8080, host="0.0.0.0", debug=False)
		#course local controll falback
		while True:
			inp = raw_input(str(threading.activeCount()) + " > ").strip()
			if inp == "1":
				for targetHost in hosts.itervalues():
					targetHost.pauseTraffic()
			elif inp == "2":
				for targetHost in hosts.itervalues():
					targetHost.resumeTraffic()
			elif inp == "3":
				justFuckingDie()

	except KeyboardInterrupt as e:
		justFuckingDie()
if __name__ == '__main__':
	main()
