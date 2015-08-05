#!/usr/bin/env python
# encoding:utf-8

import urllib
import urllib2
import cookielib
import re
import sys


# 登录的主页面
hosturl = "http://crm.fcgtech.com/admin/public/login.html"
# post数据接收和处理的页面，向这个页面发送构造的post数据
posturl = "http://crm.fcgtech.com/admin/public/login.html?s=/Admin/public/login.html"

# 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# 打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功
h = urllib2.urlopen(hosturl)

# 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
           'Referer': hosturl}

# 构造post数据，从抓取的包中分析得出
postData = {
    'username': 'admin',
    'password': '111111',
    'verify': 'undefined',
}

# 需要给post数据编码
postData = urllib.urlencode(postData)

# 通过urllib2提供的request方法向指定url发送构造的数据完成登录
request = urllib2.Request(posturl, postData, headers)
print request
response = urllib2.urlopen(request, timeout=3)
text = response.read()
print text
if re.findall('jumpUrl', text):
    print "OK"
else:
    print "false"

# -------------获取网页内容--------------
# 要获取的网页地址
get_url = "http://192.168.1.2/crm/companion/index.html"

# 打开连接
try:
    wp = urllib2.urlopen(get_url, timeout=3)
except urllib2.URLError:
    print "Please check the url"
    sys.exit()

# 获取网页内容
content = wp.read()

# 查找页面内容是否包含需要的关键字
keyword = '项目'
result = re.findall(keyword, content)
if len(result) == 0:
    print 'Not match'
else:
    print 'OK'
    print keyword

