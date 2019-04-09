#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint, pformat
from nornir import InitNornir
from nornir.plugins.tasks.text import template_file
from nornir.plugins.tasks.networking import napalm_configure
from nornir.plugins.functions.text import print_title, print_result
from ansible.plugins.filter.ipaddr import ipaddr
import argparse
import yaml
import logging
import sys

'''
Usage
python config_gen.py -v test.yaml -t Routers.j2
python config_gen.py -v test.yaml -t Routers.j2 -f R1.cfg
python config_gen.py -v test.yaml -t Routers.j2 -f R1.cfg --debug

'''


def sect_header(title):
    """
    Prints a section header with the title being passed
    """
    print("#" * 70)
    print(title)
    print("#" * 70)

def save_config(generated_config, path):
    config_dir = 'output/'
    config_path = config_dir + path
    with open(config_path, 'w') as output:
        output.write(generated_config)
        print('\nThe config file has been created at: "{}"'.format(config_path))

def log_args(args):
    """"
    args = parser.parse_args()
    Takes the args object and logs the parameters passed by the user.
    """
    logger.debug('CLI-PASSED ARGS: ' + str(args))

def render_configs(task):
    """
    Nornir task to render device configurations from j2 templates.
    Args:
        task: nornir task object
    """
    filename = task.host["j2_template_file"]
    j2_filters = {'ipaddr': ipaddr}
    r = task.run(
        task=template_file,
        name='Base Template Configuration',
        template=filename,
        path='ansible/templates',
        jinja_filters=j2_filters,
        **task.host,
    )
    task.host['config'] = r.result

def get_facts_manually(task):
    optional_args = { 'transport': 'telnet', 'port': 23 }
    task.host.open_connection("napalm",
                              configuration=task.nornir.config,
                              platform='ios',
                              extras=optional_args
                              )
    r = task.run(napalm_get, getters=['facts'])
    task.host.close_connection("napalm")
    print_result(r)

# Parsing arguments
parser = argparse.ArgumentParser(description='''Takes a values file (.yaml) along with a Jinja template (.j2) \ 
    and returns a config file''')

# Required ARGS
req_args = parser.add_argument_group('required named arguments')
req_args.add_argument('--values', '-v', type=str, 
                      help='input the path to the values template i.e "values.yaml"')

req_args.add_argument('--template', '-t', type=str, 
                      help='input the path to the Jinja template i.e "template.j2"')

# Optional ARGS
parser.add_argument('--filename', '-f', type=str,
                    help='This option saves a config file to output/<filename>.cfg')

# When the --debug option is used, args.parse will return True because of action='store_true'
parser.add_argument('--debug', default=False, action='store_true',
                    help='This option writes debug statements to ./config_gen.log')

parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

# Enabling logging
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

# Working with R2 only.    
    r2 = norn.filter(mgmt_ip='192.168.1.135/24')
    render_task = r2.run(task=get_facts_manually)
    print_result(render_task)

# Working with Routers only.    
#    routers = norn.filter(dev_type='Router')
#    render_task = routers.run(task=render_configs)

#    print_result(render_task)

# Inventory filters
#    routers = norn.filter(dev_type='Router').inventory.hosts.keys()
#    switches = norn.filter(dev_type='Switch').inventory.hosts.keys()

# Others
#    inv_hosts = norn.inventory.hosts
#    inv_hosts_values = norn.inventory.hosts.values()
#    inv_groups = norn.inventory.groups
#    inv_groups_values = norn.inventory.groups.values()
#    pprint(inv_groups)
#    pprint(inv_groups.keys())
#    pprint(inv_groups.values())
#    print(type(inv_groups)) 


# Working with all devices
#    render_task = norn.run(task=render_configs)
#    print_result(render_task)
    sys.exit()
