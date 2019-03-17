#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader
from pprint import pprint
import yaml


def sect_header(title):
    """
    Prints a section header with the title being passed
    """
    print("#" * 40)
    print(title)
    print("#" * 40)


def yaml_to_python(yaml_file):
    """
    Takes a yaml_file (str) and returns the original string + a data strucuctur
    """
    with open(yaml_file, 'r') as f:
        yaml_str = f.read()
        python_data_strc = yaml.load(yaml_str, Loader=yaml.FullLoader)
    return (yaml_str, python_data_strc)


yaml_data, python_data = yaml_to_python("OOB-SW.yaml")
sect_header("ORIGINAL YAML")
print(yaml_data)


sect_header("CONVERTED TO --> PYTHON DATA STRUCTURE")
pprint(python_data)
