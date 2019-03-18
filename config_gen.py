#!/usr/bin/python3.6
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint
import yaml


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
    with open(yaml_file) as f:
        input_values = yaml.load(f)

    # Defining Jinja Env + jinja template
    ENV = Environment(loader=FileSystemLoader('.'), trim_blocks=True)
    template = ENV.get_template(jinja_templ)

    # Rendering the template
    config = template.render(input_values)

    # Writing config to a file
    with open(cfg_file, 'w') as output:
        output.write(config)
    
    print(config)    


# PROGRAM
yaml_jinja_conf('OOB-SW.yaml', 'Initial-config.j2')
#yaml_data, python_data = yaml_to_python("OOB-SW.yaml")



#LOGGING
#sect_header("ORIGINAL YAML")
#print(yaml_data)
#sect_header("CONVERTED TO --> PYTHON DATA STRUCTURE")
#pprint(python_data)


