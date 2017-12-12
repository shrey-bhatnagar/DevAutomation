#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import logging
from files.applogging import Logger_check
from files.sshAutomation import Devstack
from files.osloconfig import get_config
from files.readjson import get_jsonconfig
from files.readyaml import get_yamlconfig
from main import maincompilationcheck
from files.osloconfig import osloconfigcompilationcheck
from files.readjson import readjsoncompilationcheck
from files.readyaml import readyamlcompilationcheck
from files.sshAutomation import sshAutomationcompilationcheck
from files.applogging import apploggingcompilationcheck
from files.applogging import Logger_check


mylog = Logger_check('checkcompilation', logging.INFO)


def myprint(str):
    print(str)
    mylog.log.info(str)


if __name__ == '__main__':
    myprint('Starting checkcompilation.py')
    data = get_config()
    if(data):
        myprint('OSLO_config read pass')
    else:
        myprint('OSLO_config read fail')
    data = get_jsonconfig()
    if(data):
        myprint('JSON read pass')
    else:
        myprint('JSON read fail')
    data = get_yamlconfig()
    if(data):
        myprint('YAML read pass')
    else:
        myprint('YAML read fail')
    data = maincompilationcheck()
    if(data):
        myprint('interpretation of main.py pass')
    else:
        myprint('interpretation of main.py fail')
    data = osloconfigcompilationcheck()
    if(data):
        myprint('interpretation of osloconfig.py pass')
    else:
        myprint('interpretation of osloconfig.py fail')
    data = readjsoncompilationcheck()
    if(data):
        myprint('interpretation of readjson.py pass')
    else:
        myprint('interpretation of readjson.py fail')
    data = readyamlcompilationcheck()
    if(data):
        myprint('interpretation of readyaml.py pass')
    else:
        myprint('interpretation of readyaml.py fail')
    data = sshAutomationcompilationcheck()
    if(data):
        myprint('interpretation of sshAutomation.py pass')
    else:
        myprint('interpretation of sshAutomation.py fail')
    data = apploggingcompilationcheck()
    if(data):
        myprint('interpretation of applogging.py pass')
    else:
        myprint('interpretation of applogging.py fail')
    mylog.log.info('Stoping checkcompilation.py\r\n\r\n')
