#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint
from nornir import InitNornir
import argparse
import yaml
import logging


def sect_header(title):
    """
    Prints a section header with the title being passed
    """
    print("#" * 70)
    print(title)
    print("#" * 70)


def yaml_to_python(yaml_file):
    """
    Takes a yaml_file (str) and returns the original string + a data strucuctur
    """
    with open(yaml_file, 'r') as f:
        yaml_str = f.read()
        python_data_strc = yaml.load(yaml_str, Loader=yaml.FullLoader)
    return (yaml_str, python_data_strc)

def yaml_jinja_conf(yaml_file, jinja_templ, cfg_file='output.cfg'):
    """
    Combine a Yaml file with a Jinja template and renders a config file.
    The template must be in the same directory than the script.
    """

    # Reading YAML and trasnforming it into a Python object
    with open('input/' + yaml_file) as f:
        input_values = yaml.load(f, Loader=yaml.FullLoader)

    # Defining Jinja Env + jinja template
    ENV = Environment(loader=FileSystemLoader('templates'), trim_blocks=True,
                      lstrip_blocks=True)
    template = ENV.get_template(jinja_templ)

    # Rendering the template
    config = template.render(input_values)

    # Writing config to a file
    with open(cfg_file, 'w') as output:
        output.write(config)
    
    print(config)    


#Parsing arguments
parser = argparse.ArgumentParser(description='''Takes a values file (.yaml) along with a Jinja template (.j2) \ 
    and returns a config file''')

parser.add_argument('--values', '-v', type=str,
                    help='input the path to the values template i.e "values.yaml"')


parser.add_argument('--template', '-t', type=str,
                    help='input the path to the Jinja template i.e "template.j2"')

# When the --debug option is used, args.parse will return True because of action='store_true'
parser.add_argument('--debug', default='None', action='store_true',
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

file_handler = logging.FileHandler('config_gen.log')
file_handler.setFormatter(formatter)

# create a console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Adds the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Returned values
logger.debug(args)

# PROGRAM
#yaml_jinja_conf('test.yaml', 'Routers.j2')
#yaml_data, python_data = yaml_to_python("OOB-SW.yaml")


norn = InitNornir(config_file='nornir_config.yaml')
#print(norn.config.core.num.workers)
#print(norn.inventory.hosts)
#print(norn.inventory.hosts['r2'])
#print(norn.inventory.groups)
#
#r2 = norn.inventory.hosts['r2']
#print(r2.keys())
#print(r2['domain'])
#
#r3 = norn.inventory.hosts['r3']
#print(r3['domain'])

#LOGGING
#sect_header("ORIGINAL YAML")
#print(yaml_data)
#sect_header("CONVERTED TO --> PYTHON DATA STRUCTURE")
#pprint(python_data)


