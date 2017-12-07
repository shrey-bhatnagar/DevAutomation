#!/usr/bin/env python

from __future__ import print_function
from oslo_config import cfg


opt_appdata_group = cfg.OptGroup(name='appdata', title='app configuration')
appdata_opts = [
    cfg.StrOpt('enable', default=False, help=('True enables, False disables')),
    cfg.StrOpt('ip', default='0.0.0.0',
               help=('IP address of remote VM to install Dev-Stack')),
    cfg.StrOpt('username', default='root', help=('Username for telnet')),
    cfg.StrOpt('password', default='root', help=('password for login')),
    cfg.StrOpt('file_name', default='local.conf', help=('filename')),
    cfg.StrOpt('devUser', default='stack', help=('nonroot user for devstack')),
    cfg.StrOpt('devUserPwd', default='root', help=('password for devsuer'))
    # cfg.ListOpt('data_local', default='default data',
    # help=('data for local.conf')),
    # cfg.StrOpt('data_local1', default='default data',
    # help=('data for local.conf'))
]


def register_opt_group(conf, opt_group, options):
    conf.register_group(opt_group)
    for opt in options:
        conf.register_opt(opt, group=opt_group.name)


def register_opts():
    register_opt_group(cfg.CONF, opt_appdata_group, appdata_opts)


def get_config():
    cfg.CONF(default_config_files=['configration/myapp.conf'])
    register_opts()
    return cfg.CONF


def shrey():
    CONF = get_config()
    print('app!!!')
    print(CONF.appdata.enable)
    print(CONF.appdata.ip)
    print(CONF.appdata.username)
    print(CONF.appdata.password)
    print(CONF.appdata.file_name)
    print(CONF.appdata.devUser)
    print(CONF.appdata.devUserPwd)
    # print(CONF.appdata.data_local)
    # print(CONF.appdata.data_local1)


def appcompilationcheck():
    return True


if __name__ == '__main__':
    shrey()
