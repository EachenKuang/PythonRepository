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
from MedicineSCI.eigenvalue import indicators, Innovation
from MedicineTool import DocNumPerTopic
import numpy as np


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

    Innovation.inno(topic_i, topic_j, MN, AN, EN)


def interdisciplinary(doc_list):
    path = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\About2Medic\\DataFile\\paper_CR_test.txt"
    indicators.get_subject_displine(doc_list, path)


def main():

    """ ****************************************************************** """
    # lda model
    lda1 = models.LdaModel.load('Corpus/lda_model_2012-2013')
    lda2 = models.LdaModel.load('Corpus/lda_model_2013-2014')
    lda3 = models.LdaModel.load('Corpus/lda_model_2013-2014')
    lda_list = [lda1, lda2, lda3]

    # corpus
    corpus0 = corpora.BleiCorpus("Corpus/corpus_2012-2013.blei")
    corpus1 = corpora.BleiCorpus("Corpus/corpus_2013-2014.blei")
    corpus2 = corpora.BleiCorpus("Corpus/corpus_2014-2015.blei")
    corpus_list = [corpus0, corpus1, corpus2]

    """ ****************************************************************** """
    # 用于存放MH-EN，MN，AN的字典,在函数innovation中使用
    # dic_EN = {}
    # dic_MN = {}
    # dic_AN = {}
    # # 用于测试、真实数据
    # t = []
    # ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    # resultList = ms.ExecQuery("SELECT MH,EN,MN,AN FROM MeshStructure")
    # for (MH, EN, MN, AN) in resultList:
    #     dic_EN[MH] = EN
    #     dic_MN[MH] = MN
    #     dic_AN[MH] = AN

    """ ****************************************************************** """
    # 用于 high_attention函数与novelty函数
    # list_PY = []
    # list_TC = []
    # file = open("DataFile/Py_TC", "r")
    # for line in file:
    #     line = line.split()
    #     list_PY.append(line[1])
    #     list_TC.append(line[2])
    # print list_PY, list_TC
    """ ****************************************************************** """
    # 初始化
    doc_all = []
    offset = [2633, 1891, 1161]
    for i in range(3):
        doc = DocNumPerTopic.doc_topic_mat(corpus_list[i], lda_list[i], offset[i])
    doc_all.append(doc)
    doc_all_np = np.array(doc_all)

if __name__ == '__main__':
    main()
