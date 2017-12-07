#!/usr/bin/env python

import os
import sys
import select
import paramiko
import time
import re
import exception


class Devstack:
    ip_address = 'x.x.x.x'

    def __init__(self, ip, user, pwd, key=None, passphrase=None):
        self.ip_address = ip
        self.username = user
        self.password = pwd
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # if key is not None:
        #    key = paramiko.RSAKey.from_private_key(StringIO(key),\
        #    password = passphrase)
        try:
            print("trying to SSH connection with %s" % self.ip_address)
            self.ssh.connect(ip, username=user, password=pwd, port=22)
            print("SSH connection established to %s" % self.ip_address)
        except paramiko.SSHException:
            print("Connection Failed")
            quit()
        except paramiko.AuthenticationException:
            print("Authentication Failed")
            quit()
        except:
            print("Unknown error")
            quit()
        self.ssh.load_system_host_keys()

    # def __del__(self):
    #    print("SSH connection clossed for %s" % self.ip_address)
    #    self.ssh.close()

    def close(self):
        if self.ssh is not None:
            try:
                self.ssh.close()
                self.ssh = None
            except:
                pass

    def local_conf(self, filename, data):
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
            print '*** Caught exception: %s: %s' % (e.__class__, e)
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
        # print(out.decode("ascii"))
        channel.send(cmd1+'\r\n')
        time.sleep(2)
        channel.send(cmd2+'\r\n')
        time.sleep(2)
        if(setpwd):  # if(setpwd != False):
            channel.send('passwd '+username+'\r\n')
            time.sleep(2)
            channel.send(pwd+'\r\n')
            time.sleep(2)
            channel.send(pwd+'\r\n')
            time.sleep(2)

        while not channel.recv_ready():
            time.sleep(3)
        out = channel.recv(9999)
        print(out.decode("ascii"))

    def cmd(self, command, sudo=False):
        feed_password = False
        # if sudo and self.username != "root":
        if (sudo):  # (sudo != False)
            command = "sudo -S -p '' %s" % command
            feed_password = self.password is not None and\
                len(self.password) > 0
        stdin, stdout, stderr = self.ssh.exec_command(command)
        if feed_password:
            stdin.write(self.password + "\n")
            stdin.flush()
        # return {'out': stdout.readlines(),
        #         'err': stderr.readlines(),
        #         'retval': stdout.channel.recv_exit_status()}
        # stdin, stdout, stderr = client.exec_command\
        #         ("/var/mylongscript.py", get_pty=True)
        b = stderr.readlines()
        if b:
            for i in b:
                print(i)
        a = stdout.readlines()
        if a:
            for i in a:
                print(i)


def sshAutomationcompilationcheck():
    return True

if __name__ == '__main__':
    print('starting ' + __name__)
    instal1 = Devstack(ip, username, password)
    instal1.cmd('ls -al')
    instal1.local_conf(file_name, data_local)
    print('stoping')
