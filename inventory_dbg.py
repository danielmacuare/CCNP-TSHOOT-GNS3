#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint, pformat
from nornir import InitNornir
import argparse
import yaml
import logging
import sys 
import ipdb

"""
Usage
python inventory_dbg.py --debug
python inventory_dbg.py --children switch
python inventory_dbg.py --filter device=router

"""

def log_args(args):
    """"
    args = parser.parse_args()
    Takes the args object and logs the parameters passed by the user.
    """
    logger.info('CLI-PASSED ARGS: ' + str(args) + '\n')


def log_hosts(inv_hosts):
    """"
    norn = InitNornir(config_file='config.yaml')
    inv_hosts = norn.inventory.hosts
    Takes the dictionary-like object of inv_hosts and logs it.
    """
    logger.info("HOSTS AVAILABLE: \n" + pformat(inv_hosts) + '\n')

def log_groups(inv_groups):
    """"
    norn = InitNornir(config_file='config.yaml')
    inv_groups = norn.inventory.groups
    Takes the dictionary-like object of inv_groups and logs it.
    """
    logger.info("GROUPS AVAILABLE: \n" + pformat(inv_groups))

def log_hosts_per_group(inv_groups_keys):
    """"
    norn = InitNornir(config_file='config.yaml')
    inv_groups_keys = norn.inventory.groups.keys()
    Takes the groups from inv_groups_keys and logs the children of the groups (set).
    """
    logger.info('HOSTS PER GROUPS:')
    for group in inv_groups_keys:
        logger.info('Children of the "' + group + '":')
        hosts_in_group = norn.inventory.children_of_group(group)
        logger.info(pformat(hosts_in_group))

def log_inherited_values(in_host_values):
    """
    norn = InitNornir(config_file='config.yaml')
    host_list = norn.inventory.host.values()
    Takes a host_list and returns all the values inherited by each host.
    """
    log_title = 'INHERITED VALUES:\n'
    log_output = []
    log_output.append(log_title)
    for devices in inv_hosts_values:
        host = 'Host: ' + str(devices)
        values = 'Values: ' + str(devices.items())
        log_line = host + '\n' + values + '\n'
        log_output.append(log_line)
    log_string = ''.join(log_output)
    logger.info(log_string)


#PARSING ARGUMENTS
parser = argparse.ArgumentParser(description='''Takes a values file (.yaml) along with a Jinja template (.j2) \
    and returns a config file''')

# Optional ARGS
parser.add_argument('--hosts', '-d', type=str,
                    help='input the path to the hosts file i.e "hosts.yaml"')

parser.add_argument('--groups', '-g', type=str,
                    help='input the path to the groups file i.e "groups.yaml"')

parser.add_argument('--filter', '-f', type=str,
                    help='input the filter you want to apply  i.e "device=router"')

parser.add_argument('--children', '-c', type=str,
                    help='input the group and will return the children of the group.  i.e "switch"')

# When the --debug option is used, args.parse will return True because of action='store_true'
parser.add_argument('--debug', default=False, action='store_true',
                    help='This option writes debug statements to ./config_gen.log')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()


#ENABLING LOGGING 
timestamp = '%d-%m-%Y %H:%M:%S'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if args.debug == True else logging.INFO)

# Creates a file handler which logs debug events to a file
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                              timestamp)

log_path = 'logs/' + sys.argv[0] +'.log'
file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)

# create a console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Adds the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


if __name__ == "__main__":
    norn = InitNornir(config_file='config.yaml')

    inv_hosts = norn.inventory.hosts
    inv_hosts_values = norn.inventory.hosts.values()
    inv_groups = norn.inventory.groups
    inv_groups_values = norn.inventory.groups.values()
    inv_groups_keys= norn.inventory.groups.keys()

    if args.debug:
        log_args(args)
        log_hosts(inv_hosts)
        log_groups(inv_groups)
        log_hosts_per_group(inv_groups_keys)
        log_inherited_values(inv_hosts_values)

    if args.filter:
        print('The following devices match the filter: "{}"'.format(args.filter))
        print(norn.filter(device='router').inventory.hosts.keys())
    if args.children:
        print('The following devices are children of the group: "{}"'.format(args.children))
        pprint(norn.inventory.children_of_group(args.children))

    sys.exit()
