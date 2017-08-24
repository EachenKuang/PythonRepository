# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.23
Goal:
Other: 集成了所有的函数
"""

import logging
import xlwt
from gensim import models
from gensim import corpora
from collections import OrderedDict
from MedicineTool import SemanticsSim, Density, DocNumPerTopic
import os


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# ---------------------------------------------------------------------------------------------------#
'''
字典有关的函数
'''
def save_dict():
    """
    保存原始字典文件以及所有词库
    :return:
    """
    # data_path_in_folds = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\SecondPartDataFiles2\\"
    data_path_in_folds = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\About2Medic\\DataWords\\"
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
    dictionary.save_as_text('Dictionary/dict2_n_text', False)
    # corpus = [dictionary.doc2bow(text) for text in texts]
    # corpora.BleiCorpus.serialize("Dictionary/corpus_all_in_dict2.blei", corpus)


def filter_dictionary():
    dictionary = corpora.Dictionary.load('Dictionary/dict2_n.dict')
    # dictionary.filter_extremes(no_below=3, no_above=0.15, keep_n=None, keep_tokens=None)
    dictionary.filter_extremes(5, 0.1)
    dictionary.save('Dictionary/dict2_n_f.dict')
    dictionary.save_as_text('Dictionary/dict2_n_f_text')


# ---------------------------------------------------------------------------------------------------#
'''
形成数据集有关的函数
'''
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
    corpora.BleiCorpus.serialize('Corpus/corpus_'+name+'.blei', corpus, id2word=dictionary)

    lda_model = \
        models.LdaModel(alpha=0.5,
                        eta=0.005,
                        corpus=corpus,
                        id2word=dictionary,
                        num_topics=10,
                        per_word_topics=True,
                        iterations=300)
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
'''
知识演化部分的函数：
   都会将结果保存在文件中
cos_sim:余弦相似度
semantic_sim:语义相似度
num_per_topic:主题中文档数量
density：主题密度
print_topic：打印主题词
'''
def cos_sim(lda_list, store_path):
    """
    计算相邻时间窗的余弦相似度，并将结果保存在Excel中
    :param lda_list:
    :param store_path
    :return:
    """
    print "cos_sim is running"

    topic_dict_all = []
    for i in range(lda_list.__len__()):
        topic_dict = dict(lda_list[i].show_topics(num_words=40, formatted=False))
        topic_dict_all.append(topic_dict)

    wbk = xlwt.Workbook()
    for i in range(4):
        sheet = wbk.add_sheet('sheet'+str(i))
        for j in range(10):
            for k in range(10):
                print(j, k)
                sim1 = models.interfaces.matutils.cossim(topic_dict_all[i][j], topic_dict_all[i+1][k])
                sheet.write(j + 1, k + 1, str(sim1))
    wbk.save(store_path+"topic_evolution_cos_sim(period).xls")


def semantic_sim(lda_list, store_path):
    """
    计算相邻时间窗的语义相似度，并将结果保存在Excel中
    需要用到数据库中的内容:MH、EN、MH、AN 原始数据在"d2017.bin"文件中
    :param lda_list:
    :param store_path:
    :return:
    """
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
    for i in range(lda_list.__len__()):
        print str(i) + 'in main'
        temp_list = SemanticsSim.model2list_topics(lda_list[i])
        list_all.append(temp_list)

    wbk = xlwt.Workbook()
    for i in range(4):
        sheet = wbk.add_sheet('sheet'+str(i))
        for j in range(10):
            for k in range(10):
                print(j, k)
                sim1 = SemanticsSim.Innovation.inno(list_all[i][j], list_all[i+1][k], dic_MN, dic_AN, dic_EN)
                sheet.write(j + 1, k + 1, str(sim1))
    wbk.save(store_path + "topic_evolution_semanticSim(period).xls")


def num_per_topic(corpus_list, lda_list, store_path):
    """
    计算每个主题中的文档数量，调用模块DocNumPerTopic中的num_doc_per_topic函数
    另外，该模块中还集成了与文档相关的其他函数
    :param corpus_list:
    :param lda_list:
    :param store_path
    :return:
    """
    print "num_per_topic is running"
    with open(store_path+"numpertopic", "w")as writer:
        writer.write("num_per_topic:")
        for i in range(lda_list.__len__()):
            writer.write(str(DocNumPerTopic.num_doc_per_topic(lda_list[i], corpus_list[i])))


def density(corpus_list, lda_list, store_path):
    """
    计算每个主题的密度情况，调用模块Density中的cal_density函数
    :param corpus_list:
    :param lda_list:
    :param store_path
    :return:
    """
    print "density is running"
    with open(store_path + "density", "w")as writer:
        writer.write("density:")
        for i in range(lda_list.__len__()):
            # print density.cal_density(lda_list[i], corpus_list[i])
            writer.write(str(Density.cal_density(lda_list[i], corpus_list[i])))


def print_topic(lda_list, store_path):
    """
    打印lda_list中的主题。可以对num_words修改，得到top的主题词
    :param lda_list:
    :param store_path:
    :return:
    """
    # name = ['2005-2006', '2006-2007', '2007-2008',
    #         '2008-2009', '2009-2010', '2010-2011',
    #         '2011-2012', '2012-2013', '2013-2014',
    #         '2014-2015', '2015-2016']
    # name = ['1999-2000', '2001-2002', '2003-2004']
    name = ['2006-2007-2008', '2008-2009-2010', '2010-2011-2012', '2012-2013-2014', '2014-2015-2016']
    for j in range(name.__len__()):
        show = lda_list[j].show_topics(num_words=40, formatted=False)
        topic_dict = OrderedDict(show)
        with open(store_path + name[j] + 'topic_format', 'w') as temp:
            # temp.write(str(show))
            for i in range(10):
                # topic_dict[i]  # topic i 中的对应字段 list
                topic_dict_each = OrderedDict(topic_dict[i])
                temp.write('topic' + str(i) + '\n')
                for id, value in topic_dict_each.iteritems():
                    temp.write(id + ' ' + str(value) + '\n')

# ---------------------------------------------------------------------------------------------------#

def main():

    names = ['2006-2007-2008', '2008-2009-2010', '2010-2011-2012', '2012-2013-2014', '2014-2015-2016']
    path = "Output/"
    lda_list = []
    corpus_list = []
    for name in names:
        lda = models.LdaModel.load('Corpus3/lda_model_'+name)
        corpus = corpora.BleiCorpus('Corpus3/corpus_'+name+'.blei')
        lda_list.append(lda)
        corpus_list.append(corpus)

    num_per_topic(lda_list, corpus_list, path)
    density(lda_list, corpus_list, path)
    print_topic(lda_list, path)
    cos_sim(lda_list, path)
    semantic_sim(lda_list, path)


if __name__ == '__main__':
    main()


# save_dict()
# filter_dictionary()
# period_store()
