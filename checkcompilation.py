#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time

from files.sshAutomation import Devstack
from files.app import get_config
# from files.app import shrey
from files.readjson import get_jsonconfig
from files.readyaml import get_yamlconfig
from main import maincompilationcheck
from files.app import appcompilationcheck
from files.readjson import readjsoncompilationcheck
from files.readyaml import readyamlcompilationcheck
from files.sshAutomation import sshAutomationcompilationcheck

if __name__ == '__main__':
    # print('starting ' + __name__)
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
    data = appcompilationcheck()
    if(data):
        print('interpretation of app.py pass')
    else:
        print('interpretation of app.py fail')
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
    # print('stoping' + __name__)
