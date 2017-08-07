# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.7
Goal: calculate the number of document per topic
Other:计算每个主题中文档数目
"""
import logging
import Global
from gensim import models
from gensim import corpora

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 返回dict型list中value最大的key
def find_max_in_list(doc_topic_list):
    temper_dict = dict(doc_topic_list)
    return max(temper_dict.items(), key=lambda x: x[1])[0]


def num_doc_per_topic(corpus, lda):
    # 通过lad[document]来判断该文档属于lda的哪个topic
    # 返回一个list，保存
    a_list = [0] * Global.TOPIC_NUM  # 全局变量，这边默认为10
    for i in range(0, corpus.__len__()):
        # print lda[corpus.docbyoffset(corpus.index[i])][0]
        temper = find_max_in_list(lda[corpus.docbyoffset(corpus.index[i])][0])
        a_list[temper] += 1
    print corpus.__len__(), a_list
    return a_list
corpus = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
lda = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')

num_doc_per_topic(corpus, lda)
