#encoding=utf8
import urllib
import socket
from MyLog import Logger
def test():
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
            res = urllib.urlopen(url, proxies=proxy).read()
            of.write(proxy_host)
            print res, proxy
        except Exception,e:
            print proxy
            print e
            continue
    f.close()
    of.close()

# print u'\u8d5f'.encode('utf-8')
# # 赟
# print u'\u79a4'.encode('utf-8')
# # 禤
# print u'\u769e'.encode('utf-8')
# # 皞
# print u'\u9ec3'
# # 黃
# print u'\u6a11'
# # 樑
# print u'\u5f22'
# # 弢
# print u'\u79a4'
# # 禤
# print u'\u764e'
# # 癎
# for i in range(20):
#     with open('data/' + str(i + 1) + '/paper_num.txt', 'r') as r:
#         print r.readline()
# for i in range(20):
#     with open('data/'+str(i+1)+'/paper_num.txt','w') as w:
#         w.write('0')
# for i in range(20):
#     with open('data/' + str(i + 1) + '/paper_num.txt', 'r') as r:
#         print r.readline()

# logger = Logger(logname='log.txt', loglevel=1, logger="hahah").getlog()
#
# # try:
# #     open('/path/to/does/not/exist', 'rb')
# # except (SystemExit, KeyboardInterrupt):
# #     raise
# # except Exception, e:
# #     logger.error('Failed to open file', exc_info=True)
#
#
# logger.info("This is level 1 info log")
# logger.error("This is an error")
