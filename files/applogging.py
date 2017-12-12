#!/usr/bin/env python


import logging
import os
from logging.handlers import RotatingFileHandler


class Logger_check:
    def __init__(self, modulename, loglevel=logging.INFO):
        self.init_log(modulename+'.log', loglevel, modulename)
        self.log = logging.getLogger(modulename)

    def init_log(self, filename, level, logger):
        PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.dirname(PROJECT_ROOT)
        # directory = os.getcwd()
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)

        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s - %(message)s\r\n')
        log = logging.getLogger(logger)

        # filehandler=RotatingFileHandler(filenme,maxBytes=2000,backupCount=10)
        loglocation = BASE_DIR+"/logs/"+filename
        filehandler = logging.FileHandler(loglocation, mode='a')
        filehandler.setFormatter(formatter)

        log.setLevel(level)
        log.addHandler(filehandler)


def apploggingcompilationcheck():
    return True
