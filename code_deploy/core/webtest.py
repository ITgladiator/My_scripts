#!/usr/bin/env python
# encoding:utf-8

import urllib
import urllib2
import cookielib
import re
import sys


def login(hosturl, posturl, postData_dic):
    # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    # 打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功
#    h = urllib2.urlopen(hosturl)

    # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
               'Referer': hosturl}

    # 构造post数据，从抓取的包中分析得出
    postData = postData_dic

    # 需要给post数据编码
    postData = urllib.urlencode(postData)

    # 通过urllib2提供的request方法向指定url发送构造的数据完成登录
    request = urllib2.Request(posturl, postData, headers)
#    print request
    try:
        response = urllib2.urlopen(request, timeout=3)
    except urllib2.URLError:
        print "\033[31;1mLogin failed,Please check the url\033[0m"
        sys.exit()
#    text = response.read()
#    print text


# -------------获取网页内容--------------
def get_content(test_url, keyword):
    # 打开连接
    try:
        wp = urllib2.urlopen(test_url, timeout=3)
    except urllib2.URLError:
        print "\033[31;1mWeb test failed,Please check the url\033[0m"
        sys.exit()

    # 获取网页内容
    content = wp.read()

    # 查找页面内容是否包含需要的关键字
    result = re.findall(keyword, content)
    return len(result)


def deploy_test(hosturl, posturl, post_data, test_url, keyword):
    # 模拟登陆网站测试是否能正常访问
    login(hosturl, posturl, post_data)
    match_result = get_content(test_url, keyword)
    if match_result == 0:
        print "\033[31;1mERROR! Web test failed!\033[0m"
    else:
        print "\033[32;1mOK! Web test sucessfull!\033[0m"
