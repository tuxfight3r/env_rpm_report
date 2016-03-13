#!/bin/bash
#pass the right DC variable to identify identical environments in different DC's
./compare_inventory.py inventory/project1_prod/inventory inventory/project1_preprod/inventory DC
