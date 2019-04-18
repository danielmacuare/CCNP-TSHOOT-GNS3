#!/usr/bin/python3.6
from napalm import get_network_driver
from pprint import pprint
driver = get_network_driver('ios')
conn_method = {'transport': 'telnet'}
host = 'r2'
user = 'danielmac'
passwd = 'ccnplab'

#device = driver(hostname=host, username=user, password=passwd, optional_args=conn_method)
#
#print('Connecting to the device')
#device.open()
#
#print('Getting facts')
#pprint(device.get_facts())
##pprint(device.get_interfaces_counters())
#
#print('Closing the connection')
#device.close()


# With context manager
with driver(hostname=host, username=user, password=passwd, optional_args=conn_method) as device:
    
    print('Getting facts')
    pprint(device.get_facts())
    #pprint(device.get_interfaces_counters())

    print('\nUsing a context Manager. Python will handle opening and closing the connection')
