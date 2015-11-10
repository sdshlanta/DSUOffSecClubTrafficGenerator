import smtplib
import imaplib
import time
import threading
import sys
import argparse
import csv
import random
import string
import email
import re
import math
import pickle


keys = []

class autoSave(object):
	"""docstring for autoSave"""
	def __init__(self):
		super(autoSave, self).__init__()
	def run(self):
		t = threading.Thread(target=self.save)
		t.setDaemon(True)
		t.start()
		return t
	def save(self):
		while 1:
			try:
				fp=open("backup.dat", 'wb')
				pickle.dump(playerManager,fp)
			except Exception, e:
				print "Auto-save failed."
			time.sleep(60)


#finished
class menu(object):
	"""docstring for menu"""
	def __init__(self, game,messenger):
		super(menu, self).__init__()
		self.game=game
		self.messenger=messenger
		saver = autoSave()
		saver.run()
		try:
			while 1:
				selection = raw_input("\033c\nMain menu:\n1.) Make a player a zombie\n2.) Make a player human\n3.) Change PZ\n4.) Get a list of players.\n5.) Get a list of zombies.\n6.) Get a list of humans.\n7.) Fetch pID from a name\n8.) Send out a mission.\n9.) Perform a manual backup\n0.) End game (there will be a conformation dialogue).\n-> ")
				selection = selection.rstrip()
				if selection == '1':
					self.setAllegiance(True, 'Zombie')
				elif selection == '2':
					self.setAllegiance(False, 'Human')
				elif selection == '3':
					self.setPZ()
				elif selection == '4':
					self.playerList()
				elif selection == '5':
					self.zombieList()
				elif selection == '6':
					self.humanList()
				elif selection == '7':
					self.getpIDFromName()
				elif selection == '8':
					self.mission()
				elif selection == '9':
					self.manualBackup()
				elif selection == '0':
					self.endGame()
				else:
					print "Invalid choice: \"%s\"\n<---Press Enter to continue--->" % selection
					raw_input()

						
		except Exception, e:
			pass
		
	
	def setAllegiance(self, side, usrHlp):
		print "\033cSet Allegiance: %s\n%s" % (usrHlp, args.f)
		self.pID = raw_input("pID-> ")
		self.pID = self.pID.rstrip()
		if self.pID in set(keys):
			playerManager.pDict[self.pID].zombie = side
		elif self.pID == "exit":
			raw_input("No allegiances have been changed\n<---Press Enter to continue--->")
		else:
			self.setAllegiance(side, usrHlp + ": Incorrect pID")

	def setPZ(self):
		print "\033cSet PZ:"
		self.selection = raw_input("Would you like to keep the current PZ(s)? (Y/N)\n-> ")
		thingSet = False
		if self.selection.lower() == 'y':
			self.selection = raw_input("\033cSet PZ:\npID-> ")
			while not thingSet:
				if self.selection.rstrip() in set(keys):
					playerManager.pDict[self.selection].PZero = True
					thingSet = True
				elif self.selection.rstrip() == 'exit':
					thingSet = True
					raw_input("Old PZ(s) kept\n<---Press Enter to continue--->")
				else:
					self.selection = raw_input("pID not found.\npID-> ")
		elif self.selection.lower() == 'n':
			self.selection = raw_input("\033cSet PZ:\npID-> ")
			while not thingSet:
				if self.selection.rstrip() in set(keys):
					for key in keys:
						if playerManager.pDict[key].PZero:
							playerManager.pDict[key].PZero = False
					playerManager.pDict[self.selection].PZero = True
					thingSet = True
				elif self.selection.rstrip() == 'exit':
					thingSet = True
					raw_input("Old PZ(s) kept\n<---Press Enter to continue--->")
				else:
					self.selection = raw_input("pID not found.\npID-> ")
		elif self.selection.rstrip() == 'exit':
			return
		else:
			raw_input("Invalid choice.\n<---Press Enter to continue--->")
	
	def playerList(self):
		print "\033cList of players:\nName\t\t| pID\t| Zombie | Kills | Is PZ"
		for key in keys:
			if playerManager.pDict[key].PZero:
				print "%s\t| %s | %s\t | %s\t | %s" % (playerManager.pDict[key].name,key,playerManager.pDict[key].zombie,playerManager.pDict[key].kills,playerManager.pDict[key].PZero)
			else:
				print "%s\t| %s | %s\t | %s\t |" % (playerManager.pDict[key].name,key,playerManager.pDict[key].zombie, playerManager.pDict[key].kills)
		raw_input("<---Press Enter to continue--->")
	
	def humanList(self):
		print "\033cList of humans:\nName\t\t| pID\t| Is PZ"
		for key in keys:
			if not playerManager.pDict[key].zombie and playerManager.pDict[key].PZero:
				print "%s\t| %s\t| %s" % (playerManager.pDict[key].name,key,playerManager.pDict[key].PZero)
			elif not playerManager.pDict[key].zombie:
				print "%s\t| %s\t|" % (playerManager.pDict[key].name,key)
		raw_input("<---Press Enter to continue--->")

	def zombieList(self):
		print "\033cList of zombies:\nName\t\t| pID\t| Kills\t| Was PZ"
		for key in keys:
			if playerManager.pDict[key].zombie and playerManager.pDict[key].PZero:
				print "%s\t| %s\t| %s\t| %s" % (playerManager.pDict[key].name,key,playerManager.pDict[key].kills,playerManager.pDict[key].PZero)
			elif playerManager.pDict[key].zombie:
				print "%s\t| %s\t| %s\t|" % (playerManager.pDict[key].name,key,playerManager.pDict[key].kills)
		raw_input("<---Press Enter to continue--->")

	def getpIDFromName(self):
		name = raw_input("\033cName to pID:\nEnter name: -> ")
		print "Name\t\t| pID\t| Is PZ"
		for key in keys:
			if name.lower() in playerManager.pDict[key].name.lower():
				if playerManager.pDict[key].PZero:
					print "%s\t| %s\t| %s" % (playerManager.pDict[key].name,key,playerManager.pDict[key].PZero)
				else:
					print "%s\t| %s\t|" % (playerManager.pDict[key].name,key)
		raw_input("<---Press Enter to continue--->")

	def mission(self):
		self.unsuccessful = True
		self.msg = ""

		self.path = raw_input("\033cMission Creation dialogue: Humans\nPlease enter the full path the the text file containing the human mission text.\n(example: C:\\Users\\Jon\\ Doe\\Documents\\HvZ\\humanMission.txt)\n-> ")
		while self.unsuccessful:
			try:
				if self.path.rstrip() == 'exit':
					return
				self.fp = open(self.path.rstrip(), 'r')
				self.msg = self.fp.read()
				self.unsuccessful = False
			except Exception, e:
				self.path = raw_input("\033cMission Creation dialogue: Human\nPlease enter the full path the the text file containing the human mission text.\n(example: C:\\Users\\Jon Doe\\Documents\\HvZ\\humanMission.txt)\nFILE DOES NOT EXIST.\n-> ")
		print "\nMessaging humans..."
		print self.messenger.emailHumans(self.msg)
		self.messenger.emailHumans(self.msg)
		self.messenger.sendHumans("Humans, new mission!\nCheck email your for details.")
		
		self.path = raw_input("\033cMission Creation dialogue: Zombies\nPlease enter the full path the the text file containing the zombie mission text.\n(example: C:\\Users\\Jon\\ Doe\\Documents\\HvZ\\humanMission.txt)\n-> ")
		while self.unsuccessful:
			try:
				if self.path.rstrip() == 'exit':
					return
				self.fp = open(self.path.rstrip, 'r')
				self.msg = self.fp.read()
				self.unsuccessful = False
			except Exception, e:
				self.path = raw_input("\033cMission Creation dialogue: Zombies\nPlease enter the full path the the text file containing the zombie mission text.\n(example: C:\\Users\\Jon Doe\\Documents\\HvZ\\humanMission.txt)\nFILE DOES NOT EXIST.\n-> ")
				self.unsuccessful = True
		print "\nMessaging zombies"
		self.messenger.emailZombies(self.msg)
		self.messenger.sendPIDs(keys, "Players, new mission!\nCheck your email for details.")

	def manualBackup(self):
		try:
			fp=open("backup.dat", 'wb')
			pickle.dump(playerManager,fp)
			raw_input("Backup successful!\n<---Press Enter to continue--->")

		except Exception, e:
			raw_input("Backup UNsuccessful!\n<---Press Enter to continue--->")
		

	def endGame(self):
		print "\033c"
		sel = raw_input("To exit type the following sentence\n\'The quick brown fox jumps over the lazy dog.'\n(WARNING: This WILL end the game and you WILL lose all unsaved data.)\n-> ")
		if sel.rstrip().lower() == 'the quick brown fox jumps over the lazy dog.':
			sys.exit()


class gameLogic(object):
	"""docstring for gameLogic"""
	def __init__(self, playerManager, mailMan, messenger):
		super(gameLogic, self).__init__()
		self.mailMan = mailMan
		self.messenger = messenger
		self.unknownCommand = "UnknownCommand: "

	def run(self):
		t = threading.Thread(target=self.logic)
		t.setDaemon(True)
		t.start()
		return t

	def logic(self):
		while 1:
			dif=0
			self.unreadMail = self.mailMan.getUnread()
			if self.unreadMail != None:
				try:
					for self.mail in self.unreadMail:
						processedMessage = re.split('tagged *', self.mail[1], flags=re.I)
						if processedMessage[0] != self.mail[1]:
							if playerManager.makeZombie( str(processedMessage[1][:5]) ) == False:
								self.messenger.sendSingle(self.mail[0], "\nPlayer doesn't exist, double check pID")
							else:
								for key in keys:
									if self.mail[0] == playerManager.pDict[key].number:
										self.messenger.sendSingle(self.mail[0], "\nTag confirmed.")
										playerManager.pDict[key].kills+=1
										playerManager.pDict[str(processedMessage[1][:5])].activeCooldown = time.time()

						else:
							processedMessage = re.split('help *', self.mail[1], flags=re.I)
							if len(processedMessage) > 1:
								if re.match('mission|tcb|kennedy center|science center|lowry|east|lowry hall|libary|kennedy|tunheim classroom buliding|beadle', processedMessage[1], flags=re.I)!=None:
									if processedMessage[0] != self.mail[1]:
										for key in keys:
											if self.mail[0] == playerManager.pDict[key].number:
												dif = time.time() - playerManager.pDict[key].activeCooldown
									
										if dif >3599:
											helpers = []
											count = 0
											watchdog = 0
											maxHelpers = range(int(math.ceil(float(len(keys))/float(3))))
											#gets the people who will help the player.

											while count <= maxHelpers and watchdog <=len(keys)*2:
												candidate = random.choice(keys)
												#print candidate
												if playerManager.pDict[candidate].number != self.mail[0]:
													if not playerManager.pDict[candidate].zombie:
														if candidate not in set(helpers):
															helpers.append(candidate)
															#print "helpers: %s" % helpers
															count += 1
												watchdog += 1
											msg = "\nSomeone nees help at " + processedMessage[1]
											self.messenger.sendPIDs(helpers, msg)
											self.messenger.sendSingle(self.mail[0], "\nRequest for help receved and forwarded")

											#sets the cooldown
											playerManager.pDict[key].activeCooldown = time.time()
										else:
											self.messenger.sendSingle(self.mail[0], "\nYour ablity to call for help is on cooldown.\nCooldown lasts for one hour after you used it. ")
									else:
										self.messenger.sendSingle(self.mail[0],"\n")
							
							else:
								key = ""
								for key in keys:
									if self.mail[0] == playerManager.pDict[key].number:
										dif = time.time() - playerManager.pDict[key].activeCooldown
										break
									elif playerManager.pDict[key].PZero:
										dif = 3600
										break
								if dif > 3599:
									processedMessage = re.split('siege *', self.mail[1], flags=re.I)

									if processedMessage[0] != self.mail[1]:
										if playerManager.pDict[key].PZero or playerManager.pDict[key].zombie:
											if	re.match('tcb|kennedy center|east|science center|lowry|lowry hall|libary|kennedy|tunheim classroom buliding|beadle',processedMessage[1], flags=re.I)!=None:
												self.messenger.sendZombies("\nSiege " + processedMessage[1])
												playerManager.pDict[key].activeCooldown= time.time()

											elif re.match('mission*|tcb.*|kennedy center.*|science center.*|lowry.*|east.*|lowry hall|libary|kennedy|tunheim classroom buliding|beadle', processedMessage[1], flags=re.I)!=None:
												self.messenger.sendZombies("\nSiege " + processedMessage[1][-5:] + "at" + processedMessage[1][:-5]+".")
												playerManager.pDict[key].activeCooldown= time.time()
											else:
												self.messenger.sendSingle(self.mail[0],"Malformed siege command")
										else:
											self.messenger.sendSingle(self.mail[0], "Sieges can only be initated by PZ or zombies.")
									else:
										self.messenger.sendSingle(self.mail[0], "\nUnknown command, please try again.")
								else:
									self.messenger.sendSingle(self.mail[0], "\nYour ablity to call for seiges is on cooldown for another "+ dif)
				except Exception, e:
					pass
				#to make sure we don't get kicked off for making too many requests to fast.
				time.sleep(1)


class mailMan(object):
	"""mailMan manages player interactions such as tags reported via text messages or emails"""
	def __init__(self, playerManager):
		super(mailMan, self).__init__()
		self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
		self.mail.login(args.username,args.password)
		self.mail.list()
		# Out: list of "folders" aka labels in gmail.
		self.mail.select("inbox") #connect to inbox.

	def getBody(self, emailMessage):
		maintype = emailMessage.get_content_maintype()
		if maintype == 'multipart':
			for part in emailMessage.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif maintype == 'text':
			return emailMessage.get_payload()

	def getUnread(self):
		self.mail.select("inbox") # Select inbox or default namespace
		(retcode, messages) = self.mail.search(None, '(UNSEEN)')

		if retcode == 'OK' and messages[0] != '':
			retlist = []
			try:		
				for num in messages[0].split(' '):
					typ, data = self.mail.fetch(num,'(RFC822)')
					msg = email.message_from_string(data[0][1])
					if retcode == 'OK':
						for item in str(msg).split('\n'):
							#finds who sent the message
							if re.match("From: ",item):
								retlist.append((item[6:], self.getBody(msg).rstrip()))
			except Exception, e:
				return None
			return retlist
		else:
			return None



class players(object):
	"""manages the player"""
	def __init__(self, pDict):
		super(players, self).__init__()
		self.pDict = pDict
	#makes a particular player a zombie
	def makeZombie(self, pID):
		if pID in set(self.pDict.keys()):
			self.pDict[pID].zombie = True
			return True
		else:
			return False


	#makes a particular player a human
	def makeHuman(self, pID):
		if pID in self.pDict.keys():
			self.pDict[pID].zombie = False
			return True
		else:
			return False
	def chosePZ(self):

		picking = True
		print "\033c"
		while picking:
			#clears the screen.
			
			selection = raw_input("Enter the player ID of the player who you would like to be PZ.\nIf you don't enter anything here a pz will be chosen at random.\n-> ")
			if selection == "":
				selection = random.choice(self.pDict.keys())

				print "%s (%s) will be set as PZ, are you satisfied with this choice? (Y/N)" % (self.pDict[selection].getAttribs()[0], selection)
				
				satisfied = raw_input("-> ")
				if satisfied.lower() == 'y':
					self.pDict[selection].PZero = True
					picking = False
				elif satisfied.lower() != 'n':
					print "\033c"
					print "Please enter a 'Y' or an 'N'.\n"

			else:
				try:
					self.pDict[selection].PZero = True
					print "%s (%s) will be set as PZ, is this correct? (Y/N)" % (self.pDict[selection].getAttribs()[0], selection)
					satisfied = raw_input("-> ")

					if satisfied.lower() == 'y':
						self.pDict[selection].PZero = True
						picking = False
					elif satisfied.lower() != 'n':
						print "\033c"
						print "Please enter a 'Y' or an 'N'.\n"
				except:
					print "\033c"
					print "That player ID does not exist please enter another one."




#holds values for a single player
class player(object):
	"""represents players and their values"""
	def __init__(self, name, number, email):
		super(player, self).__init__()
		self.name = name
		self.number = number
		self.email = email
		self.zombie = False
		self.PZero = False
		self.kills = 0
		self.activeCooldown = 0
	#returns a tupple of the name, phone number(formated as an email address) and email address of the playes.
	def getAttribs(self):
		return (self.name, self.number, self.email, self.zombie, self.PZero, self.kills, self.activeCooldown)




#Handles the login and sending of email messages via SMTP
class messaging(object):
	"""Manages all functions of the program related to sending messages but not receving them"""
	def __init__(self,fromaddr,playerManager):
		super(messaging, self).__init__()
		self.fromaddr = fromaddr
		self.server = smtplib.SMTP('smtp.gmail.com:587')
		self.server.starttls()

		print "Atempting to long in to %s (username: %s)" % (self.fromaddr, args.username)
		try:
			self.server.login(args.username,args.password)
			print "login worked"
		except Exception, e:
			print "\nlogin failed, are your sure your username and password are correct?"
			sys.exit()

	#I should call all of the "send*" functions "text*" but im going to //todo that for now.
	def sendSingle(self, returnAddress, msg):
		self.server.sendmail(self.fromaddr, returnAddress, msg)

	def sendZombies(self, msg):
		for key in keys:
			if playerManager.pDict[key].zombie or playerManager.pDict[key].PZero:
				self.server.sendmail(self.fromaddr, playerManager.pDict[key].number, msg)
				time.sleep(0.5)

	def sendHumans(self, msg):
		for key in keys:
			if not playerManager.pDict[key].zombie:
				self.server.sendmail(self.fromaddr, playerManager.pDict[key].number, msg)
				time.sleep(0.5)

	def sendPZero(self, msg):
		for key in keys:
			if playerManager.pDict[key].PZero:
				self.server.sendmail(self.fromaddr,playerManager.pDict[key].number, msg)
				time.sleep(0.5)

	def sendPIDs(self, pIDlist, msg):
		for pIDs in pIDlist:
			self.server.sendmail(self.fromaddr, playerManager.pDict[pID].number, msg)
			time.sleep(0.5)

	def emailZombies(self, msg):
		for key in keys:
			if playerManager.pDict[key].zombie:
				self.server.sendmail(self.fromaddr, playerManager.pDict[key].email, msg)
				time.sleep(0.5)

	def emailHumans(self, msg):
		for key in keys:
			if not playerManager.pDict[key].zombie:
				self.server.sendmail(self.fromaddr, playerManager.pDict[key].email, msg)
				time.sleep(0.5)

	def emailPZero(self, msg):
		for key in keys:
			if playerManager.pDict[key].PZero:
				self.server.sendmail(self.fromaddr,playerManager.pDict[key].email, msg)
				time.sleep(0.5)





#############################################################################
##a couple of ultity funcitons that are up here for clenlyness			   ##
##and that realy only main (and truthfuly not even main) has to care about.##
#############################################################################

#cleens up the numbers from the .csv only needed by the main.
def cleenUpNumber(num):
	all=string.maketrans('','')
	nodigs=all.translate(all, string.digits)
	num = num.translate(all, nodigs)

	return num

#returns a dict of players 
def processFile(fileName):
	carrerDict = {'Alltel Wireless':'@message.Alltel.com', 'Boost Mobile':'@myboostmobile.com', 'AT&T':'@txt.att.net','Sprint':'@messaging.sprintpcs.com','Straight Talk':'@VTEXT.COM', 'T-Mobile':'@tmomail.net','U.S. Cellular':'@email.uscc.net', 'Verizon':'@vtext.com', 'Virgin Mobile':'@vmobl.com'}

	playerTempList=[]

	with open(fileName, 'rb') as csvFile:
		csvData = csv.reader(csvFile, dialect='excel')
		for row in csvData:
			#+9sdG is the SHA1 hash of an empty row
			if row[0] != "+9sdG":
				cleenNum = cleenUpNumber(row[2])

				cleenNum = cleenNum+carrerDict[row[3]]

				row.remove(row[2])
				row.insert(2, cleenNum)

				playerTempList.append((row[0], player(row[1],row[2],row[4])))
		playerDict = dict(playerTempList)

	return playerDict


#Main is mostly used to set some stuff up and for debug but honestly not much else because the rest of it is handled by the threads.
def main():


	#Create the object to handle sending messages.
	messenger = messaging(args.account, playerManager)
	#messenger = None
	if not args.r:
		playerManager.chosePZ()

	print "\033cSending players thier pIDs (this will take some time)..."
	tempNum = ""
	for key in keys:
		msg = "\nYour pID is " + key
		#print msg
		tempNum = playerManager.pDict[key].number
		messenger.sendSingle(tempNum, msg)
		msg = "\nThe follwing messages are a command reffrence, it is recomended that you save it for refrence throughtout the game. Commands have an hour cooldown."
		messenger.sendSingle(tempNum, msg)
		msg = "\nHelp location\nThe help command allows a human to call for help from other humans.\nExample: help east hall"
		messenger.sendSingle(tempNum, msg)
		msg = "\nTagged pID\nThe tagged command allows a zombe or PZ to report a tag without having to get a hold of the admins.\nExample: tagged +9sdG"
		messenger.sendSingle(tempNum, msg)
		msg = "\nSiege location HH:MM\nActs like help but for zombies, is sent to all zombies, the location must be on campus.\nExample: siege science center"
		messenger.sendSingle(tempNum, msg)

	messenger.sendPZero("Hello, you have been selected as PZ for this gmae, you have no cooldown on your seiges")
	mail = mailMan(playerManager)
	#mail=None
	game = gameLogic(playerManager,mail, messenger)
	menu(game.run(), messenger)



if __name__ == '__main__':
	#parses the args...
	parser = argparse.ArgumentParser(description="Helps with adminstration and management of Humans Vs. Zombies games.")
	parser.add_argument('account',	type=str, help="The address of the email account you are using i.e. example@gmail.com")
	parser.add_argument('username', type=str, help="The username of the email account you want to login to.")
	parser.add_argument('password', type=str, help="The password of the email account you want to login to.")
	parser.add_argument('-f', type=str, help="The name of the .csv file containing the list of players.\nWill be ignored if the -r flag is given.")
	parser.add_argument('-r', action='store_true', help="Tells the program to atempt to recover a game that has been shut down.")

	args=parser.parse_args()

	#checks to see that flags are set.
	if not args.r and args.f == None:
		raw_input("Please set either the -f or the -r flag.\n<--Press Enter To Exit-->")
		sys.exit()

	#attempts to recover from a backup
	if args.r:
		fp = open('backup.dat', 'rb')
		playerManager = pickle.load(fp)
	else:
		#create the player manager object from the .csv
		playerManager = players(processFile(args.f))
		keys = playerManager.pDict.keys()
	main()