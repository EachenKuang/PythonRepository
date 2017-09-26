#encoding=utf8
import urllib
import socket
socket.setdefaulttimeout(0.5)
of = open('proxy_temp.txt', 'a')
f = open('proxy.txt')
lines = f.readlines()
# proxys = []
# for i in range(0,len(lines)):
#     ip = lines[i].strip("\n")
#     proxy_host = "http://"+ip
#     proxy_temp = {"http":proxy_host}
#     proxys.append(proxy_temp)
url = "http://ip.chinaz.com/getip.aspx"
for i in range(0,len(lines)):
    try:
        ip = lines[i].strip("\n")
        proxy_host = "http://"+ip
        proxy = {"http":proxy_host}
        proxy_host += "\n"
        res = urllib.urlopen(url,proxies=proxy).read()
        of.write(proxy_host)
        print res, proxy
    except Exception,e:
        print proxy
        print e
        continue
f.close()
of.close()