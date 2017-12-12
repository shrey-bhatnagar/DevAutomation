#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import pdb
import logging
from files.sshAutomation import Devstack
from files.osloconfig import get_config
from files.osloconfig import shrey
from files.readjson import get_jsonconfig
from files.applogging import Logger_check


mylog = Logger_check('main', logging.INFO)


def myprint(str):
    print(str)
    mylog.log.info(str)


def maincompilationcheck():
    return True


def listuser(command, CONF):
    cmd1 = 'cut -d: -f1 /etc/passwd'
    command.cmd(cmd1)


def deluser(command, delusername):
    cmd1 = 'deluser --remove-home %s' % (delusername)
    command.cmd(cmd1)


def devsetup(devinstalation, devdata):
    apt_git_success, apt_git_error = \
            devinstalation.cmd('apt install git -y', sudo=True)
    if apt_git_success[3] == 'git is already the newest version.\n':
        myprint('##########################################')
        myprint("### Git is already the newest version. ###")
        myprint('##########################################')
    elif apt_git_success[3] == 'Suggested packages:\n':
        myprint('##############################')
        myprint("### Git has been installed ###")
        myprint('##############################')
    else:
        myprint(" GIT install Has some error ... Please re-verify")

    devVersion = \
        'git clone https://github.com/shrey-bhatnagar/DevAutomation.git'
    clone_repo_success, clone_repo_fail = \
        devinstalation.cmd(devVersion, sudo=False)
    # devVersion =
    # 'git clone https://github.com/openstack-dev/devstack.git -b \
    #         stable/ocata'
    # devinstalation.cmd(devVersion, sudo=True)
    if clone_repo_fail != []:
        sub_clone = clone_repo_fail[0].split()
        if sub_clone[0] == "Cloning":
            myprint('#################################')
            myprint('########Repository Cloned########')
            myprint('#################################')
        else:
            if sub_clone[0] == 'fatal:':
                myprint('#################################')
                myprint('####Repository Already Exists####')
                myprint('#################################')
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
    # userinstalation.rootcmd1(devdata['devUser'])
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
    mylog.log.info('Starting main.py')
    myprint('we are testing the printing')
    connect_ssh()
    mylog.log.info('Stoping main.py\r\n\r\n')
