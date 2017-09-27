# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.8.17
# Goal: 万方爬虫
# Other:
# '''
from bs4 import BeautifulSoup
import urllib2
import urllib

NUM = 20
CONTENT = "作者单位%3a(宝安区人民医院%2b宝安区中医医院%2b宝安区中医院%2b宝安人民医院%2b宝安中医医院%2b宝安中医院%2b北京大学附属深圳医院%2b北京大学深圳临床医学院%2b北京大学深圳医院%2b大鹏人民医院%2b福田妇幼保健院%2b福田区妇幼保健院%2b福田区中医医院%2b福田区中医院%2b福田人民医院%2b福田中医医院%2b福田中医院%2b福永人民医院%2b福永医院%2b观澜人民医院%2b光明新区人民医院%2b广东深圳宝安区慢病防治院%2b广东省深圳市龙华新区疾病预防控制中心预防保健门诊部%2b广东医学院附属福田医院)%20*%20Date%3a2012-2016&db=wf_qk"
# CONTENT = "作者单位%3a(广州中医药大学附属深圳医院%2b广州中医药大学深圳医院%2b横岗人民医院%2b横岗镇人民医院%2b华中科技大学深圳协和医院%2b暨南大学附属宝安妇幼保健院%2b龙岗第二人民医院%2b龙岗区第二人民医院%2b龙岗区第三人民医院%2b龙岗区人民医院%2b龙岗区中医院%2b龙岗人民医院%2b龙岗中医院%2b龙华区疾病预防控制中心%2b龙华新区中心医院%2b罗湖慢性病防治院%2b罗湖区慢性病防治医院%2b罗湖区慢性病防治院%2b罗湖区中医医院%2b罗湖区中医院%2b罗湖中医医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(罗湖中医院%2b南澳人民医院%2b南方医科大学附属深圳医院%2b南方医科大学深圳附属医院%2b南方医科大学深圳医院%2b南山区人民医院%2b南山人民医院%2b南山医院%2b坪山区人民医院%2b坪山人民医院%2b蛇口区人民医院%2b蛇口人民医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深联医院%2b深圳CDC%2b深圳宝安慢病医院%2b深圳宝安慢性病防治院%2b深圳宝安区慢性病防治院%2b深圳第八人民医院%2b深圳第二人民医院%2b深圳第六人民医院%2b深圳第三人民医院%2b深圳第十人民医院%2b深圳第四人民医院%2b深圳儿童医院%2b深圳福田区慢性病防治院%2b深圳福田医院%2b深圳妇幼保健院%2b深圳光明新区疾病预防控制中心%2b深圳恒生医院%2b深圳华侨医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳急救医疗中心%2b深圳急救中心%2b深圳疾病预防控制中心%2b深圳疾控中心%2b深圳精神卫生中心%2b深圳军龙医院%2b深圳流花医院%2b深圳龙城医院%2b深圳龙岗中心医院%2b深圳龙华区疾病预防控制中心%2b深圳罗湖医院%2b深圳慢性病防治中心%2b深圳平乐骨伤科医院%2b深圳市CDC%2b深圳市宝安Ⅸ慢性病防治院%2b深圳市宝安慢性病防治院%2b深圳市宝安区福永人民医院%2b深圳市宝安区妇幼保健院%2b深圳市宝安区疾病预防控制中心%2b深圳市宝安区慢病防治站)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳市宝安区慢病站%2b深圳市宝安区慢性病防治院%2b深圳市宝安区慢性病防治站%2b深圳市宝安区慢性病院%2b深圳市宝安区人民医院%2b深圳市宝安区沙井医院%2b深圳市宝安区石岩人民医院%2b深圳市宝安区松岗人民医院%2b深圳市宝安区西乡卫生监督所%2b深圳市宝安区中心医院%2b深圳市宝安区中医院%2b深圳市大鹏新区妇幼保健院%2b深圳市大鹏新区葵涌人民医院%2b深圳市大鹏新区南澳人民医院%2b深圳市第八人民医院%2b深圳市第二人民医院%2b深圳市第六人民医院%2b深圳市第七人民医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳市第三人民医院%2b深圳市第十人民医院%2b深圳市第四(福田)医院%2b深圳市第四人民医院%2b深圳市第四医院%2b深圳市儿科研究所%2b深圳市儿童医院%2b深圳市福田慢性病防治院%2b深圳市福田区妇幼保健院%2b深圳市福田区慢病防治院%2b深圳市福田区慢病院%2b深圳市福田区慢性病防治院%2b深圳市福田区慢性痛防治院%2b深圳市福田区人民医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳市福田区中医院%2b深圳市福田医院%2b深圳市妇幼保健院%2b深圳市光明新区疾病预防控制中心%2b深圳市光明新区疾控中心%2b深圳市光明新区人民医院%2b深圳市光明新区中心医院%2b深圳市恒生医院%2b深圳市急救医疗中心%2b深圳市急救中心%2b深圳市疾病预防控制中心%2b深圳市疾控中心%2b深圳市精神卫生中心%2b深圳市康宁医院%2b深圳市流花医院%2b深圳市龙岗区第二人民医院%2b深圳市龙岗区第三人民医院%2b深圳市龙岗区第五人民医院%2b深圳市龙岗区妇幼保健院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳市龙岗区骨科医院%2b深圳市龙岗区葵涌人民医院%2b深圳市龙岗区人民医院%2b深圳市龙岗区中医院%2b深圳市龙岗中心医院%2b深圳市龙华区疾病预防控制中心%2b深圳市龙华区精神卫生中心%2b深圳市龙华区慢性病防治中心%2b深圳市龙华新区疾病预防控制中心%2b深圳市龙华新区疾病预防控中心职业卫生科%2b深圳市龙华新区人民医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳市龙华新区中心医院%2b深圳市罗湖区妇幼保健院%2b深圳市罗湖区疾病预防控制中心%2b深圳市罗湖区慢性病防治院%2b深圳市罗湖区人民医院%2b深圳市罗湖区中医院%2b深圳市慢性病防治中心%2b深圳市南山区妇幼保健院%2b深圳市南山区慢性病防治院%2b深圳市南山区人民医院%2b深圳市南山区蛇口人民医院%2b深圳市坪山区妇幼保健院%2b深圳市坪山新区人民医院%2b深圳市人民医院%2b深圳市输血医学研究所%2b深圳市孙逸仙心血管医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳市围着床期生殖免疫重点实验室%2b深圳市卫生计生能力建设和继续教育中心%2b深圳市卫生局急救中心%2b深圳市西丽人民医院%2b深圳市西乡医院%2b深圳市血液中心%2b深圳市盐田区人民医院%2b深圳市眼科医院%2b深圳市医学继续教育中心%2b深圳市职业病防治院%2b深圳市中西医结合医院%2b深圳市中心医院%2b深圳市中医医院%2b深圳市中医院%2b深圳输血医学研究所%2b深圳特区福田区慢性病防治院%2b深圳血液中心%2b深圳眼科医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳眼科中心%2b深圳中山泌尿外科医院%2b深圳中山医科大学深圳泌尿外科医院%2b深圳中西医结合医院%2b深圳中心医院%2b深圳中医医院%2b深圳中医院%2b石岩人民医院%2b石岩医院%2b松岗区人民医院%2b松岗人民医院%2b卫生部临检中心病毒核酸检测联合实验室%2b香港大学深圳医院%2b盐田区人民医院%2b盐田区医院%2b盐田人民医院%2b盐田医人民医院%2b中国医学科学院肿瘤医院深圳医院%2b中南大学湘雅二医院深圳医院%2b中山大学第三医院附属深圳医院%2b中山大学附属第八医院%2b中山医科大学深圳泌尿外科医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(宝安*妇幼)%2b作者单位%3a(宝安*中心医院)%2b作者单位%3a(大鹏*妇幼)%2b作者单位%3a(广东医科大学*观澜*医院)%2b作者单位%3a(广东医学院*观澜*医院)%2b作者单位%3a(广东医学院*深圳市第三人民医院)%2b作者单位%3a(广州中医药大学*临床医学院*深圳)%2b作者单位%3a(广州中医药大学*深圳*医院)%2b作者单位%3a(华中科技大学*协和深圳医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(暨南大学*第二*临床学院)%2b作者单位%3a(暨南大学*第二*临床医学院)%2b作者单位%3a(暨南大学*第二*医院)%2b作者单位%3a(暨南大学*二附院)%2b作者单位%3a(暨南大学*二院)%2b作者单位%3a(暨南大学*深圳眼科中心)%2b作者单位%3a(军龙*医院)%2b作者单位%3a(龙岗*第三人民医院)%2b作者单位%3a(龙岗*第五*医院)%2b作者单位%3a(龙岗*妇幼)%2b作者单位%3a(龙岗*骨科医院)%2b作者单位%3a(龙华新区*医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(罗湖*妇幼)%2b作者单位%3a(罗湖*人民*医院)%2b作者单位%3a(南方医科大学*宝安医院)%2b作者单位%3a(南山*妇幼)%2b作者单位%3a(坪山新区*人民医院)%2b作者单位%3a(沙井*医院)%2b作者单位%3a(深大*妇女儿童医院)%2b作者单位%3a(深大*妇幼保健院)%2b作者单位%3a(深圳*宝安*疾病预防)%2b作者单位%3a(深圳*宝安*慢性病)%2b作者单位%3a(深圳*宝安*西乡*卫生监督)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳*宝安医院)%2b作者单位%3a(深圳*第九*医院)%2b作者单位%3a(深圳*东湖医院)%2b作者单位%3a(深圳*福田*慢病)%2b作者单位%3a(深圳*福田*慢性病)%2b作者单位%3a(深圳*福田区人民医院)%2b作者单位%3a(深圳*福田医院)%2b作者单位%3a(深圳*公明*医院)%2b作者单位%3a(深圳*光明*疾病)%2b作者单位%3a(深圳*光明*疾病预防控制中心)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳*光明*医院)%2b作者单位%3a(深圳*光明新区*妇幼保健院)%2b作者单位%3a(深圳*光明新区*中心医院)%2b作者单位%3a(深圳*华侨医院)%2b作者单位%3a(深圳*康宁医院)%2b作者单位%3a(深圳*葵涌人民医院)%2b作者单位%3a(深圳*龙城*医院)%2b作者单位%3a(深圳*龙岗区中心医院)%2b作者单位%3a(深圳*龙华*疾病)%2b作者单位%3a(深圳*龙华*疾控)%2b作者单位%3a(深圳*龙华*精神卫生)%2b作者单位%3a(深圳*龙华*卫生检验中心)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳*龙华*职业病防治中心)%2b作者单位%3a(深圳*龙华人民*医院)%2b作者单位%3a(深圳*罗湖区*慢性病*防治中心)%2b作者单位%3a(深圳*罗湖区公共卫生宣传教育中心)%2b作者单位%3a(深圳*罗湖区疾病预防控制中心)%2b作者单位%3a(深圳*慢性病*防治)%2b作者单位%3a(深圳*南山慢性病防治院)%2b作者单位%3a(深圳*南山区精神卫生中心)%2b作者单位%3a(深圳*南山区慢病防治医院)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳*南山区慢病防治院)%2b作者单位%3a(深圳*南山区慢病防治中心)%2b作者单位%3a(深圳*南山区慢性病防治医院)%2b作者单位%3a(深圳*南山区慢性病防治院)%2b作者单位%3a(深圳*南山区慢性病防治中心)%2b作者单位%3a(深圳*平湖*医院)%2b作者单位%3a(深圳*坪山*妇幼保健院)%2b作者单位%3a(深圳*坪山区妇幼保健院)%2b作者单位%3a(深圳*坪山新区妇幼保健院)%2b作者单位%3a(深圳*孙逸仙心血管病医院)%2b作者单位%3a(深圳*孙逸仙心血管医院)%2b作者单位%3a(深圳*血液病研究所)%2b作者单位%3a(深圳*职业病防治院)%2b作者单位%3a(深圳*中山*生殖免疫诊疗中心)%20*%20Date%3a2014-2016&db=wf_qk"
# CONTENT = "作者单位%3a(深圳*中西医结合老年病研究所)%2b作者单位%3a(深圳*肿瘤研究所)%2b作者单位%3a(深圳大学*第一*医院)%2b作者单位%3a(深圳大学*妇女儿童医院)%2b作者单位%3a(深圳大学*妇幼保健院)%2b作者单位%3a(深圳大学*一附院)%2b作者单位%3a(深圳大学*一院)%2b作者单位%3a(西丽*医院)%2b作者单位%3a(西乡*卫生监督所)%2b作者单位%3a(西乡人民医院*深圳)%2b作者单位%3a(中国医学科学院肿瘤医院*深圳医院)%2b作者单位%3a(中山*第三*深圳医院)%2b作者单位%3a(中山大学*深圳医院)%20*%20Date%3a2014-2016&db=wf_qk"

def str2num(string=""):
    sum_ = 0
    for x in string:
        if (x <= '9') & (x >= '0'):
            sum_ = sum_ * 10 + int(x)
    return sum_


# ===============================class===================================
class title2Url(object):
    """
    This class is uesd to get the result of the search keywords
    """

    def __init__(self, url):
        self.url = url
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = {'User-Agent': user_agent}
            request = urllib2.Request(self.url, headers=headers)
            response = urllib2.urlopen(request)
            self.content = response.read()
            self.soup = BeautifulSoup(self.content, "html.parser")
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print e.code
            if hasattr(e, "reason"):
                print e.reason

    def get_items_num(self):
        """
        This function is uesd to count the total num of the result of the search
        """
        num = self.soup.find(id="lefthitlist").span.span.text
        print num
        sum_ = str2num(num.encode("utf8"))
        self.sum_ = sum_
        return sum_

    def get_urls(self):
        urls_ = []
        urls = self.soup.find_all('ul', class_="list_ul", style="display: none;")
        # print urls[0].find_all('a')[1].get('href')
        for url in urls:
            temp = url.find_all('a')[1].get('href')
            urls_.append(temp.encode("utf8"))
        self.urls_ = urls_
        return urls_

    def get_cite_count(self):
        cite_count_ = []
        cite_counts = self.soup.find_all('span', class_="c_gray")
        for cite_count in cite_counts:
            temp = str2num(cite_count.get_text())
            cite_count_.append(temp)
        self.cite_count = cite_count_
        return cite_count_

    def get_option_journal(self):
        option_journal_ = []
        option_journals = self.soup.find_all('span', class_="HideInfo", title="精简模式")

        # print option_journals
        temp =''
        for option_journal in option_journals:
            try:
                temp1 = option_journal.parent.parent.find('span', title="被中信所《中国科技期刊引证报告》收录").get_text()
                temp2 = option_journal.parent.parent.find('span', title="被北京大学《中文核心期刊要目总览》收录").get_text()
                temp = temp1 + ',' + temp2
            except AttributeError:
                print AttributeError.message

            option_journal_.append(temp)
        self.option_journal = option_journal_
        return option_journal_


def first_visit(url):
    """
    This function main work is to storage the total num of the result
    """
    a = title2Url(url)
    # urls = a.get_urls()
    # cite_counts = a.get_cite_count()
    # option_journals = a.get_option_journal()
    # get the total num
    num = a.get_items_num()
    # storage the total num in cscfile
    txt_file = open('data/'+str(NUM)+'/total_num.txt', 'w')
    txt_file.write(str(num))
    txt_file.close()
    # storage the page num in cscfile
    txt_file = open('data/'+str(NUM)+'/now_visit.txt', 'w')
    txt_file.write("0")
    txt_file.close()

    # storage the fist visited urls
    # txt_file = open('data/'+str(NUM)+'/urls.txt', 'a')
    # print urls.__len__()
    # for url in urls:
    #     temp = url+'\n'
    #     txt_file.write(temp)
    #     print temp
    # txt_file.close()
    # storage the fist visited urls
    # txt_file = open('data/' + str(NUM) + '/urls.txt', 'a')
    # for index in range(len(urls)):
    #     temp = urls[index] + ';' + str(cite_counts[index]) + ';' + option_journals[index] + '\n'
    #     txt_file.write(temp)
    # txt_file.close()


def second_visit(url):
    """
    This function main work is to storage the urls of the result
    """
    a = title2Url(url)
    urls = a.get_urls()
    cite_counts = a.get_cite_count()
    option_journals = a.get_option_journal()

    # storage the fist visited urls
    txt_file = open('data/'+str(NUM)+'/urls.txt', 'a')
    for index in range(len(urls)):
        temp = urls[index] + ';'+str(cite_counts[index]) + ';'+option_journals[index] + '\n'
        txt_file.write(temp)
    txt_file.close()


def control_function():
    """
    This function main work is to finish the next work after the first_visit function have done
    """
    # read the total num of items
    txt_file = open('data/'+str(NUM)+'/total_num.txt', 'r')
    items_num = int(txt_file.readline())
    txt_file.close()

    # compute the page num base on the total num of items
    page_num = items_num / 50 + 2

    # read the page num that should be visit in the next time
    txt_file = open('data/'+str(NUM)+'/now_visit.txt', 'r')
    page_th = int(txt_file.readline()) + 1
    txt_file.close()

    while page_th <= page_num:
        # storage the page num in cscfile
        txt_file = open('data/'+str(NUM)+'/now_visit.txt', 'w')
        txt_file.write(str(page_th))
        txt_file.close()

        url = "http://librarian.wanfangdata.com.cn/SearchResult.aspx?dbhit=wf_qk%3a"\
              + str(items_num) \
              + "&q="\
              + CONTENT\
              + "&p=" + str(page_th)
        print url, page_th
        second_visit(url)
        page_th += 1


def main():

    search_word = ''
    search_word = urllib.quote(search_word)  # 将原始检索字段转化为网页可识别

    url = "http://librarian.wanfangdata.com.cn/SearchResult.aspx?q="\
          + CONTENT

    first_visit(url)
    control_function()


if __name__ == '__main__':
    main()
