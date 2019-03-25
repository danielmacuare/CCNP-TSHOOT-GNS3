#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint, pformat
from nornir import InitNornir
import argparse
import yaml
import logging
import sys


def sect_header(title):
    """
    Prints a section header with the title being passed
    """
    print("#" * 70)
    print(title)
    print("#" * 70)

def yaml_to_str(yaml_filename):
    """
    Takes a yaml_filename (str) from the input/ dir and a string
    """
    with open('input/' + yaml_filename, 'r') as f:
        yaml_str = f.read()
    return yaml_str

def yamlstr_to_python(yamlstr):
    """
    Takes a yaml string (yamlstr) and returns a python data structure
    """
    python_struc = yaml.load(yamlstr, Loader=yaml.FullLoader)
    return python_struc

def gen_config(yaml_file, jinja_templ, cfg_file='output.cfg'):
    """
    Combine a Yaml file with a Jinja template and renders a config file.
    The Yaml must be in the inputs/ directory relative to the script
    The Jinja template must be in the templates/ directory relative to the script.
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

def log_args(args):
    """"
    args = parser.parse_args()
    Takes the args object and logs the parameters passed by the user.
    """
    logger.debug('CLI-PASSED ARGS: ' + str(args))


# Parsing arguments
parser = argparse.ArgumentParser(description='''Takes a values file (.yaml) along with a Jinja template (.j2) \ 
    and returns a config file''')

# Required ARGS
req_args = parser.add_argument_group('required named arguments')
req_args.add_argument('--values', '-v', type=str, required=True,
                      help='input the path to the values template i.e "values.yaml"')

req_args.add_argument('--template', '-t', type=str, required=True,
                      help='input the path to the Jinja template i.e "template.j2"')

# Optional ARGS
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


if __name__ == "__main__":
    print(args)
    print(type(args))
    gen_config(args.values, args.template)

    print(args.debug)
    if args.debug:
        log_args(args)
        yamlstr = yaml_to_str(args.values)
        sect_header('YAML')
        print (yamlstr)
        sect_header('PYTHON')
        python_yaml = yamlstr_to_python(yamlstr)
        pprint(python_yaml)

    sys.exit()
