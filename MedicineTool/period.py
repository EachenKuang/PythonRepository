# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.11
Goal: three period 1980-2000,2001-2012,2013-2017
Other: 分阶段形成LDA模型文件以及词文件
"""
import logging
import xlwt
from gensim import models
from gensim import corpora
from collections import OrderedDict
import SemanticsSim
import Density
import DocNumPerTopic
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


# **************************************************************************************************
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
    dictionary = corpora.Dictionary.load('./dictionary/dict.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize('./period_static/corpus_'+name+'.blei', corpus, id2word=dictionary)

    lda_model = \
        models.LdaModel(alpha=5,
                        eta=0.1,
                        corpus=corpus,
                        id2word=dictionary,
                        num_topics=10,
                        per_word_topics=True,
                        iterations=200)
    lda_model.save('./period_static/_'+name+'lda_model')

    # lda_model.show_topics(num_words=40)

    print name+"successful\n"


def period_store():
    """
    分阶段形成LDA模型文件以及词文件
    :return:
    """
    # default_path = "D:\\Kuangyichen\\PythonRepository\\MedicineTool\\year\\2000\\"
    default_path = "./period/"
    data_in_folds_year = os.listdir(default_path)

    for time in data_in_folds_year:
        text = read_from_raw(default_path+time+'//')
        make_store(text, time)
# **************************************************************************************************


def cos_sim(lda_list):
    print "cos_sim is running"
    show1 = lda_list[0].show_topics(num_words=40, formatted=False)
    topic_dict1 = dict(show1)
    show2 = lda_list[1].show_topics(num_words=40, formatted=False)
    topic_dict2 = dict(show2)
    show3 = lda_list[2].show_topics(num_words=40, formatted=False)
    topic_dict3 = dict(show3)

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("sheet 1")

    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict1[i], topic_dict2[j])
            sheet.write(i + 1, j + 1, str(sim1))
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim2 = models.interfaces.matutils.cossim(topic_dict2[i], topic_dict3[j])
            sheet.write(i + 1, j + 13, str(sim2))
    wbk.save("./period_out/topic_evolution_cos_sim(period).xls")


def semantic_sim(lda_list):
    print "semantic_sim is running"
    ms = SemanticsSim.Innovation.MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    resultList = ms.ExecQuery("SELECT MH,EN,MN,AN FROM MeshStructure")
    # 用于存放MH-EN，MN，AN的字典
    dic_EN = {}
    dic_MN = {}
    dic_AN = {}
    for (MH, EN, MN, AN) in resultList:
        dic_EN[MH] = EN
        dic_MN[MH] = MN
        dic_AN[MH] = AN

    list_all = []
    for i in range(3):
        print str(i) + 'in main'
        temp_list = SemanticsSim.model2list_topics(lda_list[i])
        list_all.append(temp_list)

    # print list_all.__len__()
    # print list_all[0].__len__()
    # print list_all[0][0].__len__()
    # print list_all

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("sheet1")
    for j in range(10):
        for k in range(10):
            print(j, k)
            sim1 = SemanticsSim.Innovation.inno(list_all[0][j], list_all[1][k], dic_MN, dic_AN, dic_EN)
            sheet.write(j + 1, k + 1, str(sim1))

    for j in range(10):
        for k in range(10):
            print(j, k)
            sim2 = SemanticsSim.Innovation.inno(list_all[1][j], list_all[2][k], dic_MN, dic_AN, dic_EN)
            sheet.write(j + 1, k + 13, str(sim2))
    wbk.save("./period_out/topic_evolution_semanticSim(period).xls")


def num_per_topic(corpus_list, lda_list):
    print "num_per_topic is running"
    with open("./period_out/density&numpertopic", "a")as writer:
        writer.write("num_per_topic:")
        for i in range(3):
            # print density.cal_density(lda_list[i], corpus_list[i])
            writer.write(str(DocNumPerTopic.num_doc_per_topic(lda_list[i], corpus_list[i])))


def density(corpus_list, lda_list):
    with open("./period_out/density&numpertopic", "a")as writer:
        writer.write("density:")
        for i in range(3):
            # print density.cal_density(lda_list[i], corpus_list[i])
            writer.write(str(Density.cal_density(lda_list[i], corpus_list[i])))


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

    lda1 = models.LdaModel.load('./period_static/_buddinglda_model')
    lda2 = models.LdaModel.load('./period_static/_growinglda_model')
    lda3 = models.LdaModel.load('./period_static/_maturelda_model')
    lda_list = [lda1, lda2, lda3]

    corpus0 = corpora.BleiCorpus("./period_static/corpus_budding.blei")
    corpus1 = corpora.BleiCorpus("./period_static/corpus_growing.blei")
    corpus2 = corpora.BleiCorpus("./period_static/corpus_mature.blei")
    corpus_list = [corpus0, corpus1, corpus2]

    cos_sim(lda_list)
    semantic_sim(lda_list)
    num_per_topic(lda_list, corpus_list)
    density(lda_list, corpus_list)
    print_topic(lda_list)

if __name__ == '__main__':
    main()

