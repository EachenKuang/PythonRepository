# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.18
Goal: 计算4个特征测度
        高关注度（HighAttention）
        新颖性（Novelty）
        创新性（Innovation）
        学科交叉性（Interdisciplinary）
"""

from gensim import models, corpora
from MedicineSCI.InterfaceSQL import MSSQL
from MedicineSCI.eigenvalue import indicators, Innovation
from MedicineTool import DocNumPerTopic, SemanticsSim
from collections import OrderedDict
import numpy as np
import xlwt


# 〖HA〗_i代表第i个主题的关注度值，∑_(j=1)^n▒C_j 计算了主题内n篇文献的总被引频次，n代表主题内文献总量。
# 被引用频次 TC
def high_attention(times_cited):
    total_times_cited = 0.0
    n = len(times_cited)
    for cite in times_cited:
        total_times_cited += int(cite)
    return total_times_cited/n


# N_i代表第i个主题的新颖性值，∑_(j=1)^n▒T_j 计算了主题内n篇文献的总产生时间，n代表主题内文献总量。
# 发表时间 PY
def novelty(published_year):
    total_published_year = 0.0
    n = len(published_year)
    for year in published_year:
        total_published_year += int(year)
    return total_published_year/n


def innovation(topic_i, topic_j, MN, AN, EN):

    return Innovation.inno(topic_i, topic_j, MN, AN, EN)


def interdisciplinary(doc_list):
    path = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\About2Medic\\DataFile\\paper_CR_test.txt"
    return indicators.get_subject_displine(doc_list, path)


def print_topic(lda_list):
    name = ['budding', 'growing', 'mature']
    for j in range(3):
        show = lda_list[j].show_topics(num_words=40, formatted=False)
        topic_dict = OrderedDict(show)
        with open('./period_out/' + name[j] + 'topic_format', 'w') as temp:
            # temp.write(str(show))
            for i in range(10):
                # topic_dict[i]  # topic i 中的对应字段 list
                topic_dict_each = OrderedDict(topic_dict[i])
                temp.write('topic' + str(i) + '\n')
                for id, value in topic_dict_each.iteritems():
                    temp.write(id + ' ' + str(value) + '\n')


def main():
    """ ****************************************************************** """
    # lda model
    lda1 = models.LdaModel.load('Corpus/lda_model_2012-2013')
    lda2 = models.LdaModel.load('Corpus/lda_model_2013-2014')
    lda3 = models.LdaModel.load('Corpus/lda_model_2014-2015')
    lda_list = [lda1, lda2, lda3]

    # corpus
    corpus0 = corpora.BleiCorpus("Corpus/corpus_2012-2013.blei")
    corpus1 = corpora.BleiCorpus("Corpus/corpus_2013-2014.blei")
    corpus2 = corpora.BleiCorpus("Corpus/corpus_2014-2015.blei")
    corpus_list = [corpus0, corpus1, corpus2]

    """ ****************************************************************** """
    # 用于存放MH-EN，MN，AN的字典,在函数innovation中使用
    dic_EN = {}
    dic_MN = {}
    dic_AN = {}
    # 用于测试、真实数据
    ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    result_list = ms.ExecQuery("SELECT MH,EN,MN,AN FROM MeshStructure")
    for (MH, EN, MN, AN) in result_list:
        dic_EN[MH] = EN
        dic_MN[MH] = MN
        dic_AN[MH] = AN

    """ ****************************************************************** """
    # 用于 high_attention函数与novelty函数
    list_PY = []
    list_TC = []
    file = open("DataFile/Py_TC", "r")
    for line in file:
        line = line.split()
        list_PY.append(line[1])
        list_TC.append(line[2])
    # print list_PY, list_TC
    # list_PY_np = np.array(list_PY)
    # list_TC_np = np.array(list_TC)

    """ ****************************************************************** """
    # 初始化doc_topic_matrix
    doc_all = []
    offset = [2633, 1891, 1161]
    for i in range(3):
        doc = DocNumPerTopic.doc_topic_mat(corpus_list[i], lda_list[i], offset[i])
        doc_all.append(doc)
    print doc_all.__len__(), doc_all[0].__len__(),
    doc_all_np = np.array(doc_all)
    # doc_all_np 3维 （时间维0,1,2）（主题维（0,9））（文档）

    """ ****************************************************************** """
    # 初始化word_topic_matrix
    word_topic_all = []
    for i in range(3):
        print str(i)+'in main'
        temp_list = SemanticsSim.model2list_topics(lda_list[i])
        word_topic_all.append(temp_list)

    # print list_all.__len__()
    # print list_all[0].__len__()
    # print list_all[0][0].__len__()
    # print list_all

    """ ****************************************************************** """
    # 循环 3*10
    wbk = xlwt.Workbook()
    for period in range(3):
        sheet = wbk.add_sheet("sheet"+str(period))
        for topic in range(10):
            temp1 = high_attention([list_PY[j-1] for j in doc_all_np[period][topic]])
            temp2 = novelty([list_TC[j-1] for j in doc_all_np[period][topic]])
            temp3 = interdisciplinary(doc_all_np[period][topic])
            sheet.write(1, topic+1, temp1)
            sheet.write(2, topic+1, temp2)
            sheet.write(3, topic+1, temp3)

    wbk.save("Output/eigenvalue.xls")

    wbk = xlwt.Workbook()
    # sum_list_all = []
    for i in range(2, 3):
        sheet = wbk.add_sheet('sheet' + str(i))
        # sum_list = []
        for j in range(10):
            sum_topic = 0.0
            for k in range(10):
                print str(i) + str(i + 1) + 'topic'
                print(j, k)
                sim1 = innovation(word_topic_all[i][j], word_topic_all[i][k], dic_MN, dic_AN, dic_EN)
                print sim1
                sheet.write(j + 1, k + 1, str(sim1))
                # sum_topic += sim1
            # sum_list.append(sum_topic)
        # sum_list_all.append(sum_list)

    wbk.save("Output/Innovation1.xls")
    # print sum_list_all
if __name__ == '__main__':
    main()
