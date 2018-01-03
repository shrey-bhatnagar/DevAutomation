#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import logging
from Script_Dir.applogging import LoggerCreate
from Script_Dir.sshAutomation import Devstack
from Script_Dir.osloconfig import get_config
from Script_Dir.readjson import get_jsonconfig
from Script_Dir.readyaml import get_yamlconfig
from main import maincompilationcheck
from Script_Dir.osloconfig import osloconfigcompilationcheck
from Script_Dir.readjson import readjsoncompilationcheck
from Script_Dir.readyaml import readyamlcompilationcheck
from Script_Dir.sshAutomation import sshAutomationcompilationcheck
from Script_Dir.applogging import apploggingcompilationcheck


mylog = LoggerCreate('checkcompilation', logging.INFO)


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
