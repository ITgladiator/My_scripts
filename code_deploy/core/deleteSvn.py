#!/usr/bin/env python

import commands


def del_svn_info(source_dir):
    if source_dir != "/":
        cmd = "find " + source_dir + " -type d -name \.svn | xargs rm -rf"
        print cmd
        status, result = commands.getstatusoutput(cmd)
        if status == 0:
            print "\033[32;1mOK,the '.svn' delete sucessfull!\033[0m"
        else:
            print "\033[31;1mError! Please delete '.svn' by yourself\033[0m"
    else:
        print "\033[31;1mYou want to excute 'rm -rf /'? Do not be stupid!\033[0m"
