#coding=utf-8
 
import logging
import time
import os

# name      : log name which is located in ./log/
# fmode     : it decides which methods used by fileHandler
# fLevel    : fileLog level
# cLevel    : consoleLog level

class dLog:
    def __init__(self,name,fmode,fLevel,cLevel):
        if not os.path.isdir('log') :
            os.makedirs('log')
        self.logname = os.path.join('log/', '{0}.log'.format(name))
        self.logger = logging.getLogger(name)
        self.logger.setLevel(cLevel)

        fh = logging.FileHandler(self.logname,fmode,encoding='utf-8')
        fh.setLevel(fLevel)

        ch = logging.StreamHandler()
        #ch.setLevel(cLevel)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def debug(self,message):
        self.logger.debug(message)
 
    def info(self,message):
        self.logger.info(message)
 
    def warning(self,message):
        self.logger.warning(message)
 
    def error(self,message):
        self.logger.error(message)
