#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import pdb

from files.sshAutomation import Devstack
from files.app import get_config
from files.app import shrey
from files.readjson import get_jsonconfig


def listuser(command, CONF):
    cmd1 = 'cut -d: -f1 /etc/passwd'
    command.cmd(cmd1)


def deluser(command, delusername):
    cmd1 = 'deluser --remove-home %s' % (delusername)
    command.cmd(cmd1)


def devsetup(devinstalation, devdata):
    devinstalation.cmd('apt install git -y', sudo=True)
    # devVersion =
    # 'git clone https://github.com/openstack-dev/devstack.git -b \
    #         stable/ocata'
    # devinstalation.cmd(devVersion, sudo=True)
    # pdb.set_trace()  # we are breaking here to check !!!
    devinstalation.local_conf(devdata['file_name'],
                              devdata['data_local'])
    # devinstalation.cmd('cd devstack')
    # devinstalation.cmd('./stack')


def usercreation(userinstalation, devdata):
    cmd1 = "useradd -s /bin/bash -d /opt/%s -m %s" % \
            (devdata['devUser'], devdata['devUser'])
    cmd2 = 'echo "%s ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' % \
           (devdata['devUser'])
    devusername = devdata['devUser']
    devuserpwd = devdata['devUserPwd']
    setpwd = True
    userinstalation.rootcmd(cmd1, cmd2, setpwd, devusername, devuserpwd)


def step1(jsondata):
    userdata = jsondata['userdata']
    devdata = jsondata['devdata']
    userinstalation = Devstack(
            userdata['ip'], userdata['username'], userdata['password'])
    usercreation(userinstalation, devdata)
    userinstalation.close()


def step2(devdata):
    devinstalation = Devstack(
        devdata['ip'], devdata['devUser'], devdata['devUserPwd'])
    devsetup(devinstalation, devdata)
    devinstalation.close()


def connect_ssh():
    jsondata = get_jsonconfig()
    step1(jsondata['appdata'])
    step2(jsondata['appdata']['devdata'])


if __name__ == '__main__':
    print('starting ' + __name__)
    connect_ssh()
    print('stoping' + __name__)
