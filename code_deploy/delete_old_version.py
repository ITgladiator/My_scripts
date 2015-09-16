#!/usr/bin/env python
# encoding:utf-8

import commands
import sys
from conf import setting

host = "10.10.10.30"
user = "root"
prod_tmp = setting.deploy_config["prod_tmp"]
log_file = setting.log_file

cmd_ls = "ssh " + user + "@" + host + " ls " + prod_tmp + "|awk -F '_' '{print $3}'|sort -n |uniq"

f = file(log_file, 'r')
v_str = ""

for i in f.readlines():
    v_str = i

f.close()

v_now = int(v_str)

status, values = commands.getstatusoutput(cmd_ls)
v_list = values.split("\n")

# 只保留当前版本和上一个版本
if len(v_list) <= 2:
    print "Nothing to do, exit!"
    print v_list
    sys.exit()
else:
    v_list.remove(str(v_now))
    print v_list
    max = 0
    for i in v_list:
        if int(i) > max:
            max = int(i)
    v_list.remove(str(max))
    for value in v_list:
        cmd = "ssh " + user + "@" + host + " mv " + prod_tmp + "/" + "*_" + value + "_* /tmp/"
        print cmd
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            print "OK, the old version moved sucessfull"
        else:
            print "ERROR!"
