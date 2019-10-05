#!/usr/bin/python

import os
import sys
import logging
import time
import subprocess
from readNFC import NFCReader
from socketIO_client import SocketIO, LoggingNamespace
from logging.handlers import RotatingFileHandler

class FileParser:
    COMMENT_CHAR = '#'
    OPTION_CHAR =  '='
 
    def parse_config(self,filename):
        options = {}
        f = open(filename)
        for line in f:
            # First, remove comments:
            if self.COMMENT_CHAR in line:
                # split on comment char, keep only the part before
                line, comment = line.split(self.COMMENT_CHAR, 1)
                # Second, find lines with an option=value:
            if self.OPTION_CHAR in line:
                # split on option char:
                option, value = line.split(self.OPTION_CHAR, 1)
                # strip spaces:
                option = option.strip()
                value = value.strip()
                # store in dictionary:
                options[option] = value
        f.close()
        return options
 

class PollForAction:

    def __init__(self,args,logger):
        self.data = []
        self._options = []
        self.logger = logger
        self.logger.info("Starting pollForAction.py")
        self.logger.info("Number of arguments %s", len(sys.argv) )
        self.logger.info("Argument List: %s", str(sys.argv) )
      
        if len(args) == 2:
            self.configureFromFile(args[1])
	else:
	    self.logger.error("No config file specified")


    def lookupActionFromOptions(self, data):
       if data in self._options.keys():
           return self._options[data]
       else:
           return None

    def configureFromFile(self, data):
       self.logger.info("configure")
       if (self._argIsValidFile(data) != None):
         self.logger.info("Parsing config %s", data) 
         self._optionsReloadFile = data
         self._options = FileParser().parse_config(data)
         self.logger.info("Found %i",self.getOptionsCount())

    def getOptionsCount(self):
       return len(self._options)

    def runActionLoopForever(self):
       self.logger.info("run ActionLoopForever")
       self.logger.info("pausing for 60 seconds")
       time.sleep(60)
       self.logger.info("pause over - attempting card reading")

       restartCount = 0;
       while NFCReader(self.logger).run(self._handleCardReadUIDCallback):
		restartCount+=1
		if restartCount == 10:
			restartCount = 0
			self.configureFromFile(self._optionsReloadFile)
	#pass #The pass statement does nothing. It can be used when a statement is required syntactically but the program requires no action


    def _argIsValidFile(self,data):
       if not isinstance(data, basestring):
           return None
       exists = os.path.isfile(data)
       if exists:
           return data
       else:
           return None
    
    def _handleCardReadUIDCallback(self,uid):
        self.goPop()
	if uid :
                uidStr = uid.encode("hex")
        	self.logger.info("Received card uid %s", uidStr)
        action = self.lookupActionFromOptions(uidStr)
        if action != None :
		self.logger.info("Known action %s", action)
                self.dispatchActionToSocket(action)
        else:
                self.logger.info("Unknown action")

    def dispatchActionToSocket(self,action):
    	socketIO = SocketIO('localhost', 3000, LoggingNamespace)
    	if str(action).startswith("STOP"):
		self.logger.info("Issuing stop command")
		socketIO.emit('stop',{}); 
	else:
		self.logger.info("replace and play %s",action)
		socketIO.emit('replaceAndPlay', {"uri":action})

    def goPop(self):
        subprocess.call(['aplay -fdat /home/volumio/RFID/pop/pop1.wav'], shell=True)
 
def createRotatingLog():
	# create logger
	logger = logging.getLogger('simple_example')
	logger.setLevel(logging.INFO)

        log_file = '/home/volumio/poll.log'
        rh = RotatingFileHandler(log_file, maxBytes=2*1024*1024,backupCount=5) # allow 6 * 2MB logfiles
	rh.setLevel(logging.INFO)

	# create console handler and set level to debug
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	
	# create formatter
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

	# add formatter to ch
	ch.setFormatter(formatter)
	rh.setFormatter(formatter)

	# add ch to logger
	logger.addHandler(ch)
	logger.addHandler(rh)

        logger.info('The local time is %s', time.asctime())
        return logger

if __name__ == '__main__':
    logger = createRotatingLog()
    PollForAction(sys.argv,logger).runActionLoopForever()
