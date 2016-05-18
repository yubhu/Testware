"""Logging module   

This module manages logging for the entire test automation framework.
All the modules use this module to log debug messages into debug logs.

It has functions to create logger, as well as a few other utility functions.

"""



import logging
from logging import Handler, getLogger
from Tkinter import *

log_dir = ""

# The path of the Beyond compare 3 program
BC3 = "C:\Program Files\Beyond Compare 3\BComp.exe"


class Logger():
    """Logger class"""

    index = 0

    def __init__(self):
        
		"""Create the logger"""
    
        
		self.l = logging.getLogger()
        
		self.l.setLevel(logging.DEBUG)
        
		self.l.addHandler(logging.NullHandler()) #By default, no logging
		self.fh = "" #File handler
		self.ch = "" #Console handler
		self.box = "NO BOX"
				
	

	
    def create_loghandler(self, logfile="", logtoconsole = 1):
        """Creates logging handler. Two handlers can be created.
        One that writes to the file, another that writes to the console.
        Both can be controlled on or off using the two input arguments.
        
        It is expected that the same file will be written to every time (in a
        session).
        For example, if 2 calls are made to this function, each time with a
        different logfile argument, the second one will be ignored. In other
        words, logs will continue to be logged into the first file. 
        If logging to the second file is desired, then the first file should first
        be 'closed' with a call to this function with the logfile argument set
        to "", and then another call should be made with the logfile argument
        set to the second file.


        For logging to the console, it can be turned off and on with the logtoconsole
        argument.
        """

        # create logger

        if logfile != "":
            if not self.fh:
                #Create a file handler that prints to the file by prepending
                #the message with a time-stamp
                self.fh = logging.FileHandler(logfile) #File handler

                formatter = logging.Formatter("%(asctime)s %(message)s")
                self.fh.setFormatter(formatter)

                self.l.addHandler(self.fh)        

        else:
            if self.fh:
                self.fh.close()
                self.l.removeHandler(self.fh)
                self.fh = ""


        if logtoconsole == 1:
            if not self.ch:
                #Create a console handler that prints to the console by prepending
                #the message with a time-stamp
                self.ch = logging.StreamHandler()

                # create formatter
                formatter = logging.Formatter("%(message)s")
                # add formatter to self.ch
                self.ch.setFormatter(formatter)

                # add self.ch to logger
                self.l.addHandler(self.ch)
        else:
            if self.ch:
                self.ch.close()
                self.l.removeHandler(self.ch)
                self.ch = ""
				
		
		# self.wh = logging.ListboxHandler(target)
				
		# # create formatter
		# formatter = logging.Formatter("%(asctime)s %(message)s")
		# # # add formatter to self.ch
		# self.wh.setFormatter(formatter)
		# self.l.addHandler(self.wh)
			
	

    def log(self, s, logtobox=1):
		"""Print the supplied string using the logging handler"""

		self.l.debug(s)

		#if box is provided, pipe to box
		
		if (logtobox == 1):
			if (self.box != "NO BOX"):
				self.box.insert(END,s)
				#self.box.select_clear(self.box.size()-2)
				#self.box.select_set(END)
				self.box.yview(END)
				self.box.update()
				self.index =+ 1

    def addBox(self, box):
        self.box = box
        return
