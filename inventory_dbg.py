#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint, pformat
from nornir import InitNornir
import argparse
import yaml
import logging
import sys 


def log_args(args):
    """"
    args = parser.parse_args()
    Takes the args object and logs the parameters passed by the user.
    """
    logger.debug('CLI-PASSED ARGS: ' + str(args))


def log_hosts(inv_hosts):
    """"
    norn = InitNornir(config_file='nornir_config.yaml')
    inv_hosts = norn.inventory.hosts
    Takes the dictionary-like object  of inv_hosts and logs it.
    """
    logger.debug("HOSTS AVAILABLE: \n" + pformat(inv_hosts))

def log_groups(inv_groups):
    """"
    norn = InitNornir(config_file='nornir_config.yaml')
    inv_groups = norn.inventory.groups
    Takes the dictionary-like object of inv_groups and logs it.
    """
    logger.debug("GROUPS AVAILABLE: \n" + pformat(inv_groups))

def log_inherited_values(in_host_values):
    """
    norn = InitNornir(config_file='nornir_config.yaml')
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
    logger.debug(log_string)


#PARSING ARGUMENTS
parser = argparse.ArgumentParser(description='''Takes a values file (.yaml) along with a Jinja template (.j2) \
    and returns a config file''')

# Optional ARGS
parser.add_argument('--hosts', '-d', type=str,
                    help='input the path to the hosts file i.e "hosts.yaml"')

parser.add_argument('--groups', '-g', type=str,
                    help='input the path to the groups file i.e "groups.yaml"')

# When the --debug option is used, args.parse will return True because of action='store_true'
parser.add_argument('--debug', default='None', action='store_true',
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
    norn = InitNornir(config_file='nornir_config.yaml')

    inv_hosts = norn.inventory.hosts
    inv_hosts_values = norn.inventory.hosts.values()
    inv_groups = norn.inventory.groups
    inv_groups_values = norn.inventory.groups.values()

    if args.debug:
        log_args(args)
        log_hosts(inv_hosts)
        log_groups(inv_groups)
        log_inherited_values(inv_hosts_values)
    sys.exit()
