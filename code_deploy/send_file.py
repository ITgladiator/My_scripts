#!/usr/bin/env python
# encoding:utf-8

import paramiko


def sendfile(host, port, user, pkey_file, src_filename, dst_filename):
    try:
        s = paramiko.SSHClient()
        s.load_system_host_keys()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        t = paramiko.Transport((host, port))
        key = paramiko.RSAKey.from_private_key_file(pkey_file)
        t.connect(username=user, pkey=key)

        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(src_filename, dst_filename)
        s.close()
        status = 0
        return status
    except:
        status = -1
        return status



#if __name__ == "__main__":
#    sendfile("10.10.10.30",22,"root","/Users/gladiator/.ssh/id_rsa", "/Users/gladiator/deploy/tmp/prod_cms_1_2015-08-04-10-56.tar.gz", "/data/website/deploy_tmp/prod_cms_1_2015-08-04-10-56.tar.gz")