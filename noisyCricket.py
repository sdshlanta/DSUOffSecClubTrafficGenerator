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

args = parser.parse_args()

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
