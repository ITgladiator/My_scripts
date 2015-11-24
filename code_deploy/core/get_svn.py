#!/usr/bin/env python
# coding:utf-8

import commands


def get_ver(svn_dir):
    cmd_get_ver = "cd %s && svn info|grep Revision|awk '{print $2}'" % svn_dir
    status, ver = commands.getstatusoutput(cmd_get_ver)
    if status == 0:
        return ver
    else:
        return -1


def get_code(dst_dir, svn_url, svn_user, svn_pass, svn_ver=None):
    if svn_ver is None:
        cmd_get_code = "cd %s && svn co %s --username=%s --password=%s" % (dst_dir, svn_url, svn_user, svn_pass)
    else:
        cmd_get_code = "cd %s && svn co -r %d %s --username=%s --password=%s" % (dst_dir, svn_ver, svn_url, svn_user, svn_pass)
    status, output = commands.getstatusoutput(cmd_get_code)
    return status


#if __name__ == "__main__":
#    get_code("/Users/gladiator/deploy/code", "svn://192.168.1.221/cms", "deploy", "x..18610876365..")
#    print get_ver("/Users/gladiator/deploy/code/cms")