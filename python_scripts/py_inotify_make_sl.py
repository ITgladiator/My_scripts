#!/usr/bin/env python
# encoding:utf-8
# 监控目录创建操作，在创建的目录里创建软链接，前提该目录下只会创建目录


import pyinotify
import commands

wm = pyinotify.WatchManager()
mask = pyinotify.IN_CREATE
ln_dir_list = ["/data/website/cms/data/html/public/js", "/data/website/cms/data/html/public/css", "/data/website/cms/data/html/public/img"]
error_log = "/var/log/cms_make_ln.log"


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        # print "Creating:",event.pathname
        fullname = event.pathname
        for ln_dir in ln_dir_list:
            cmd = "ln -s " + ln_dir + " " + fullname
            status, result = commands.getstatusoutput(cmd)
            if status == 0:
#                print "ln ", ln_dir, " to ", fullname, " sucessfull"
                pass
            else:
                f = file(error_log, "a")
                message = "DIR: " + fullname + " make ln " + ln_dir + " failed!"
                f.write(fullname)
                f.close()

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch("/data/website/cms/data/html", mask, rec=False)
while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break
