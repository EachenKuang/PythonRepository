# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.7
Goal: calculate the number of document per topic
Other:计算每个主题中文档数目
"""
import logging
import Global
import heapq
from gensim import models
from gensim import corpora
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 返回dict型list中value最大的key,value 对
def find_max_in_list(doc_topic_list):
    temper_dict = dict(doc_topic_list)
    return max(temper_dict.items(), key=lambda x: x[1])


def find_top_document(corpus, lda, topn=5):
    """
    寻找每个主题中评分最高的n个文档，n默认为5
    :param corpus: 语料库
    :param lda: LDA模型
    :param topn: 数量 默认为5
    :return: a_list
    """
    a_list = [[] for i in range(Global.TOPIC_NUM)]

    # 将每篇文档对应主题的 document_id与概率 结果保存在一个二维数组中
    for i in range(0, corpus.__len__()):
        # print lda[corpus.docbyoffset(corpus.index[i])][0]
        temper = find_max_in_list(lda[corpus.docbyoffset(corpus.index[i])][0])
        a_list[temper[0]].append((i, temper[1]))

    # 遍历每个主题，利用heapq.nlargest函数计算出最大的n个，重新保存在a_list中
    for j in range(Global.TOPIC_NUM):
        temper_dict = dict(a_list[j])
        # heapq.nlargest(topn, temper_dict.items(), key=lambda x: x[1])
        a_list[j] = heapq.nlargest(topn, temper_dict.items(), key=lambda x: x[1])

    # print corpus.__len__(), a_list
    return a_list


def num_doc_per_topic(corpus, lda):
    """
    计算每个主题中文档数目
    :param corpus:语料库
    :param lda: LDA模型
    :return: a_list:主题文档数目的list
    """
    # 通过lad[document]来判断该文档属于lda的哪个topic
    # 返回一个list，保存
    a_list = [0] * Global.TOPIC_NUM  # 全局变量，这边默认为10
    for i in range(0, corpus.__len__()):
        # print lda[corpus.docbyoffset(corpus.index[i])][0]
        temper = find_max_in_list(lda[corpus.docbyoffset(corpus.index[i])][0])[0]
        a_list[temper] += 1
    # print corpus.__len__(), a_list
    return a_list


def doc_topic_mat(corpus, lda, offset=0):
    """
    :param corpus:
    :param lda:
    :param offset: 偏移量，用于修正doc_id在整体数据中的位置
    :return: 返回一个二维矩阵，保存doc_id
    """
    a_list = [[] for i in range(Global.TOPIC_NUM)]
    for i in range(0, corpus.__len__()):
        # print lda[corpus.docbyoffset(corpus.index[i])][0]
        temper = find_max_in_list(lda[corpus.docbyoffset(corpus.index[i])][0])[0]
        a_list[temper].append(i+offset)
    return np.array(a_list)


# 先写一个示例，用一个corpus与一个LdaModel来测试，之后在使用循环解决所有问题
# corpus_exam = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
# lda_exam = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')
#
# num_doc_per_topic(corpus_exam, lda_exam)

# 计算所有的文献topic


def main():

    lda0 = models.LdaModel.load('./timewindow_in3/_1999-2000lda_model')
    lda1 = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')
    lda2 = models.LdaModel.load('./timewindow_in3/_2002-2003-2004lda_model')
    lda3 = models.LdaModel.load('./timewindow_in3/_2004-2005-2006lda_model')
    lda4 = models.LdaModel.load('./timewindow_in3/_2006-2007-2008lda_model')
    lda5 = models.LdaModel.load('./timewindow_in3/_2008-2009-2010lda_model')
    lda6 = models.LdaModel.load('./timewindow_in3/_2010-2011-2012lda_model')
    lda7 = models.LdaModel.load('./timewindow_in3/_2012-2013-2014lda_model')
    lda8 = models.LdaModel.load('./timewindow_in3/_2014-2015-2016lda_model')
    lda9 = models.LdaModel.load('./timewindow_in3/_2016-2017lda_model')

    LDA_list = [lda0, lda1, lda2, lda3, lda4, lda5, lda6, lda7, lda8, lda9]

    corpus_exam0 = corpora.BleiCorpus("./timewindow_in3/corpus_1999-2000.blei")
    corpus_exam1 = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
    corpus_exam2 = corpora.BleiCorpus("./timewindow_in3/corpus_2002-2003-2004.blei")
    corpus_exam3 = corpora.BleiCorpus("./timewindow_in3/corpus_2004-2005-2006.blei")
    corpus_exam4 = corpora.BleiCorpus("./timewindow_in3/corpus_2006-2007-2008.blei")
    corpus_exam5 = corpora.BleiCorpus("./timewindow_in3/corpus_2008-2009-2010.blei")
    corpus_exam6 = corpora.BleiCorpus("./timewindow_in3/corpus_2010-2011-2012.blei")
    corpus_exam7 = corpora.BleiCorpus("./timewindow_in3/corpus_2012-2013-2014.blei")
    corpus_exam8 = corpora.BleiCorpus("./timewindow_in3/corpus_2014-2015-2016.blei")
    corpus_exam9 = corpora.BleiCorpus("./timewindow_in3/corpus_2016-2017.blei")

    corpus_list = [corpus_exam0, corpus_exam1, corpus_exam2, corpus_exam3, corpus_exam4,
                   corpus_exam5, corpus_exam6, corpus_exam7, corpus_exam8, corpus_exam9]

    # for (lda, corpus) in zip(LDA_list, corpus_list):
    #     # print num_doc_per_topic(corpus, lda)
    #     print lda
    #     print doc_topic_mat(corpus, lda)
    list_all = []
    for i in range(10):
        # print i
        list_t = doc_topic_mat(corpus_list[i], LDA_list[i])
        # print list_t
        list_all.append(list_t)
    list_np = np.array(list_all)

    # print type(list_all), type(list_all[0]),type(list_all[0][0])
    print "******************************************************"

    # print np.array(list_np[0][1])+7284
    # print np.array(list_np[1][5])+6940
    # print np.array(list_np[2][5])+6488
    # print np.array(list_np[3][5])+5961
    # print np.array(list_np[4][4])[np.array(list_np[4][4]) < 252] + 4749, np.array(list_np[4][4])[np.array(list_np[4][4]) >= 252] + 5249
    # print np.array(list_np[4][6])[np.array(list_np[4][6]) < 252]+4749, np.array(list_np[4][6])[np.array(list_np[4][6]) >= 252]+5249
    # print np.array(list_np[4][9])[np.array(list_np[4][9]) < 252] + 4749, np.array(list_np[4][9])[
    #                                                                          np.array(list_np[4][9]) >= 252] + 5249
    # print np.array(list_np[5][4])[np.array(list_np[5][4]) < 1164]+3836, np.array(list_np[5][4])[np.array(list_np[5][4]) >= 1164]+4336
    # print np.array(list_np[6][6])+2623
    # print np.array(list_np[7][1])[np.array(list_np[7][1]) <= 393] + 617, np.array(list_np[7][1])[np.array(list_np[7][1]) > 393] + 1117
    # print np.array(list_np[7][5])[np.array(list_np[7][5]) <= 393] + 617, np.array(list_np[7][5])[np.array(list_np[7][5]) > 393] + 1117
    # print np.array(list_np[7][7])[np.array(list_np[7][7]) <= 393] + 617, np.array(list_np[7][7])[np.array(list_np[7][7]) > 393] + 1117
    # print np.array(list_np[8][6])[np.array(list_np[8][6]) <= 1913], np.array(list_np[8][6])[np.array(list_np[8][6]) > 1913]+3087
    # print np.array(list_np[9][8])[np.array(list_np[9][8]) <= 499] + 1001, np.array(list_np[9][8])[np.array(list_np[9][8]) > 499] + 4501

if __name__ == '__main__':
    main()

