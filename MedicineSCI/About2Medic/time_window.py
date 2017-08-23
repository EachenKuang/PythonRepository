# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.23
Goal: time_window by 3 years with a year covered
Other:
每两年一个时间窗 2005-2016 共12年 两年重叠一年，一共是11时间窗
"""
import logging
from gensim import models
from gensim import corpora
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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
    dictionary = corpora.Dictionary.load('Dictionary/dict2_n_f.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize('Corpus2/corpus_'+name+'.blei', corpus, id2word=dictionary)

    lda_model = \
        models.LdaModel(alpha=0.5,
                        eta=0.005,
                        corpus=corpus,
                        id2word=dictionary,
                        num_topics=10,
                        per_word_topics=True,
                        iterations=300)
    lda_model.save('Corpus2/lda_model_'+name)

    print name+"successful\n"


def main():
    # default_path = "D:\\Kuangyichen\\PythonRepository\\MedicineTool\\year\\2000\\"
    default_path = "YearWindow/"
    data_in_folds_year = os.listdir(default_path)
    # data_in_folds_year.sort()   #排序
    # print data_in_folds_year
    texts_list = []
    dictionary_list = {}
    for time in data_in_folds_year:
        text = read_from_raw(default_path+time+'//')
        # print text[0]
        texts_list.append(text)
        dictionary_list[time] = text

    # 调用函数保存成文件
    for i in range(11):
        texts_use = dictionary_list[data_in_folds_year[i]] + dictionary_list[data_in_folds_year[i + 1]]
        make_store(texts_use, data_in_folds_year[i]+'-'+data_in_folds_year[i+1])

if __name__ == '__main__':
    main()




