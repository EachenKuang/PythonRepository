# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.7.11
Goal: time_window by 3 years with a year covered
Other:
每三年一个时间窗，一年重叠  2000-2017 共18年 九个时间窗
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
        with open(path + doc_name, 'r') as doc:
            text = []
            for line in doc:
                text.append(line.strip())
        texts.append(text)
    return texts


def make_store(texts, name):
    # dictionary = corpora.Dictionary(texts)
    # dictionary.save('./tmp/_' + name + '.dict')
    dictionary = corpora.Dictionary.load('./dictionary/dict.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize('./timewindow_in3/corpus_' + name + '.blei', corpus, id2word=dictionary)

    lda_model = \
        models.LdaModel(alpha=0.5,
                        eta=0.1,
                        corpus=corpus,
                        id2word=dictionary,
                        num_topics=10,
                        per_word_topics=True,
                        iterations=100)
    lda_model.save('./timewindow_in3/_' + name + 'lda_model')

    # # 保存主题
    # show = lda_model.show_topics(num_words=40, formatted=False)
    # topic_dict = dict(show)
    #
    # with open('./out3/'+name+'topic_format', 'w') as temp:
    #     # temp.write(str(show))
    #     for i in range(10):
    #         topic_dict[i]  # topic i 中的对应字段 list
    #         topic_dict_each = dict(topic_dict[i])
    #         temp.write('topic'+str(i)+'\n')
    #         for id, value in topic_dict_each.iteritems():
    #             temp.write(id+' '+str(value)+'\n')
    #
    # # lda_model.expElogbeta
    # print name + "successful\n"


def main():
    # default_path = "D:\\Kuangyichen\\PythonRepository\\MedicineTool\\year\\2000\\"
    default_path = "./year/"
    data_in_folds_year = os.listdir(default_path)
    # data_in_folds_year.sort()   #排序
    # print data_in_folds_year

    texts_list = []
    dictionary_list = {}
    for time in data_in_folds_year:
        text = read_from_raw(default_path + time + '//')
        # print text[0]
        texts_list.append(text)
        dictionary_list[time] = text
    # print dictionary[2000]
    # print texts_list[0]

    for i in range(0, 9):

        texts_use = dictionary_list[data_in_folds_year[i * 2]] + \
                    dictionary_list[data_in_folds_year[i * 2 + 1]] + \
                    dictionary_list[data_in_folds_year[i * 2 + 2]]
        print texts_use[0]
        make_store(texts_use, data_in_folds_year[i * 2] +
                   '-' + data_in_folds_year[i * 2 + 1] +
                   '-' + data_in_folds_year[i * 2 + 2])


#增加1999-2000 时间窗。
def test():
    path = "./year/1999/"
    # read_from_raw(path)
    make_store(read_from_raw(path), "1999-2000")

test()
# if __name__ == '__main__':
#     main()




