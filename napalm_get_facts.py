#!/usr/bin/python3.6
from napalm import get_network_driver
from pprint import pprint
driver = get_network_driver('ios')
optional_args = {'transport': 'telnet', 'secret': 'ccnplab'}
host = 'OOB-SW'
user = 'danielmac'
passwd = 'ccnplab'


device = driver(hostname=host, username=user, password=passwd, optional_args=optional_args)


device.open()
pprint(device.get_facts())
#pprint(device.get_interfaces_counters())
device.close()
