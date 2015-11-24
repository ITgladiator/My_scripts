#!/usr/bin/env python
# encoding:utf-8

import commands


def sendConfig(nodeName, siteName, env):
    cmd = "salt '%s' state.sls %s_config.%s_config env=%s" % (nodeName, siteName, siteName, env)
    status, result = commands.getstatusoutput(cmd)
    result_list = result.split('\n')
    for item in result_list:
        if "Failed" in item:
            item_list = item.split()
            if item_list[1] == '0':
                print "\033[32;1mOK! Send the config file to %s sucessfull!\033[0m" % nodeName
            else:
                print "\033[31;1mERROR! Send the config file to %s failed!\033[0m" % nodeName


if __name__ == "__main__":
    sendConfig("linux-node3", "cms")
