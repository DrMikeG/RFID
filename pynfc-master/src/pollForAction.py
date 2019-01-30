#!/usr/bin/python

import os
import sys

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

    def __init__(self,*args):
        self.data = []
        self._options = []

    def lookupActionFromOptions(self, data):
       if data in self._options.keys():
           return self._options[data]
       else:
           return None

    def configureFromFile(self, data):
       if (self.argIsValidFile(data) != None):
         self._options = FileParser().parse_config(data)

    def getOptionsCount(self):
       return len(self._options)

    def add(self, x):
        self.data.append(x)

    def addtwice(self, x):
        self.add(x)
        self.add(x)
 
    def runActionLoopForever(self):
       print("Bag main function")

    def argIsValidFile(self,data):
       if not isinstance(data, basestring):
           return None
       exists = os.path.isfile(data)
       if exists:
           return data
       else:
           return None


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
if __name__ == '__main__':
    Bag(sys.argv).runActionLoopForever()
