# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.18
Goal: three period 2012-2013, 2013-2014, 2014-2015 about medical 2 series
Other: 分阶段形成LDA模型文件以及词文件
"""

import logging
from gensim import models
from gensim import corpora
import numpy as np
import os
from pprint import pprint

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def save_dict():
    """
    保存原始字典文件以及所有词库
    :return:
    """
    # data_path_in_folds = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\SecondPartDataFiles2\\"
    data_path_in_folds = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\About2Medic\DataWords\\"
    data_in_folds_filenames = os.listdir(data_path_in_folds)
    # data_in_folds_filenames.sort()
    texts = []
    for date_in_file in data_in_folds_filenames:
        with open(data_path_in_folds+date_in_file, 'r') as doc:
            text = []
            for line in doc:
                text.append(line.strip())
        texts.append(text)

    dictionary = corpora.Dictionary(texts)
    dictionary.save('Dictionary/dict2_n.dict')
    dictionary.save_as_text('Dictionary/dict2new_text')
    # corpus = [dictionary.doc2bow(text) for text in texts]
    # corpora.BleiCorpus.serialize("Dictionary/corpus_all_in_dict2.blei", corpus)


def filter_dictionary():
    dictionary = corpora.Dictionary.load('Dictionary/dict2_n.dict')
    dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=None, keep_tokens=None)
    dictionary.save('Dictionary/dict2new.dict')
    dictionary.save_as_text('Dictionary/dict2new2_text')


# ---------------------------------------------------------------------------------------------------#
def read_from_raw(path):
    docs_name_list = os.listdir(path)
    texts = []
    for doc_name in docs_name_list:
        with open(path+doc_name, 'r') as doc:
            text = []
            for line in doc:
                text.append(line.strip())
        texts.append(text)
    return texts


def make_store(texts, name):
    dictionary = corpora.Dictionary.load('Dictionary/dict2new.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize('Corpus/corpus_'+name+'.blei', corpus, id2word=dictionary)

    lda_model = \
        models.LdaModel(alpha=5,
                        eta=0.1,
                        corpus=corpus,
                        id2word=dictionary,
                        num_topics=10,
                        per_word_topics=True,
                        iterations=200)
    lda_model.save('Corpus/lda_model_'+name)

    print name+"successful\n"


def period_store():
    """
    分阶段形成LDA模型文件以及词文件
    :return:
    """
    default_path = "Year/"
    data_in_folds_year = os.listdir(default_path)

    for time in data_in_folds_year:
        text = read_from_raw(default_path+time+'//')
        make_store(text, time)
# ---------------------------------------------------------------------------------------------------#
# save_dict()
# filter_dictionary()
# period_store()


def main():
    pass

