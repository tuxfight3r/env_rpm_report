#!/bin/bash

####PROJECT1####

#PROJECT1 PREPROD
echo "Running PROJECT1 PREPROD"
ansible-playbook -i inventory/project1_preprod/inventory fetch_rpmlist.yml -e "env_var=preprod project=project1" -vv --diff

#PROJECT1 PROD
echo "Running PROJECT1 PROD"
ansible-playbook -i inventory/project1_prod/inventory fetch_rpmlist.yml -e "env_var=prod project=project1" -vv --diff
