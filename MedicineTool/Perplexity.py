# -*- encoding: utf-8 -*-

"""
Author: Eachen Kuang
Date:  2017.7.11
Goal: Perplexity 困惑度画图计算
Other:
"""

import logging
from gensim import models
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# calculating the log perplexity per word as obtained by gensim code
# https://radimrehurek.com/gensim/models/atmodel.html
# parameters: pass in trained corpus
# return: graph of perplexity per word for varying number of topics

# 初始化数据
# 如果已经保存，就可不运行
# data_path_in_folds = "D:\\Kuangyichen\\JavaRepository\\LDAGibbsSampling-master\\data\\LdaOriginalDocs\\"
# data_in_folds_filenames = os.listdir(data_path_in_folds)
# # data_in_folds_filenames.sort()
# texts = []
#
# for date_in_file in data_in_folds_filenames:
#     with open(data_path_in_folds+date_in_file, 'r') as doc:
#         text = []
#         for line in doc:
#             text.append(line.strip())
#     texts.append(text)
#
# dictionary = corpora.Dictionary(texts)
# dictionary.save('./tmp/all_doucment.dict.txt')
# corpus = [dictionary.doc2bow(text) for text in texts]
# corpora.BleiCorpus.serialize('./tmp/corpus.blei', corpus)

# 如果已经有数据，运行以下语句即可
# dictionary = corpora.Dictionary.load('./tmp/all_doucment.dict.txt')
# corpus = corpora.BleiCorpus('./tmp/corpus.blei')

parameter_list = range(5, 40)
grid = {}
grid1 = {}
corpus = corpora.BleiCorpus("./timewindow_in3/corpus_2008-2009-2010.blei")
dictionary = corpora.Dictionary.load("./dictionary/dict.dict")
# lda1 = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')

for parameter_value in parameter_list:

    ldaModel = models.LdaModel(corpus=corpus, id2word=dictionary, alpha='auto', eta='auto', num_topics=parameter_value, iterations=10)
    ldaModel1 = models.LdaModel(corpus=corpus, id2word=dictionary,  num_topics=parameter_value, iterations=10)
    coherenceModel = CoherenceModel(model=ldaModel, corpus=corpus, dictionary=dictionary, coherence='u_mass')
    coherenceModel1 = CoherenceModel(model=ldaModel1, corpus=corpus, dictionary=dictionary, coherence='u_mass')

    grid[parameter_value] = []
    coherence = coherenceModel.get_coherence()
    grid[parameter_value].append(coherence)

    grid1[parameter_value] = []
    coherence1 = coherenceModel1.get_coherence()
    grid1[parameter_value].append(coherence1)

    print parameter_value, coherence, coherence1

df = pd.DataFrame(grid)
ax = plt.figure(figsize=(5, 3), dpi=300).add_subplot(111)
df.iloc[0].transpose().plot(ax=ax,  color="#254F09")
plt.xlim(parameter_list[0], parameter_list[-1])
plt.ylabel('Perplexity')
plt.xlabel('topics')
plt.show()

df = pd.DataFrame(grid1)
ax = plt.figure(figsize=(5, 3), dpi=300).add_subplot(111)
df.iloc[0].transpose().plot(ax=ax,  color="#254F09")
plt.xlim(parameter_list[0], parameter_list[-1])
plt.ylabel('Perplexity')
plt.xlabel('topics')
plt.show()

for topic_num, perplex_tn in grid.iteritems():
    print topic_num, perplex_tn

for topic_num, perplex_tn in grid1.iteritems():
    print topic_num, perplex_tn