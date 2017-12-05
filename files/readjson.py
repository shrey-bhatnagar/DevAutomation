#!/usr/bin/env python

from __future__ import print_function
import json


def get_jsonconfig():
    with open('myappConfig.json') as file:
        jsondata = json.loads(file.read())
    return jsondata


if __name__ == '__main__':
    get_jsonconfig()
