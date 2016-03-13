#!/usr/bin/python
#This script acts as a common library script for the main script
#Date: 10/03/2016
#Author: Mohan Balasundaram


import sys
import re
import json
import os

from jinja2 import Environment, FileSystemLoader
 

def getGroupsFromInventory(ansible_inventory_file):

    #Get groups from inventory file and add it to array. 
    cat_hosts_file = open(ansible_inventory_file).readlines()
    groups_list = {}

    for line in cat_hosts_file:
        # Skip comments & empty lines
        line = line.strip()
        if not line or line.startswith('#'):
            continue
  
        if line.startswith('['): # group
            group = re.sub(r'[\[\]]', '', line)
            groups_list[group] = {}
        elif "ansible_ssh_host" in line:
            host_var = re.split(r'[\t," "]+',line)
            hostname = host_var[0].split(".")[0]
            #logic to accomodate ansible inventory with aliases
            ip_var = [item for item in host_var if "ansible_ssh_host" in item]
            ip=ip_var[0].split("=")[1]
            #print hostname, ip
            groups_list[group].update({hostname: ip})

    #delete empty groups from dictionary         
    for k,v in groups_list.items():
        if not groups_list[k]:
            groups_list.pop(k)
     
    #Print output in json format.
    return json.dumps(groups_list,indent=4, sort_keys=True)

def usageExit():
    print """
    NOTE: program needs 3 parameters 2 similar ansible inventories and DataCenterID
    Usage: ./compare_inventory.py inventory/idam_prod/elevated inventory/idam_preprod/elevated UKDC

    HELP: This program compares 2 Identical ansible inventories and checks the rpms installed in the
          hosts in the same group and generates a html report under reports directory.
          The script wont work if you have mismatching groups in inventories.
    """
    sys.exit(2)


def generateHtmlReport(title, env1, env2,global_sort,exclude_common):
    THIS_DIR=os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
    return j2_env.get_template('template.html').render(title=title,environment1=env1, environment2=env2, hash=global_sort, commonpkgs=exclude_common)



if __name__ == "__main__":
    print getGroupsFromInventory(sys.argv[1])
