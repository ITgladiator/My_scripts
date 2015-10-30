#!/usr/bin/env python
# encoding:utf-8

import commands
import sys
from conf import setting


def usage():
    print "Usage: %s IP PROJECTNAME" % sys.argv[0]


if len(sys.argv) != 3:
    usage()
    sys.exit()

host = sys.argv[1]
projectName = sys.argv[2]
user = "root"
prod_tmp = setting.deploy_config["prod_tmp"]
log_file = "%s/%s_svn_ver.log" % (setting.log_dir, projectName)

cmd_ls = "ssh %s@%s ls %s | grep %s |awk -F '_' '{print $3}'|sort -n |uniq" % (user, host, prod_tmp, projectName)

f = file(log_file, 'r')
v_str = ""

for i in f.readlines():
    v_str = i

f.close()

v_now = int(v_str)

status, values = commands.getstatusoutput(cmd_ls)
v_list = values.split("\n")
print v_list

# 只保留当前版本和上一个版本
if len(v_list) <= 3:
    print "Nothing to do, exit!"
    print v_list
    sys.exit()
else:
    v_list.remove(str(v_now))
    # print v_list
    # max = 0
    # for i in v_list:
    #     if int(i) > max:
    #         max = int(i)
    # v_list.remove(str(max))
    for i in range(2):
        v_list.remove(max(v_list))
        print v_list
    for value in v_list:
        cmd = "ssh %s@%s mv %s/*_%s_%s_* /tmp/" % (user, host, prod_tmp, projectName, value)
        print cmd
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            print "OK, the old version moved sucessfull"
        else:
            print "ERROR!"
