# -*- coding:utf8 -*-
import requests
import re
import time
import urllib2
from bs4 import BeautifulSoup
of = open('proxy1.txt', 'w')
url = 'http://www.haodailiip.com/guonei/'
for i in range(1,20):
    Url = 'http://www.kuaidaili.com/free/intr/' + str(i)+'/'
    # Url = 'http://www.haodailiip.com/guonei/' + str(i)
    print "正在采集"+Url
    html = requests.get(Url)
    bs = BeautifulSoup(html, "html.parser")
    print bs
    table = bs.find("table")
    print table
    tr = table.findAll('tr')
    for i in range(1,31):
        td = tr[i].findAll('td')
        proxy_ip = td[0].text.strip()
        proxy_port = td[1].text.strip()
        of.write('%s:%s\n' %(proxy_ip,proxy_port))
        print '%s:%s\n' %(proxy_ip,proxy_port)
    time.sleep(2)
of.closed