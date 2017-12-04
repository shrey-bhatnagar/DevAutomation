#!/usr/bin/env python

from __future__ import print_function
from oslo_config import cfg


opt_appdata_group = cfg.OptGroup(name='appdata',
                         title='app configuration')
appdata_opts = [
    cfg.StrOpt('enable', default=False, help=('True enables, False disables')),
    cfg.StrOpt('ip', default='0.0.0.0', help=('IP address of remote VM where we need to install Dev-Stack')),
    cfg.StrOpt('username', default='root', help=('Username for telnet')),
    cfg.StrOpt('password', default='root', help=('password for login')),
    cfg.StrOpt('file_name', default='local.conf', help=('filename')),
    cfg.StrOpt('devUser', default='stack', help=('non root user for devstack')),
    cfg.StrOpt('devUserPwd', default='root', help=('password for devsuer'))#,
    #cfg.ListOpt('data_local', default='default data', help=('data for local.conf')),
    #cfg.StrOpt('data_local1', default='default data', help=('data for local.conf'))
]

def register_opt_group(conf, opt_group, options):
    conf.register_group(opt_group)
    for opt in options:
        conf.register_opt(opt, group=opt_group.name)

def register_opts():
    register_opt_group(cfg.CONF, opt_appdata_group, appdata_opts)

def get_config():
    cfg.CONF(default_config_files=['myapp.conf'])
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
    #print(CONF.appdata.data_local)
    #print(CONF.appdata.data_local1)

if __name__ == '__main__':
    shrey()






















"""
opt_simple_group = cfg.OptGroup(name='simple',
                         title='A Simple Example')

opt_morestuff_group = cfg.OptGroup(name='morestuff',
                         title='A more complex Example')

opt_shrey_group = cfg.OptGroup(name='shrey',
                          title='a shreys example')

shrey_opts = [
    cfg.StrOpt('msg',default='Name',help=('a name will be displayed'))        
]


#############

simple_opts = [
    cfg.BoolOpt('enable', default=False,
                help=('True enables, False disables'))
]
 
morestuff_opts = [
    cfg.StrOpt('message', default='no data',
                help=('A message')),
    cfg.ListOpt('usernames', default=None,
                help=('A list of usernames')),
    cfg.DictOpt('usermetadata', default=None,
                help=('A dictionary of usernames and job title')),
    cfg.IntOpt('payday', default=30,
                help=('Default payday of month')),
    cfg.FloatOpt('pi', default=0.0,
                help=('The value of Pi'))
]


################
CONF = cfg.CONF
CONF.register_group(opt_simple_group)
CONF.register_opts(simple_opts, opt_simple_group)
CONF.register_group(opt_morestuff_group)
CONF.register_opts(morestuff_opts, opt_morestuff_group)
CONF.register_group(opt_shrey_group)
CONF.register_opts(shrey_opts,opt_shrey_group)
 
 
if __name__ == "__main__":
    CONF(default_config_files=['app.conf', 'app2.conf'])
    print(CONF.simple.enable)
    print(CONF.morestuff.message)

    print('(morestuff) usernames: {}'.format(CONF.morestuff.usernames))
    print(CONF.shrey.msg)




--------------------------------------------
"""

'''
def group(myname, mytitle):
    #opt_group = cfg.OptGroup(name='shrey',title='a shreys example')
    opt_group = cfg.OptGroup(name=myname,title=mytitle)
    return opt_group

def opts(content, name, helpstr):
    #shrey_opts = [cfg.StrOpt('msg',default='Name',help=('a name will be displayed'))]
    shrey_opts = [cfg.StrOpt(content,default=name,help=(helpstr))]


def regg():
    register_opt_group(cfg.CONF, myopt_group, mysimple_opts)
    
"""
    myopt_group = group('shrey','my example shrey code')
    mysimple_opts = opts('msg','Name','a name will be displayed')
    cfg.CONF.register_group(myopt_group)
    cfg.CONF.register_opts(mysimple_opts, myopt_group)
"""

def main():
    #CONF = cfg.CONF
    cfg.CONF(default_config_files=['app.conf', 'app2.conf'])
    regg()
    return CONF

CONF = cfg.CONF

if __name__ == "__main__":
    my_conf = main()
    #CONF = cfg.CONF
    #CONF(default_config_files=['app.conf', 'app2.conf'])
    print(my_conf.simple.enable)
    print(my_conf.morestuff.message)

    print('(morestuff) usernames: {}'.format(my_conf.morestuff.usernames))
    print(my_conf.shrey.msg)
'''    
