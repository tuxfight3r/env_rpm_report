RPM Comparison Report Between 2 Environments
======

Overview
------
This script will generate a RPM comparision report between 2 similar Environments
like (prod/preprod) based on thier ansible inventories. The report will display
what packages are unique in the two machines compared and whats common between them.

**Note: This script will not work if you have mismatching group names in the ansible inventories.**

###Report Screenshot
![alt text][screenshot]

[screenshot]:
https://github.com/tuxfight3r/env_rpm_report/raw/master/reports/demo_screen.png
"Report Screenshot"

[Checkout the demo page
here](http://htmlpreview.github.io/?https://github.com/tuxfight3r/env_rpm_report/blob/master/reports/DC_project1_prod-preprod_2016-03-14.html)

PreRequisites
------
* Ansible with Jinja2
* Python2.6+
* Bash

Usage
------
The script works in 2 parts:

1. Run the ansible script provided against the needed inventory to collect the data and store it locally
2. Run the python script to analyze the data collected and generate the report.

##Configuration
Edit the provided `fetch_rpmlist.yml` file and update the folder path. update
it to the folder where you are running this script from. your data files will be
stored under this folder in thier corresponding environment directory. ex: prod
for production data.
```
folder_path: "/home/ansible_user/env_rpm_report"
```
The script by default ignores the common packages available in both machines
from the report, if you are interested in viewing it please change the
file `compare_inventory.py` and set the option `exclude_common=False`.

##Inventory Setup
To add new inventory please create the folder structure like as shown below
```
project_environment
#for example project1_prod/inventory 

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
The folder has to be named `project_environment` as the logic is used in
generating multiple reports. 

##Collecting Data
use `fetch_rpmlist_project1.sh` as template and create a script to suit your
project/Environment name. please update the project variable and environment variable in
that script to reflect your environment. The script assumes you have key based
auth setup from the machine where you are trying to collect the data from, if
not pass -k option to the ansible command and it will prompt for password.

```bash
#!/bin/bash

####PROJECT1####

#PROJECT1 PREPROD
echo "Running PROJECT1 PREPROD"
#add -k at the end to prompt for password
ansible-playbook -i inventory/project1_preprod/inventory fetch_rpmlist.yml -e
"env_var=preprod project=project1" -vv --diff

#PROJECT1 PROD
echo "Running PROJECT1 PROD"
#add -k at the end to prompt for password
ansible-playbook -i inventory/project1_prod/inventory fetch_rpmlist.yml -e
"env_var=prod project=project1" -vv --diff

```

Once you run that script, ansible will collect the data and store the files locally on the machine
under the right environment folder.
For example: we are comparing prod/preprod so check prod/preprod folder and it should look like below
```bash
prod/
├── prod_project1_prj1prapp01_rpmlist.log
├── prod_project1_prj1prapp02_rpmlist.log
├── prod_project1_prj1prlban01_rpmlist.log
├── prod_project1_prj1prlban02_rpmlist.log
├── prod_project1_prj1prngnx01_rpmlist.log
├── prod_project1_prj1prngnx02_rpmlist.log
├── prod_project1_prj1prpgdb01_rpmlist.log
└── prod_project1_prj1prpgdb02_rpmlist.log

preprod/
├── preprod_project1_prj1ppapp01_rpmlist.log
├── preprod_project1_prj1ppapp02_rpmlist.log
├── preprod_project1_prj1pplban01_rpmlist.log
├── preprod_project1_prj1pplban02_rpmlist.log
├── preprod_project1_prj1ppngnx01_rpmlist.log
├── preprod_project1_prj1ppngnx02_rpmlist.log
├── preprod_project1_prj1pppgdb01_rpmlist.log
└── preprod_project1_prj1pppgdb02_rpmlist.log

```
The files are prefixed with environment/project/hostname so the data can be identified properly.

##Generating Reports
Create a script similar to the provided `DC_generate_project1_report.sh` to suit
your environment/project settings
```bash
##DC_generate_project1_report.sh 
#!/bin/bash
./compare_inventory.py inventory/project1_prod/inventory inventory/project1_preprod/inventory DC

```
pass the 2 inventories for which you have collected data and it should generate the
report under the reports folder. As you can see below it has generated
`DC_project1_prod-preprod_2016-03-13.html` file, similarly you should see a
report for your project/environment/DC value.

```
reports/
├── cuscosky.css
├── DC_project1_prod-preprod_2016-03-13.html
├── demo_screen.png
└── start_webserver.sh
```

you can either copy it along with the css provided to a webserver and view
it from there or run the `./start_webserver.sh` and it will start a simple 
python webserver on port 8000 from which you can view the generated report.

##Troubleshooting
you can view what groups are seen by the compare inventory script by passing
the inventories directly to the `common_libs.py`

```json
./common_libs.py inventory/project1_prod/inventory 
{
    "appservers": {
        "prj1prapp01": "192.168.1.130", 
        "prj1prapp02": "192.168.1.131"
    }, 
    "dbservers": {
        "prj1prpgdb01": "192.168.1.180", 
        "prj1prpgdb02": "192.168.1.181"
    }, 
    "loadbalancers": {
        "prj1prlban01": "192.168.1.10", 
        "prj1prlban02": "192.168.1.11"
    }, 
    "webservers": {
        "prj1prngnx01": "192.168.1.65", 
        "prj1prngnx02": "192.168.1.66"
    }
}
```
it takes one inventory as input and shows the groups it sees and both the inventories
you are passing to the main script should have identical groups.

###Todo
* Extend support for other automation tools if possible



