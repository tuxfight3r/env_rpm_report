#!/usr/bin/env python
#Purpose to find the unique/common packages between 2 ansible inventory hosts
#This script needs a similar inventory file with the same group names
#Date: 10/03/2016
#Author: Mohan Balasundaram

import json
import sys
import pprint
import datetime

from common_libs import *

#set the below parameter to False to include common packages in report
exclude_common=True

if len(sys.argv) != 4:
    usageExit()

#get the environment and file/folder paths for env
file1, file2 = sys.argv[1], sys.argv[2]
env1=sys.argv[1].split("/")[1]
env2=sys.argv[2].split("/")[1]
project1, env1_path=env1.split("_")
project2, env2_path=env2.split("_")
#print project1, env1_path, project2, env2_path
slevel=sys.argv[3]

#print "you are comparing %s->%s and %s->%s" % (env1, os.path.basename(file1), env2, os.path.basename(file2) )

#read the group hashes per env
env1_hash=json.loads(getGroupsFromInventory(sys.argv[1]))
env2_hash=json.loads(getGroupsFromInventory(sys.argv[2]))
global_sort={}

for group in sorted(env1_hash.iterkeys()):
    #print "Checking group: " , group
    global_sort.update({group:{}})
    try:
        for var1, var2 in zip( sorted(env1_hash[group].keys()), sorted(env2_hash[group].keys())):
            #print var1, var2
            outfile1="%s_%s_%s_rpmlist.log" % (env1_path,project1,var1)
            outfile2="%s_%s_%s_rpmlist.log" % (env2_path,project2,var2)
            #print outfile1, outfile2
            hostkey=var1+"_"+var2
            global_sort[group].update({hostkey:{}})

            #created empty arrays inside hostkey
            for env in "env1_array", "env2_array", "env_common":
                global_sort[group][hostkey][env]=[]

            #python logic to read 2 files and parse the array
            file1 = "%s/%s" % (env1_path, outfile1)
            file2 = "%s/%s" % (env2_path, outfile2)
            #print file1, file2

            try:
                with open (file1,'r') as infile1, open(file2,'r')as infile2:
                    list1=[line.strip('\n')for line in infile1.readlines()]
                    list2=[line.strip('\n')for line in infile2.readlines()]
            except IOError as e:
                if not os.path.isfile(file1):
                    filename=file1
                    list1="Reading Failed: %s<br>Check File: %s" % (e.strerror,filename)
                    list1=list1.split('\n')
                elif not os.path.isfile(file2):
                    filename=file2
                    list2="Reading Failed: %s<br>Check File: %s" % (e.strerror,filename)
                    list2=list2.split('\n')
                else:
                    pass

                #list "Reading Failed: %s.Check Files: %s" % (e.strerror,filename)

            (env1_array, env2_array, env_common) = compareArrayDiff(list1, list2)
            global_sort[group][hostkey]["env1_array"]=env1_array
            global_sort[group][hostkey]["env2_array"]=env2_array
            global_sort[group][hostkey]["env_common"]=env_common

    except:
       print "No Common Groups Found, Exiting.."
       sys.exit(2)


#    break
#final_hash=pprint.pprint(global_sort,indent=1,width=2)

#Generate HTML Report

PROJ1=project1.upper() + "->" + env1_path.upper()
PROJ2=project2.upper() + "->" + env2_path.upper()
TITLE="RPM Comparision Between " + PROJ1 + " and " + PROJ2 + " Hosts - " + slevel.upper()

#write the report
file_name="reports/"+slevel.upper()+"_"+project1+"_"+env1_path+"-"+env2_path +"_"+str(datetime.date.today()) + ".html"
print "Report is stored in " + file_name
openfile=open(file_name,"w")
parsed_output_html=generateHtmlReport(TITLE,PROJ1,PROJ2,global_sort,exclude_common)
openfile.write(parsed_output_html)
openfile.close()


