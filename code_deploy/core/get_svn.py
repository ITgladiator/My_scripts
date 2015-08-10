#!/usr/bin/env python
# coding:utf-8

import commands


def get_ver(svn_dir):
    cmd_get_ver = "cd " + svn_dir + "&& svn info|grep Revision|awk '{print $2}'"
    status, ver = commands.getstatusoutput(cmd_get_ver)
    if status == 0:
        return ver
    else:
        return -1


def get_code(dst_dir, svn_url, svn_user, svn_pass):
    cmd_get_code = "cd " + dst_dir + "&& svn co " + svn_url + " --username=" + svn_user + " --password=" + svn_pass
    status, output = commands.getstatusoutput(cmd_get_code)
    return status


#if __name__ == "__main__":
#    get_code("/Users/gladiator/deploy/code", "svn://192.168.1.221/cms", "deploy", "x..18610876365..")
#    print get_ver("/Users/gladiator/deploy/code/cms")