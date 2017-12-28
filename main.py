#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import pdb
import logging
from Script_Dir.sshAutomation import Devstack
from Script_Dir.sshAutomation import ping_check_for_server
from Script_Dir.readjson import get_jsonconfig
from Script_Dir.applogging import LoggerCreate


my_Log = LoggerCreate('event_logger', logging.INFO)


def print_log(str):
    print(str)
    my_Log.log.info(str)


def maincompilationcheck():
    return True


def listuser(command, CONF):
    cmd1 = 'cut -d: -f1 /etc/passwd'
    command.cmd(cmd1)


def deluser(command, delusername):
    cmd1 = 'deluser --remove-home %s' % (delusername)
    command.cmd(cmd1)


def check_test_status(list_data, last_val):
    data1, newlist = [], []
    count_pass = 0
    count_fail = 0
    data1 = list_data[-last_val:]
    for i in data1:
        newlist.append(i.split('\n')[0])
    while '' in newlist:
        newlist.remove('')
    # print newlist
    for s in newlist:
        if 'PASS' in s:
            count_pass = count_pass + 1
        elif 'FAIL' in s:
            count_fail = count_fail + 1
    print_log("TEST execution Completed")
    print_log(":::Summary:::")
    print_log("Cases PASS == %s" % count_pass)
    print_log("Cases FAIL == %s" % count_fail)


def devstack_infra_creation(devinstalation, devdata):

    devVersion = \
        'git clone https://github.com/shrey-bhatnagar/DevAutomation.git'
    apt_git_success, apt_git_error = \
        devinstalation.cmd('apt install git -y', sudo=True)
    print_log("Installing GIT...............")
    success_check = 'git is already the newest version.\n'
    fail_check = 'Suggested packages:\n'
    if apt_git_success[3] == success_check:
        print_log(apt_git_success)
        print_log("Git is already the newest version......\
                  . Skipping GIT installation")
    elif apt_git_success[3] == fail_check:
        print_log(apt_git_error)
        print_log(".Git has been installed successfully.")
    else:
        print_log(" GIT install Has some error ... Please re-verify")

    print_log("Cloning repository.")
    print_log(devVersion)
    clone_repo_success, clone_repo_fail = \
        devinstalation.cmd(devVersion, sudo=False)
    # devVersion =
    # 'git clone https://github.com/openstack-dev/devstack.git -b \
    #         stable/ocata'
    # devinstalation.cmd(devVersion, sudo=True)
    if clone_repo_fail != []:
        sub_clone = clone_repo_fail[0].split()
        if sub_clone[0] == "Cloning":
            print_log(clone_repo_fail)
            print_log('Repository Cloned Successfully')
        else:
            if sub_clone[0] == 'fatal:':
                print_log(clone_repo_fail)
                print_log('Repository Already Exists.... Cloning not required')
    devinstalation.local_conf(devdata['file_name'],
                              devdata['data_local'])

    print_log('RUNNING DEVSTACK TEST')

    dev_test_success, dev_test_error =\
        devinstalation.cmd('source /opt/stack/devstack/run_tests.sh')
    check_test_status(dev_test_success, 13)
    # print(dev_test_success, dev_test_error)
    # devinstalation.cmd('cd devstack')
    # devinstalation.cmd('source /devstack/stack')


def create_devstack_user(userinstalation, devdata):
    print_log("Creating devstack user : %s" % devdata['devUser'])
    add_user = "useradd -s /bin/bash -d /opt/%s -m %s" % \
               (devdata['devUser'], devdata['devUser'])
    add_user_to_file = 'echo "%s ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers' % \
                       (devdata['devUser'])
    devusername = devdata['devUser']
    devuserpwd = devdata['devUserPwd']
    setpwd = True
    userinstalation.rootcmd(add_user, add_user_to_file,
                            setpwd, devusername, devuserpwd)
    print_log("User Creation Successfull")


def fetch_data_for_user(jsondata):
    userdata = jsondata['userdata']
    devdata = jsondata['devdata']
    userinstalation = Devstack(
            userdata['ip'], userdata['username'], userdata['password'])
    # userinstalation.rootcmd1(devdata['devUser'])
    create_devstack_user(userinstalation, devdata)
    userinstalation.close_host_connection()


def install_devstack(devdata):
    devinstalation = Devstack(
        devdata['ip'], devdata['devUser'], devdata['devUserPwd'])
    devstack_infra_creation(devinstalation, devdata)
    devinstalation.close_host_connection()


def connect_to_host():
    jsondata = get_jsonconfig()
    if ping_check_for_server(jsondata['appdata']['devdata']['ip']):
        pass
    else:
        sys.exit()
    fetch_data_for_user(jsondata['appdata'])
    install_devstack(jsondata['appdata']['devdata'])


if __name__ == '__main__':
    print_log('Starting Devstack infrastructure Creation\n')
    connect_to_host()
    print_log('Execution has been completed......Please check the log under\
            ..../logs/event_logger.log')
