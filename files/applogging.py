#!/usr/bin/env python


import logging
import os
from logging.handlers import RotatingFileHandler


class Logger_check:
    def __init__(self, modulename, loglevel=logging.INFO):
        self.init_log(modulename+'.log', loglevel, modulename)
        self.log = logging.getLogger(modulename)

    def init_log(self, filename, level, logger):
        directory = os.getcwd()
        # directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s - %(message)s\r\n')
        log = logging.getLogger(logger)

        # filehandler=RotatingFileHandler(filenme,maxBytes=2000,backupCount=10)
        loglocation = directory+"/logs/"+filename
        filehandler = logging.FileHandler(loglocation, mode='a')
        filehandler.setFormatter(formatter)

        log.setLevel(level)
        log.addHandler(filehandler)


def apploggingcompilationcheck():
    return True
