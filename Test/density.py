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
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# 先写一个示例，用一个corpus与一个LdaModel来测试，之后在使用循环解决所有问题
corpus = corpora.BleiCorpus("./timewindow_in3/corpus_2000-2001-2002.blei")
lda = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')

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


# 因为需要多次在list中进行加法运算，故使用一个函数来集成
def average_from_list(input_list):
    sum_of_list = 0.0
    len_list = len(input_list)
    for num in input_list:
        sum_of_list += num
    ave = sum_of_list/len_list
    return ave


density = []
for topic_id in range(0, 10):
    raw_string = lda.get_topic_terms(topic_id, 100)
    mid_string = [s[0] for s in raw_string]
    # 计算每个topic_id对应的密度指标
    ave = average_from_list(average_np[mid_string])
    density.append(ave)

print density

