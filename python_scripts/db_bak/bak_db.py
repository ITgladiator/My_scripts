#!/usr/bin/env python
# encoding:utf-8
# mysql backup script
# by gc@20150723
################

import os,commands,datetime,sys
import rmFile
import time

bak_user = "backup"
bak_pass = "x..backup.123.."
ip = "112.126.64.212"
log_file = "/var/log/db_bak.log"
vpn_script = "/server/scripts/vpn_connect.sh"

today = datetime.datetime.now()
date_now = today.strftime("%Y-%m-%d_%H%M%S")
bak_file_name = "bak_db_" + ip + "_" + str(date_now) + ".tar.gz"
bak_dir = "/server/backup/dbbak/"
fullbak_cmd = "/usr/bin/innobackupex --user=" + bak_user + " --password=" + bak_pass + " --stream=tar " + bak_dir + "|gzip>" + bak_dir + bak_file_name

rmFile.rmFile(bak_dir, today, 3)
#print fullbak_cmd
#sys.exit()

status,result = commands.getstatusoutput(fullbak_cmd)
bak_mess = "null"
send_mess = "null"
if status == 0:
    bak_mess = "DB bakcup sucessfull"
    rsync_cmd = "rsync -az " + bak_dir + bak_file_name + " rsync_backup@192.168.1.218::mysqlbak --password-file=/etc/rsync.password"
    s,r = commands.getstatusoutput(rsync_cmd)
    if s == 0:
        send_mess = "file send sucessfull"
    else:
        cmd_vpnconn = "/bin/sh " + vpn_script
        for i in range(3):
            os.popen(cmd_vpnconn)
            time.sleep(5)
            sn,rn = commands.getstatusoutput(rsync_cmd)
            if sn == 0:
                send_mess = "file send sucessfull"
                break
            else:
                send_mess = "file send failed"
else:
    bak_mess = "DB bakcup failed"

message = date_now + " | " + bak_mess + " | " + send_mess
f = file(log_file,"a")
f.write(message)
f.write('\n')
f.close()
