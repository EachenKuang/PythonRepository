# -*- encoding: utf-8 -*-

"""
Author: Eachen Kuang
Date:  2017.8.1
Goal: Decsity Index 密度指标
Other:
"""
from gensim import matutils
from gensim import models
from gensim import corpora
import numpy as np
import logging
import Global
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def cal_density(corpus, lda):
    """
    用来计算主题模型的密度
    :param corpus:语料库
    :param lda:LDA模型
    :return:density:密度值的list
    """

    # 将一个corpus转化为一个密集矩阵（全矩阵）
    # 函数corpus2dense中的参数num_docs为可选
    dense_matrix = matutils.corpus2dense(corpus=corpus, num_terms=corpus.id2word.__len__(), num_docs=corpus.__len__())

    # 矩阵相乘使用np.dot 参数为两个ndaray类型的（需要与np.mutiply区分开来）
    # out 的结果是一个 num_terms * num_terms 的矩阵，也就是我们需要的共线矩阵
    out = np.dot(dense_matrix, dense_matrix.T)

    # average保存了每个词的共线度
    average = []
    for line in out:
        sum_line = 0.0
        length = line.__len__()
    #    print length
        for element in line:
            sum_line += element
        average_line = sum_line/length
        average.append(average_line)
    # print average
    average_np = np.array(average)

    density = []
    for topic_id in range(0, 10):
        raw_string = lda.get_topic_terms(topic_id, 100)
        mid_string = [s[0] for s in raw_string]
        # 计算每个topic_id对应的密度指标
        ave = Global.average_from_list(average_np[mid_string])
        density.append(ave)

    return density

# 先写一个示例，用一个corpus与一个LdaModel来测试，之后在使用循环解决所有问题
corpus_exam = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
lda_exam = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')
cal_density(corpus_exam, lda_exam)
