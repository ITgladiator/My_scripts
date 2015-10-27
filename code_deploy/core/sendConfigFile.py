#!/usr/bin/env python
# encoding:utf-8

import commands
import re


def sendConfig(nodeName, siteName):
    cmd = "salt '%s' state.sls %s_config.%s_config env=prod" % (nodeName, siteName, siteName)
    status, result = commands.getstatusoutput(cmd)
    a = re.findall("Failed:    0", result)
    if len(a) != 0:
        print "\033[32;1mOK! Send the config file to %s sucessfull!\033[0m" % nodeName
    else:
        print "\033[31;1mERROR! Send the config file to %s failed!\033[0m" % nodeName


if __name__ == "__main__":
    sendConfig("linux-node3", "cms")
