import sys
import os
import yaml
import subprocess
import jinja2
from jinja2 import Template

def load_yaml_file(path):
    with open(path, 'r') as stream:
        dict = yaml.safe_load(stream)
    return dict

vlans = load_yaml_file("../vlan_list.yml")

vlan_list = []

for key in vlans["vlans_list"].keys():
    print (key)
