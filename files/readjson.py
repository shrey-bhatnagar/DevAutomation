#!/usr/bin/env python

from __future__ import print_function
import json


def get_jsonconfig():
    with open('configration/myappConfig.json') as file:
        jsondata = json.loads(file.read())
    return jsondata

#for module compilation check
def readjsoncompilationcheck():
    return True


if __name__ == '__main__':
    get_jsonconfig()
            
