RPM Comparision Report Between 2 Environments
======

Overview
------
This script will generate a RPM comparision report between 2 similar Environments like (prod/preprod) based on thier ansible inventories.
**Note: This script will not work if you have mismatching group names in the inventories.**

PreRequisites
------
* Ansible with Jinja2
* python2.6+
* bash with coreutils installed

Usage
------
The script works in 2 parts:

1. Run the ansible script provided against the needed inventory to collect the data and store it locally
2. Run the python script to analyze the data collected and generate the report.

##setup
Edit the provided `fetch_rpmlist.yml` file and update the folder path. update
it to the folder where you are running this script from.
```
folder_path: "/home/ansible_user/rpm_comparison"
```

##Inventory Structure
To add new inventory please create the folder structure like as shown below
```
project_environment
#for example project1_prod/inentory 

#Sample inventory structure provided
inventory/
├── project1_preprod
│   └── inventory
├── project1_prod
│   └── inventory
├── project2_preprod
│   └── inventory
└── project2_prod
    └── inventory

```


