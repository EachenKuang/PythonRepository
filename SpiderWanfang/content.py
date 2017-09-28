# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import random
import time
import sys
import csv
from MyLog import Logger
reload(sys)
sys.setdefaultencoding("utf-8")


NUM = 20
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


class url2Content(object):
    """
    This class's main work is to return each single paper's content base on the parameter(url)
    """
    def __init__(self, url):
        self.url = url
        try:
            # agent set
            index = random.randint(0,len(USER_AGENTS)-1)
            headers = {'User-Agent': USER_AGENTS[index]}
            request = urllib2.Request(self.url, headers=headers)
            response = urllib2.urlopen(request, timeout=100)
            self.content = response.read()
            self.soup = BeautifulSoup(self.content, "html.parser")
            # self.span = self.soup.find(
            #     class_="fixed-width-wrap fixed-width-wrap-feild")
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def get_id(self):
        """
        获得唯一标志符号
        :return:
        """
        self.id = self.url[self.url.find('_')+1:self.url.find('.as')]
        return self.id

    def get_title(self):
        """
        标题
        :return:
        """
        rows = self.soup.find('h1')
        title = rows.get_text().strip()
        title = title.encode("utf-8")
        self.title = title
        return self.title

    def get_doi(self):
        """
        获取doi
        :return:
        """
        doi = ''
        try:
            rows = self.soup.find('dl', id="doi_dl").find('dd').find('a')
            doi = rows.get_text()
            doi = doi.encode("utf-8")
        except:
            doi=''
        self.doi = doi
        return doi

    def get_author(self):
        """
        获取作者以及作者编号
        :return:
        """
        author_tag = self.soup.find_all('td', class_='author_td')[0]
        # get author's name array
        author = author_tag.find_all('a')
        # get author's num array
        num = author_tag.find_all('sup')

        # result is a string used to storage name+num
        result = ""
        for x in range(0, len(author)):
            author_num = num[x].get_text()
            author_name = author[x].get_text().strip()
            author_name = author_name.encode("utf8")
            result += author_name + author_num + ";"
        self.author = result
        return self.author

    def get_author_employer(self):
        """
        This function main work is to storage the author's employer
        """
        # try:
        result = ""
        try:
            s = '作者单位'.decode('utf-8')
            rows = self.soup.find(text=re.compile(s)).parent.parent.find_next_sibling()
            # print rows.get_text()
            # print rows.find_all('li')
            if rows.find_all('li').__len__() < 1:
                result = '[1]'+rows.get_text().strip()
                # print result
            else:
                rows = rows.find_all('li')
                for index, item in enumerate(rows):
                    temp = item.get_text().strip()
                    temp = temp.encode("utf8")
                    result += "[" + str(index+1) + "]" + temp + ";"
            self.employer = result
        except:
            result = ""
        return result

    def get_journal_name(self):
        """
        期刊
        :return:
        """
        result = ''
        try:
            rows = self.soup.find('table').find_all('tr')[3]
            result = rows.find('a').get_text().strip()
            result = result.encode("utf8")
            self.journal_name = result
        except:
            result = ''
        return result

    def get_year_paper(self):
        """
        年、卷、（期）
        :return:
        """
        result = ''
        # rows = self.soup.find('table').find_all('tr')[5]
        # rows = self.soup.find(re.compile('年，卷(期)'.__str__()))
        try:
            s = '年，卷\(期\)'.decode('utf-8')
            result = self.soup.find(text=re.compile(s)).parent.parent.find_next_sibling()
            result = result.find('a').text
            self.year = result.split(',')[0].strip()
            self.volume = result.split(',')[1].split('(')[0].strip()
            self.period = result.split(',')[1].split('(')[1][:-1].strip()
        except:
            return '','',''
        return self.year, self.volume, self.period

    def get_class_num(self):
        """
        分类号
        :return:
        """
        result = ''
        try:
            s = '分类号'.decode('utf-8')
            rows = self.soup.find(text=re.compile(s)).parent.parent.find_next_sibling()
            # rows = self.soup.find('table').find_all('tr')[6]
            result = rows.get_text().strip().replace('\r','').replace('\n','')
        except:
            result = ''
        self.classific_num = result
        return result

    def get_keyword(self):
        """
        关键字
        :return:
        """
        try:
            s = '关键词：'.decode('utf-8')
            rows = self.soup.find(text=re.compile(s)).parent.parent.find_next_sibling()
            # rows = self.soup.find('table').find_all('tr')[7]
            keywords = rows.find_all(href=re.compile(
                "http://s.g.wanfangdata.com.cn/Paper.aspx"))
            result = ""
            for keyword in keywords:
                keyword = keyword.get_text().strip()
                a = keyword.encode("utf-8")
                result += a + ";"
            self.keyword = result
        except:
            result = ''
        return result


def agent_set():
    # set proxy
    f = open('proxy_temp.txt')
    lines = f.readlines()
    proxys = []
    for i in range(0, len(lines) - 1):
        ip = lines[i].strip("\n")
        proxy = {"http": ip}
        proxys.append(proxy)
    # take proxy from proxy_temp.txt by random
    m = random.randint(0, (len(lines) - 2))
    proxy = proxys[m]
    # print proxy
    enable_proxy = True
    proxy_handler = urllib2.ProxyHandler(proxy)
    null_proxy_handler = urllib2.ProxyHandler({})
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
    urllib2.install_opener(opener)

def solve(input_str=''):
    """
    解决'gb2312' codec can't encode character u'\xa0'问题
    :param input_str:
    :return:
    """
    input_str = input_str.replace(u'\xa0', u'\x20')
    return input_str

def main():

    logger = Logger(logname='data/' + str(NUM) + '/log.txt', loglevel=1, logger="Eachen").getlog()
    logger.info('this is a level 1 log')
    # read the url that should be visit in the next time
    txt_file = open('data/'+str(NUM)+'/urls.txt', 'r')
    lines = txt_file.readlines()
    txt_file.close()
    # read the url that should be visit in the next time
    txt_file = open('data/'+str(NUM)+'/paper_num.txt', 'r')
    paper_th = int(txt_file.readline())
    txt_file.close()
    False_num = 0
    x = paper_th - 1

    # while x < len(lines):
    sup = [2694,5553]
    for x in sup:
        try:
            # x += 1

            # 从文件中解析出已经存储的 cite_count、journal_rank
            url = lines[x].split(';')[0]
            cite_count = lines[x].split(';')[1]
            optional_journal = lines[x].split(';')[-1].strip('\n')

            parser_conten = url2Content(url)

            # get infomation
            paper_id = parser_conten.get_id()
            title = parser_conten.get_title()
            doi = parser_conten.get_doi()
            author = parser_conten.get_author()
            employer = parser_conten.get_author_employer()
            journal_name = parser_conten.get_journal_name()
            keyword = parser_conten.get_keyword()
            class_num = parser_conten.get_class_num()
            y, v, p = parser_conten.get_year_paper()

            row = [paper_id, cite_count, optional_journal, title, doi, author, employer, journal_name, keyword, class_num, y, v, p]

            with open('data/'+str(NUM)+'/sup.csv','ab+') as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow(row)
                csvfile.close()


            logger.info("sucess:"+url+' '+str(x))
            False_num = 0
            # stroage the page num in cscfile
            # txt_file = open('data/'+str(NUM)+'/paper_num.txt', 'w')
            # txt_file.write(str(x))
            # txt_file.close()
            # delayed access to avoid the ip be shield
            time.sleep(5)
            # if x % 10 == 0:
            #     agent_set()
        except Exception, e:
            # agent_set()
            False_num += 1
            if False_num > 3:
                # agent_set()
                x -= False_num - 1
                False_num = 0
            # print e, x
            logger.error('fail:'+ url + ' err:' + str(e) + ' line:'+ str(x))
            continue


def test():
    # txt_file = open('urls.txt', 'r')
    # urls = txt_file.readlines()
    # txt_file.close()
    # agent_set()
    url = "http://d.g.wanfangdata.com.cn/Periodical_zgyf201521016.aspx"
    url = "http://d.g.wanfangdata.com.cn/Periodical_shzjzz201602010.aspx"
    url = "http://d.g.wanfangdata.com.cn/Periodical_zhwcyxzz201601010.aspx"
    url = "http://d.g.wanfangdata.com.cn/Periodical_syxnfxgbzz201508040.aspx"
    url = "http://d.g.wanfangdata.com.cn/Periodical_shandyy201405042.aspx"
    # url = "http://d.g.wanfangdata.com.cn/Periodical_syxnfxgbzz201508040.aspx"
    # url = "http://d.g.wanfangdata.com.cn/Periodical_ytctyy201405041.aspx"
    a = url2Content(url)
    title = a.get_title()
    doi = a.get_doi()
    author = a.get_author()
    employer = a.get_author_employer()
    journal_name = a.get_journal_name()
    key_word = a.get_keyword()
    classific_num = a.get_class_num()
    y,v,p = a.get_year_paper()

    print title
    # print cite_count
    print doi
    print author
    print employer
    print journal_name
    print key_word
    print classific_num
    print y,v,p
    # for x in range(200, len(urls)):
    #     url = urls[x]
    #     a = url2Content(url)
    #     # get infomation
    #     title = a.get_title()
    #     employer = a.get_author_employer()
    #     keyword = a.get_keyword()
    #     author = a.get_author()
    #     print title + "\n", employer + "\n", keyword + "\n", author
    #     # print author
    #     time.sleep(0.5)

# test()
if __name__ == '__main__':
    main()


