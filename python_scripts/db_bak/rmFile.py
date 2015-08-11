#!/usr/bin/env python
import os
import datetime

def rmFile(bakdir, date_now, interval):
    files = os.listdir(bakdir)
    for filename in files:
        fileDate = filename.split('_')[3]
        t = (date_now - datetime.datetime.strptime(fileDate, "%Y-%m-%d")).days
        if t >= interval:
            try:
                os.chdir(bakdir)
                os.remove(filename)
                print filename
            except:
                print "ERROR"

