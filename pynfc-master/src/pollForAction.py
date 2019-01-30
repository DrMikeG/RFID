#!/usr/bin/python

import os
import sys
import logging
from readNFC import NFCReader
from socketIO_client import SocketIO, LoggingNamespace

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

    def __init__(self,args):
        self.data = []
        self._options = []
        if len(args) == 2:
      		self.configureFromFile(args[1])

    def lookupActionFromOptions(self, data):
       if data in self._options.keys():
           return self._options[data]
       else:
           return None

    def configureFromFile(self, data):
       if (self._argIsValidFile(data) != None):
         print "Parsing config ",data 
         self._options = FileParser().parse_config(data)

    def getOptionsCount(self):
       return len(self._options)

    def runActionLoopForever(self):
       print("run Action main function")
       logger = logging.getLogger("cardhandler").info
       while NFCReader(logger).run(self._handleCardReadUIDCallback):
           pass


    def _argIsValidFile(self,data):
       if not isinstance(data, basestring):
           return None
       exists = os.path.isfile(data)
       if exists:
           return data
       else:
           return None
    
    def _handleCardReadUIDCallback(self,uid):
	if uid :
                uidStr = uid.encode("hex")
        	print "Received card uid", uidStr
        action = self.lookupActionFromOptions(uidStr)
        if action != None :
		print "Known action", action
                self.dispatchActionToSocket(action)
        else:
                print "Unknown action"

    def dispatchActionToSocket(self,action):
    	socketIO = SocketIO('localhost', 3000, LoggingNamespace)
    	socketIO.emit('replaceAndPlay', {"uri":action})


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
if __name__ == '__main__':
    PollForAction(sys.argv).runActionLoopForever()
