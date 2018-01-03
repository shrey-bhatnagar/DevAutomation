from keystoneauth1 import loading
from keystoneauth1 import session
import argparse
from novaclient import client as nova_client
import time
import os


AUTH_URL = 'http://192.168.195.182:5000/v3'
USERNAME = 'admin'
PASSWORD = 'openstack123'
PROJECT_NAME = 'demo'
USER_DOMAIN_NAME = 'Default'
PROJECT_DOMAIN_NAME = 'Default'
NOVA_API_VERSION = '2'


def get_creds():
    credentials = {'auth_url': AUTH_URL, 'username': USERNAME,
                   'password': PASSWORD, 'project_name': PROJECT_NAME,
                   'user_domain_name': USER_DOMAIN_NAME,
                   'project_domain_name':PROJECT_DOMAIN_NAME}
    return credentials


parser = argparse.ArgumentParser(description="VM name required")
parser.add_argument("--name", type=str, help="provide vm name")
args = parser.parse_args()

credentials = get_creds()

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(**credentials)
sess = session.Session(auth=auth)

nova = nova_client.Client(NOVA_API_VERSION, session=sess)

# If there are no keypairs creating the keypairs for the instance to boot with
if not nova.keypairs.findall(name="mykey"):
    BASE_DIR = os.path.dirname(os.path.abspath(os.getcwd()))
    PROJECT_DIR = os.path.join(BASE_DIR, '.ssh/')
    for root, directory, filenames in os.walk(PROJECT_DIR):

        if not filenames:
            os.system('test -f ~/.ssh/id_rsa.pub || ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa')

    with open(os.path.expanduser('~/.ssh/id_rsa.pub')) as my_ssh_key:
        nova.keypairs.create(name="testkey", public_key=my_ssh_key.read())


print(nova.servers.list())

image_store = nova.glance.find_image("cirros-0.3.4-x86_64-uec")
flavor_store = nova.flavors.find(name="m1.tiny")

#Create VM using minimum args in nova server create cmd
vm = nova.servers.create(name=args.name, image=image_store, flavor=flavor_store, key_name="testkey")

status = vm.status
# Poll at 5 second intervals, until the status is no longer 'BUILD'
while status=='BUILD':
    time.sleep(5)
    # Retrieve the instance again so the status field updates
    vm = nova.servers.get(vm.id)
    status = vm.status

#display the status of VM
print("VM is now: {}\n".format(status))

print('Network information is {}'.format(vm.networks))

# Updating the Security Group
security_group = nova.security_groups.find(name="default")
nova.security_group_rules.create(security_group.id, ip_protocol="tcp", from_port=22, to_port=22)
nova.security_group_rules.create(security_group.id, ip_protocol="icmp", from_port=-1, to_port=-1)

#output console information of newly created VM on screen
print(vm.get_console_output())