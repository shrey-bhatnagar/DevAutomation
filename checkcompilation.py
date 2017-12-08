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


if __name__ == '__main__':
    # print('starting ' + __name__)
    mylog = Logger_check('checkcompilation', logging.INFO)
    mylog.log.info('Starting checkcompilation.py')
    data = get_config()
    if(data):
        print('OSLO_config read pass')
    else:
        print('OSLO_config read fail')
    data = get_jsonconfig()
    if(data):
        print('JSON read pass')
    else:
        print('JSON read fail')
    data = get_yamlconfig()
    if(data):
        print('YAML read pass')
    else:
        print('YAML read fail')
    data = maincompilationcheck()
    if(data):
        print('interpretation of main.py pass')
    else:
        print('interpretation of main.py fail')
    data = osloconfigcompilationcheck()
    if(data):
        print('interpretation of osloconfig.py pass')
    else:
        print('interpretation of osloconfig.py fail')
    data = readjsoncompilationcheck()
    if(data):
        print('interpretation of readjson.py pass')
    else:
        print('interpretation of readjson.py fail')
    data = readyamlcompilationcheck()
    if(data):
        print('interpretation of readyaml.py pass')
    else:
        print('interpretation of readyaml.py fail')
    data = sshAutomationcompilationcheck()
    if(data):
        print('interpretation of sshAutomation.py pass')
    else:
        print('interpretation of sshAutomation.py fail')
    data = apploggingcompilationcheck()
    if(data):
        print('interpretation of applogging.py pass')
    else:
        print('interpretation of applogging.py fail')
    mylog.log.info('Stoping checkcompilation.py')
    # print('stoping' + __name__)
