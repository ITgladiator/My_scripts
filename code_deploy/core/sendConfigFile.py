#!/usr/bin/env python
# encoding:utf-8

import commands
import re


def sendConfig(nodeName, siteName):
    cmd = "salt \'" + nodeName + "\' state.sls " + siteName + "_config." + siteName + "_config env=prod"
    status, result = commands.getstatusoutput(cmd)
    a = re.findall("Failed:    0", result)
    if len(a) != 0:
        print "\033[33;1mOK! Send the config file sucessfull!\033[0m"
    else:
        print "\033[31;1mERROR! Send the config file failed!\033[0m"


if __name__ == "__main__":
    sendConfig("linux-node3", "cms")
