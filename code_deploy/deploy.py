#!/usr/bin/env python
# encoding:utf-8

import sys
import os
import time
import commands
import my_tar
import get_svn
import setting
import shutil
import send_file
import webtest
from multiprocessing import Process, Pool

log_file = setting.log_file
web_root = setting.deploy_config["web_root"]  # 远端服务器的web根目录

login_url = setting.webtest_config["login_url"]
post_url = setting.webtest_config["post_url"]
post_data = setting.webtest_config["post_data"]
test_url = setting.webtest_config["test_url"]
keyword = setting.webtest_config["keyword"]


def usage():
    print "Usage: " + sys.argv[0] +" [deploy | rollback-list | rollback-pro host ver]"


if len(sys.argv) < 2:
    usage()
    sys.exit()

elif sys.argv[1] == "deploy":
    # 从svn服务器checkout code 到本地
    dst_dir = setting.deploy_config["svn_checkout_dir"]  # checkout的目录
    svn_url = setting.svn_config["svn_url"]  # svn地址
    svn_user = setting.svn_config["svn_user"]  # svn用户名
    svn_pass = setting.svn_config["svn_pass"]  # svn密码
    svn_library = setting.svn_config["svn_library"]

    print "\033[33;1mbegin svn checkout...\033[0m"
    # 执行svn命令co代码
    status = get_svn.get_code(dst_dir, svn_url, svn_user, svn_pass)
    if status == 0:
        print "\033[32;1mSvn checkout sucessfull\033[0m"
    else:
        print "\033[31;1mSvn checkout ERROR!\033[0m"
        sys.exit()

    # 复制到临时目录并改名
    deploy_tmp_dir = setting.deploy_config["deploy_tmp"]  # 临时目录
    src_dir = dst_dir + "/" + svn_library  # 需要复制的目录，即svn co出得代码目录
    env = setting.deploy_config["env"]  # 部署环境（test、prod等）
    time_stamp = time.strftime("%Y-%m-%d-%H-%M")  # 时间
    svn_ver_status = get_svn.get_ver(src_dir)  # 当前版本库版本号（svn info）
    if svn_ver_status != -1:
        svn_ver = str(svn_ver_status)
        try:
            f = file(log_file, "w")
            f.write(svn_ver)
            f.close()
        except:
            print "\033[31;1mCan not write to the log file\033[0m"
            print "\033[31;1mThe current version will to deploy is %s\033[0m" % svn_ver
    else:
        print "\033[31;1mERROR! Get svn ver Failed!\033[0m"
        sys.exit()

    # 重命名后的目录名：prod_cmd_123_2015-08-02
    code_dir = env + "_" + svn_library + "_" + svn_ver + "_" + time_stamp
    tar_dir = deploy_tmp_dir + "/" + code_dir
    print "src_dir = %s" % src_dir
    print "tar_dir = %s" % tar_dir
    shutil.copytree(src_dir, tar_dir)  # 复制目录并重命名

    # 打包代码目录
    print "\033[33;1mbegin tar...\033[0m"
    status, tar_filename = my_tar.get_tar(tar_dir, deploy_tmp_dir)
    full_tar_filename = deploy_tmp_dir + "/" + tar_filename
    if status == 0:
        print '''\033[32;1mOK! The codes tar sucessfull!
Filename : %s\033[0m''' % full_tar_filename
    else:
        print "\033[31;1mERROR! The codes tar failed!\033[0m"
        sys.exit()

    # 发送打包文件到目标服务器，并解压做软连接
    hosts_list = setting.host_config["hosts_list"]
    port = setting.host_config["port"]
    user = setting.host_config["user"]
    pkey_file = setting.host_config["pkey_file"]
    prod_tmp = setting.deploy_config["prod_tmp"]
    dst_filename = prod_tmp + "/" + tar_filename
    print "\033[33;1mbegin send, untar file and make soft_link...\033[0m"


    # 定义发送文件、解压文件、删除已有软链接和创建新软链接的方法
    def send_untar_mksl(host, port, user, pkey_file, full_tar_filename, dst_filename, untar_cmd, rm_sl_cmd, sl_cmd):
        status = send_file.sendfile(host, port, user, pkey_file, full_tar_filename, dst_filename)
        if status == 0:
            print "\033[32;1mOK! Send file to %s sucessfull!\033[0m" % host
            untar_status, untar_result = commands.getstatusoutput(untar_cmd)
            if untar_status == 0:
                print "\033[32;1mOK! Untar file on %s sucessfull!\033[0m" % host
                try:
                    os.popen(rm_sl_cmd)
                except:
                    pass
                sl_status, sl_result = commands.getstatusoutput(sl_cmd)
                if sl_status == 0:
                    print "\033[32;1mOK! Make soft_link on %s sucessfull!\033[0m" % host
                else:
                    print "\033[31;1mERROR! Make soft_link on %s failed!\033[0m" % host 
            else:
                print "\033[31;1mERROR! Untar file on %s failed!\033[0m" % host
        else:
            print "\033[31;1mERROR! Send file to %s failed!\033[0m" % host

    sl_src = prod_tmp + "/" + code_dir  # 需要做软链接的目录
    sl_dst = web_root + "/" + svn_library  # 软链接位置：/data/website/cms
    pool = Pool(processes=4)
    result_list = []
    for host in hosts_list:
        sl_cmd = "ssh " + user + "@" + host + " ln -s " + sl_src + " " + sl_dst  # 创建软链接命令
        rm_sl_cmd = "ssh " + user + "@" + host + " rm -f " + sl_dst  # 删除已有软链接的命令
        untar_cmd = 'ssh ' + user + '@' + host + ' "' + 'cd ' + prod_tmp + ' && tar zxf ' + tar_filename + '"'
        result = pool.apply_async(send_untar_mksl, [host, port, user, pkey_file, full_tar_filename, dst_filename, untar_cmd, rm_sl_cmd, sl_cmd])
        result_list.append(result)
    for r in result_list:
        r.get()


# ========================================================================================================
        # Upload 目录和 data目录为用户上传的文件目录，放在web根目录，软链接到程序目录
        dir_list = ["Upload", "data"]
        for ln_dir in dir_list:
            sl_cmd = "ssh " + user + "@" + host + " ln -s " + web_root + "/" + ln_dir + " " + sl_dst + "/"
            rm_sl_cmd = "ssh " + user + "@" + host + " rm -rf " + sl_dst + "/" + ln_dir
            try:
                os.popen(rm_sl_cmd)
            except:
                pass
            os.popen(sl_cmd)
# ========================================================================================================

    webtest.deploy_test(login_url, post_url, post_data, test_url, keyword)

    print "*****************************\033[32;1m END \033[0m*****************************"

elif sys.argv[1] == "rollback-list":
    hosts_list = setting.host_config["hosts_list"]
    user = setting.host_config["user"]
    prod_tmp = setting.deploy_config["prod_tmp"]
    for host in hosts_list:
        ls_cmd = "ssh " + user + "@" + host + " ls " + prod_tmp + " | grep -v 'tar.gz'"
        ls_status, ls_result = commands.getstatusoutput(ls_cmd)
        if ls_status == 0:
            print '''
\033[32;1mHost: %s \033[0m
%s
            ''' % (host,ls_result)
        else:
            print "\033[31;1mERROR! Ls failed!\033[0m"

elif len(sys.argv) == 4 and sys.argv[1] == "rollback-pro":
    host = sys.argv[2]
    code_ver = sys.argv[3]
    get_curr_ver_cmd = "echo " + code_ver + " | awk -F '_' '{print $3}' "
    c_status, curr_ver = commands.getstatusoutput(get_curr_ver_cmd)
    user = setting.host_config["user"]
    prod_tmp = setting.deploy_config["prod_tmp"]
    svn_library = setting.svn_config["svn_library"]
    sl_dst = web_root + "/" + svn_library
    rollback_cmd = "ssh " + user + "@" + host + " ln -s " + prod_tmp + "/" + code_ver + " " + web_root + "/" + svn_library
    rm_sl_cmd = "ssh " + user + "@" + host + " rm -f " + sl_dst
    try:
        os.popen(rm_sl_cmd)
    except:
        pass
    r_status, r_ruslt = commands.getstatusoutput(rollback_cmd)
    # ========================================================================================================
    # Upload 目录和 data目录为用户上传的文件目录，放在web根目录，软链接到程序目录
    dir_list = ["Upload", "data"]
    for ln_dir in dir_list:
        sl_cmd = "ssh " + user + "@" + host + " ln -s " + web_root + "/" + ln_dir + " " + sl_dst + "/"
        rm_sl_cmd = "ssh " + user + "@" + host + " rm -rf " + sl_dst + "/" + ln_dir
        try:
            os.popen(rm_sl_cmd)
        except:
            pass
        r2_status, r2_result = commands.getstatusoutput(sl_cmd)
    # ========================================================================================================
    if r_status == 0 and r2_status == 0:
        try:
            f = file(log_file, "w")
            f.write(curr_ver)
            f.close()
        except:
            print "\033[31;1mCan not write to the log file\033[0m"
        print "\033[33;1mBegin web test...\033[0m"
        webtest.deploy_test(login_url, post_url, post_data, test_url, keyword)
        print "\033[32;1mRollback sucessfull!\033[0m"
        print "\033[32;1mThe current version is %s\033[0m" % code_ver
    else:
        print "\033[31;1mERROR! Rollback failed!\033[0m"
else:
    usage()
