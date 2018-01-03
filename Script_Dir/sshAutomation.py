#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import re
import exception
import logging
from Script_Dir.applogging import LoggerCreate


mylog = LoggerCreate('event_logger', logging.INFO)


def print_log(str):
    print(str)
    mylog.log.info(str)

def ping_check_for_server(ip_add):
    response = os.system("ping -c 1 {}".format(ip_add))
    if response == 0:
        print_log("Server is Active!\n")
        return True
    else:
        print_log("Server is inactive!\n")
        return False


class Devstack:
    ip_address = None

    def __init__(self, ip, user, pwd):
        self.ip_address = ip
        self.username = user
        self.password = pwd

        if ping_check_for_server:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                print_log("trying to SSH connection with %s" % self.ip_address)
                self.ssh.connect(ip, username=user, password=pwd, port=22)
                print_log("SSH connection established to %s" % self.ip_address)

            except paramiko.AuthenticationException:
                print_log("Authentication Failed")

            except paramiko.BadHostKeyException:
                print_log("Bad HostKey values")

            except paramiko.SSHException:
                print_log("Connection Failed")

            except:
                print_log("Unknown error")

            self.ssh.load_system_host_keys()

        else:
            sys.exit()


    def __del__(self):
        if self.ssh:
            try:
                print_log("SSH connection closed for %s\r\n" % self.ip_address)
                self.ssh.close()
                self.ssh = None
            except:
                pass

    def close_host_connection(self):
        if self.ssh:
            try:
                print_log("SSH connection closed for %s\r\n" % self.ip_address)
                self.ssh.close()
                self.ssh = None
            except:
                pass

    def local_conf(self, filename, data):
        f = None
        self.sftp = self.ssh.open_sftp()
        filepath = filename
        try:
            try:
                self.sftp.chdir('devstack')
            except IOError:
                self.sftp.mkdir('devstack')
                filepath = 'devstack/' + filename
            f = self.sftp.open(filepath, 'w')
            f.write(data)

        except exception as e:
            print_log('*** Caught exception: %s: %s' % (e.__class__, e))
        f.close()

    def rootcmd(self, cmd1, cmd2, setpwd=False,
                username='default', pwd='root'):
        channel = self.ssh.invoke_shell()
        out = channel.recv(9999)
        channel.send('sudo su -\r\n')
        time.sleep(2)
        channel.send(self.password+'\r\n')
        time.sleep(5)
        # while not channel.recv_ready():
        #     time.sleep(3)
        # out = channel.recv(9999)
        # print_log(out.decode("ascii"))
        channel.send(cmd1+'\r\n')
        time.sleep(2)
        channel.send(cmd2+'\r\n')
        time.sleep(2)
        if(setpwd):
            channel.send('passwd '+username+'\r\n')
            time.sleep(2)
            channel.send(pwd+'\r\n')
            time.sleep(2)
            channel.send(pwd+'\r\n')
            time.sleep(2)
        while not channel.recv_ready():
            time.sleep(3)
        out = channel.recv(9999)
        print_log(out.decode("ascii"))

    def cmd(self, command, sudo=False):
        feed_password = False
        if (sudo):
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and \
                            len(self.password) > 0
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        # return {'out': stdout.readlines(),
        #         'err': stderr.readlines(),
        #         'retval': stdout.channel.recv_exit_status()}
        return(stdout.readlines(), stderr.readlines())

    def rootcmd1(self, username='default'):
        channel = self.ssh.invoke_shell()
        out = channel.recv(9999)
        channel.send('sudo su - '+username+'\r\n')
        time.sleep(2)
        channel.send(self.password+'\r\n')
        time.sleep(3)
        channel.send('cd devstack\r\n')
        time.sleep(1)
        channel.send('./run_tests.sh\r\n')
        # channel.send('ls -lrt\r\n')
        max_loops = 5000
        not_done = True
        MAX_BUFFER = 655351
        output = ''
        i = 0
        sys.stdout.flush()
        sys.stdin.flush()
        while (not_done) and (i <= max_loops):
            time.sleep(1)
            i += 1
            # Keep reading data as long as available (up to max_loops)
            if channel.recv_ready():
                output += channel.recv(MAX_BUFFER)
                # print("Lenght ", len(channel.recv(MAX_BUFFER)))
            else:
                not_done = False
        print_log(output)


def sshAutomationcompilationcheck():
    return True


if __name__ == '__main__':
    print_log('starting ' + __name__)
    instal1 = Devstack(ip, username, password)
    instal1.cmd('ls -al')
    instal1.local_conf(file_name, data_local)
    print_log('stoping')