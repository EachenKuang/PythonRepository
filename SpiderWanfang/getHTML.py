# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import urllib2
import csv
import re
import random
import time
import sys
import datetime
import logging
reload(sys)
sys.setdefaultencoding("utf-8")

def spide(url):
    list = {}
    proxy = '112.120.87.20:443'
    opener = urllib2.build_opener(urllib2.ProxyHandler({'socks': proxy}))
    urllib2.install_opener(opener)
    # url='http://www.baidu.com/s?wd=intitle:%s+site:%s'%(name,url)
    request = urllib2.Request(url)
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
                   (KHTML, like Gecko) Element Browser 5.0',
                   'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                   'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                   'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                   'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
                   Version/6.0 Mobile/10A5355d Safari/8536.25',
                   'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
                   Chrome/28.0.1468.0 Safari/537.36',
                   'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
    index = random.randint(0, 9)
    user_agent = user_agents[index]
    request.add_header('User-Agent', user_agent)
    try:
        html = urllib2.urlopen(request, timeout=120)
    except urllib2.URLError, e:
        print(e)
        return False
    else:
        text = html.read()
        bs = BeautifulSoup(text, "html.parser")
        h3 = bs.title
        print h3


def test():
    txt_file = open('urls.txt', 'r')
    urls = txt_file.readlines()
    txt_file.close()
    # read the url that should be visit in the next time
    txt_file = open('paper_num.txt', 'r')
    paper_th = int(txt_file.readline())
    txt_file.close()
    # create file
    csv_file = open('relation.csv', 'a')
    x = paper_th - 1
    while x < len(urls):
        spide(x)

# test()


import urllib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

html = getHtml("http://d.g.wanfangdata.com.cn/Periodical_ytctyy201405041.aspx")

print html