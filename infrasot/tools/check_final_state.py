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

yaml_path = "/drone/src/infrasot/vlan_list.yml"

def load_yaml_file(path):
    with open(path, 'r') as stream:
        dict = yaml.safe_load(stream)
    return dict

vlans = load_yaml_file(yaml_path)

vlan_list_sot_not_fab = []
vlan_list_fab_not_sot = []
#Check if vlans in vlan state are configured on the fabric :
for vlan in vlans["vlans_list"].keys():
    #print ("Check vlan :"+str(vlan))
    vlans_suz = get_sqobject("vlan")().get(vlan=vlan).hostname
    if vlans_suz.empty:
        #print ("Vlan",str(vlan)," should be configured")
        if vlan not in vlan_list_sot_not_fab:
            vlan_list_sot_not_fab.append(vlan)
    #else:
        #print (vlans)

#Check if vlan in fabric are in vlan state
for vlan in get_sqobject("vlan")().get().vlan:
    if vlan not in vlans["vlans_list"].keys():
        #print ("Vlan",str(vlan)," should not be on fabric")
        if vlan not in vlan_list_fab_not_sot:
            vlan_list_fab_not_sot.append(vlan)

if (not vlan_list_sot_not_fab and not vlan_list_fab_not_sot):
    print ("Infra is up to date")
else :
    print ("Following vlans should be configured :",vlan_list_sot_not_fab)
    print ("Following vlans shoudl be deleted :",vlan_list_fab_not_sot)
    raise Exception ("Infra is not aligned with sot")
