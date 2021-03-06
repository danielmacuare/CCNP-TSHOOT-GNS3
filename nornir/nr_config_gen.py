#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint, pformat
from nornir import InitNornir
from nornir.core.filter import F
from ansible.plugins.filter.ipaddr import ipaddr
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks.files import write_file
from nornir.plugins.tasks.text import template_file
from nornir.plugins.tasks.networking import napalm_configure, napalm_get
import argparse
import yaml
import logging
import sys
import ipdb

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

def log_args(args):
    """"
    args = parser.parse_args()
    Takes the args object and logs the parameters passed by the user.
    """
    logger.debug('CLI-PASSED ARGS: ' + str(args))

def render_configs(task):
    """
    Nornir task to render device configurations from j2 templates and write it
    to the output/ folder
    Args:
        task: nornir task object
    """
    filename = task.host["j2_template_file"]
    j2_filters = {'ipaddr': ipaddr}
    res = task.run(
        task=template_file,
        name='Base Template Configuration',
        template=filename,
        path='../ansible/templates',
        jinja_filters=j2_filters,
        **task.host)
    config = res.result
    hostname = task.host.name
    write_to_file(content=config, hostname=hostname)
    

def write_to_file(content: str, hostname: str, output_dir='output/') -> None:
    """Writes the content to a file based on the hostname & output_dir

    Parameters
    __________
    config: str
        The content that will be written to the file
    hostname: str
        The hostname that will the used to name the file.
    output_dir: str
        The dir where you want to output the file (default='output/')
    """
     
    filename = output_dir + hostname + '.conf'
    with open(filename, 'w' ) as wf:
        wf.write(content)
    print(f'Config for: {hostname} - Has been written to: {filename}')


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
    nr = InitNornir(config_file='config.yaml')
    #nr = InitNornir(config_file='config.yaml', core={'num_workers': 1})

    #common filters
    routers = nr.filter(F(groups__contains='Routers'))
    switches = nr.filter(F(groups__contains='Switches'))
    r1_r2 = nr.filter(F(hostname='r1') | F(hostname='r2'))
    r2_simple = nr.filter(hostname='r2')

    #Unfiltered task
    rend_conf = nr.run(task=render_configs)

    #Filtered task
    #filter_inv = routers
    #rend_conf = filter_inv.run(task=render_configs)
    
    print_result(rend_conf)
    
    sys.exit()
