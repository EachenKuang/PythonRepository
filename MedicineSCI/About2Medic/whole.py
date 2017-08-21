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
    default_path = "Year1/"
    data_in_folds_year = os.listdir(default_path)

    for time in data_in_folds_year:
        text = read_from_raw(default_path+time+'//')
        make_store(text, time)
# ---------------------------------------------------------------------------------------------------#


def Interdisciplinary(paperIDs):
    reference = 0
    CategoryNum = 0   #保存学科数量
    JournalList = {}  #用于保存期刊对应所属类别的字典
    paperIDWithList = {} #用于保存每篇期刊ID对应的引用期刊LIST
    classWithNum = {}  #用于保存每个类对应的索引
    paperIDWithClass = {} #用于保存每篇期刊ID对应的分类LIST
    list = []

   #读取 ESIMasterJournalList.xlsx 文件 将表存在字典中
    data = xlrd.open_workbook("ESIMasterJournalList.xlsx","r")
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    for i in xrange(0, nrows):
        rowValues = table.row_values(i)  # 某一行数据
        for item in rowValues[0:3]:
            JournalList[item] = rowValues[-1]
    #print(JournalList)


#   #对主题内每个paperID对应的引文进行计算
    ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    for id in paperIDs:
        resList = ms.ExecQuery("SELECT CR FROM RawMedicine2 where paperID ='"+str(id) +"'")
        list = [] #初始化
        list2 = []
        print id
        try:
            for (CR,) in resList:

                referenceString = str(CR)
                stringList = referenceString.split(";")
                for string in stringList:
                    if (re.search("^[A-Z\s]*-*[A-Z\s]*$",string)):
                        list.append(string.strip())
            paperIDWithList[id] = list
            #print list,list.__len__()
            for li in list:
                if JournalList.has_key(li):
                    list2.append(JournalList[li])
            paperIDWithClass[id] = list2
            print paperIDWithClass[id]
        except BaseException, Argument: #出现异常跳过，在CR会存在一些非编码字符
            print Argument
            pass

    # 保存paperID 对应的 期刊 用分号隔开

    with open("paper_CR_new.txt", 'a') as write:
        for id in range(1, 13679):
            write.write(str(id)+";")
            for string in paperIDWithClass[id]:
                write.write(string+";")
            write.write("\n")

    write.close()

    #计数
    #classWithDocMatric = np.zeros()
    listIn = []

    print "---------------------------------"
    listAll = []
    for ids in paperIDs:
        tempList = paperIDWithClass[id]
        for string in tempList:
            #print type(string)
            if not listAll.__contains__(str(string)):
                listAll.append(string)
    print listAll
    print "---------------------------------"
    #print paperIDWithList
    print paperIDWithClass.keys()
    #print type(referenceString)

    # for id in paperIDs:
    #     list
    #     paperIDWithClass[id] = list


def main():
    pass

# save_dict()
# filter_dictionary()
period_store()
