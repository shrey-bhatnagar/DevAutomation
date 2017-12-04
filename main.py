#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time

from files.sshAutomation import Devstack
from files.app import get_config
from files.app import shrey

#variable that need to be edited
data_local = '[[local|localrc]]\r\nRECLONE=True\r\nHOST_IP=192.168.195.182\r\nSERVICE_TOKEN=mytoken123\r\nADMIN_PASSWORD=openstack123\r\nMYSQL_PASSWORD=mysql123\r\nRABBIT_PASSWORD=rabbit123\r\nSERVICE_PASSWORD=$ADMIN_PASSWORD\r\nLOGFILE=$DEST/logs/stack.sh.log\r\nLOGDAYS=2\r\nenable_plugin neutron-lbaas https://github.com/openstack/neutron-lbaas.git stable/ocata\r\ndisable_service n-net c-api c-sch c-vol\r\nenable_service q-svc q-agt q-dhcp q-l3 q-meta q-lbaasv2'

def listuser(command, CONF):
    cmd1 = 'cut -d: -f1 /etc/passwd'
    command.cmd(cmd1)


def deluser(command, delusername):
    cmd1 = 'deluser --remove-home %s' % (delusername)
    command.cmd(cmd1)


def devsetup(devinstalation, CONF):
    devinstalation.cmd('apt install git -y', sudo=True)
    devVersion = 'git clone https://github.com/openstack-dev/devstack.git -b stable/ocata'
    devinstalation.cmd(devVersion, sudo=True)
    devinstalation.local_conf(CONF.appdata.file_name, data_local)


def usercreation(userinstalation, CONF):
    cmd1 = "useradd -s /bin/bash -d /opt/%s -m %s" % (CONF.appdata.devUser, CONF.appdata.devUser)
    cmd2 = 'echo "%s ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' % (CONF.appdata.devUser)
    devusername = CONF.appdata.devUser
    devuserpwd = CONF.appdata.devUserPwd
    setpwd=True
    userinstalation.rootcmd(cmd1,cmd2,setpwd,devusername,devuserpwd)


def connect_ssh():
    CONF = get_config()
    userinstalation=Devstack(CONF.appdata.ip, CONF.appdata.username, CONF.appdata.password)
    usercreation(userinstalation, CONF)
    devinstalation=Devstack(CONF.appdata.ip, CONF.appdata.devUser, CONF.appdata.devUserPwd)
    devsetup(devinstalation, CONF)


if __name__ == '__main__':
    print('starting '+ __name__)
    connect_ssh()
    print('stoping'+ __name__)
