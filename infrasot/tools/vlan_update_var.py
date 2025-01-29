import sys
import os
import yaml
import subprocess
import jinja2
from jinja2 import Template
import pandas
import numpy as np
from suzieq.sqobjects import get_sqobject
from rich import print

old_yaml_path = "/drone/src/infrasot/archive/vlan_list_last_state.yml"
new_yaml_path = "/drone/src/infrasot/vlan_list.yml"
path_template = "/drone/src/ansible-material/template"
group_vars_path = "/tmp/ansible/"

def load_yaml_file(path):
    with open(path, 'r') as stream:
        dict = yaml.safe_load(stream)
    return dict

old_vlans = load_yaml_file(old_yaml_path)
new_vlans = load_yaml_file(new_yaml_path)

vlan_list_to_be_created = []
vlan_list_to_be_deleted = []

#Check if new vlans in vlan state are in the previous state :
for vlan in new_vlans["vlans_list"].keys():
    if vlan not in old_vlans["vlans_list"].keys():
        if vlan not in vlan_list_to_be_created:
            vlan_list_to_be_created.append(vlan)

#Check if old vlans in vlan state are still in the new state :
for vlan in old_vlans["vlans_list"].keys():
    if vlan not in new_vlans["vlans_list"].keys():
        if vlan not in vlan_list_to_be_deleted:
            vlan_list_to_be_deleted.append(vlan)

if (not vlan_list_to_be_created and not vlan_list_to_be_deleted):
    print ("No change")
else :
    print ("Following vlans should be created :",vlan_list_to_be_created)
    print ("Following vlans shoudl be deleted :",vlan_list_to_be_deleted)

vgf = jinja2.Environment(loader=jinja2.FileSystemLoader(path_template)).get_template('vlan_update.j2').render(vlans = vlan_list_to_be_created)
print (vgf)
f = open(group_vars_path+"Leaves.yaml",'w')
f.write(vgf)
f.close()
