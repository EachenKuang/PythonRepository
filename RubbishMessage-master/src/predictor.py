# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 基于主题的情感分析比赛（使用jieba）
# Other:
# '''
# import gensim
import numpy as np
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.externals import joblib
from gensim import corpora, models, matutils
import random
import logging
from datetime import datetime

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def iter_readbatch(data_stream, minibatch_size=10000):
    """
    迭代器
    给定文件流（比如一个大文件），每次输出minibatch_size行，默认选择1k行
    :param data_stream:
    :param minibatch_size:
    :return:
    """
    cur_line_num = 0
    with open(data_stream, 'r') as doc:
        text = []
        for line in doc:
            text.append(line.strip().split())
            cur_line_num += 1
            if cur_line_num >= minibatch_size:
                yield text
                text = []
                cur_line_num = 0


def save_dict():
    """
    保存字典以及语料库
    :return:
    """
    dictionary = corpora.Dictionary()
    for index, text in enumerate(iter_readbatch('../data/trainLeft.txt', minibatch_size=20000)):
        print("{} time".format(index))
        dictionary.add_documents(text)
        print("success")
        dictionary.save('../dictionary/dict{}.dict'.format(index))
        # corpus = [dictionary.doc2bow(t) for t in text]
        # corpora.BleiCorpus.serialize("../corpus/corpus_{}.blei".format(index), corpus, id2word=dictionary)
    dictionary.save('../dictionary/dict.dict')
    dictionary.save_as_text('../dictionary/dict4text', False)

def save_corpus():
    """
    在Dictionary已经生产的情况下，标准化corpus并且存储在本地，20000doc一个corpus
    :return:
    """
    dictionary = corpora.Dictionary.load('../dictionary/new_dict_filter.dict')
    for index, text in enumerate(iter_readbatch('../data/testLeft.txt', minibatch_size=20000)):
        print ("{} time".format(index))
        print ("success")
        corpus = [dictionary.doc2bow(t) for t in text]
        corpora.MmCorpus.serialize("../test_corpus/corpus_{}.mm".format(index), corpus, id2word=dictionary)


def filter_dictionary():
    """
    过滤字典，将字典缩小
    :return:
    """

    """
    ../dictionary/dict.dict 最原始的字典，保留最完全200w
    ../dictionary/dict_filter.dict 过滤后剩下30w字段的字典
    ../dictionary/new_dict_filter.dict 过滤掉2.4w 特殊字符的后剩下27.6w字段的字典
    """
    dictionary = corpora.Dictionary.load('../dictionary/dict.dict')
    # dictionary.filter_extremes(no_below=3, no_above=0.15, keep_n=None, keep_tokens=None)
    dictionary.filter_extremes(5, 0.1, keep_n=300000)  # 保证有300000的词汇
    dictionary.save('../dictionary/dict_filter.dict')
    dictionary.save_as_text('../dictionary/dict_filter4text')

    # 28116
    # dictionary = corpora.Dictionary.load('../dictionary/dict_filter.dict')
    # bad_ids = []
    # with open('../dictionary/dict_filter4text') as fr:
    #     for line in fr.readlines()[0:28116]:
    #         line = line.strip().split()[0]
    #         bad_ids.append(int(line))
    # dictionary.filter_tokens(bad_ids=bad_ids)
    # dictionary.save('../dictionary/new_dict_filter.dict')
    # dictionary.save_as_text('../dictionary/new_dict_filter4text')

def read_label():
    label_list = []
    with open('../data/classLabel.txt') as fr:
        for line in fr:
            label_list.append(int(line.strip()))
    return np.array(label_list)


def totalScore(pred, y_test):
    A = 0
    C = 0
    B = 0
    D = 0

    for i in range(len(pred)):
        if y_test[i] == 0:
            if pred[i] == 0:
                A += 1

            elif pred[i] == 1:
                B += 1

        elif y_test[i] == 1:
            if pred[i] == 0:
                C += 1

            elif pred[i] == 1:
                D += 1

    print (A, B, C, D, A + B + C + D)

    rb_pr = 1.0 * D / (B + D)
    rb_re = 1.0 * D / (C + D)
    rt_pr = 1.0 * A / (A + C)
    rt_re = 1.0 * A / (A + B)

    # Frb = 0.65 * rb_pr + 0.35 * rb_re
    # Frt = 0.65 * rt_pr + 0.35 * rt_re
    # Ftotal = 0.7 * Frb + 0.3 * Frt
    Ftotal = 2*rb_pr*rb_re/(rb_pr+rb_re)
    print(Ftotal)
    return Ftotal

def nbc():
    choose_1 = random.randint(0, 25)
    # choose_2 = random.randint(0, 25)
    corpus1 = corpora.BleiCorpus('../corpus/corpus_{}.blei'.format(choose_1))
    corpus1 = corpora.BleiCorpus('../corpus/corpus_0.blei')
    # corpus_2 = corpora.BleiCorpus('../corpus/corpus_{}.blei'.format(choose_1))
    test_X = matutils.corpus2csc(corpus1).transpose()  # 测试集
    # print test_X.get_shape()
    label_list = read_label()
    test_y = label_list[(choose_1*20000):(choose_1+1)*20000]  # 测试集标签
    test_y = label_list[(0 * 20000):(0 + 1) * 20000]
    clf = MultinomialNB(alpha=0.01)
    for index in range(0, 25):
        corpus = corpora.BleiCorpus('../corpus/corpus_{}.blei'.format(index))
        csi_matrix = matutils.corpus2csc(corpus).transpose()
        if csi_matrix.get_shape() ==(20000, 271884):
            print(csi_matrix.get_shape())
            clf.partial_fit(csi_matrix,
                            label_list[(index*20000):(index+1)*20000],
                            classes=np.array([0, 1]))
            print("第{}次".format(index))
            pre = clf.predict(test_X)
            totalScore(pre, test_y)

# sklearn.naive_bayes.MultinomialNB
# sklearn.naive_bayes.BernoulliNB
# sklearn.linear_model.Perceptron
# sklearn.linear_model.SGDClassifier
# sklearn.linear_model.PassiveAggressiveClassifier

def this_is_for_fun():
    # clf = MultinomialNB(alpha=1.0)
    # clf = SGDClassifier(alpha=0.0001)
    # clf = PassiveAggressiveClassifier()
    clf = BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
    # clf = Perceptron(alpha=0.001)
    print('BernoulliNB,a = 1')

    label_list = read_label()
    choose = random.randint(10, 24)
    corpus = corpora.MmCorpus('../corpus_mm/corpus_{}.mm'.format(choose))
    test_X = matutils.corpus2csc(corpus).transpose()  # 测试集
    test_y = label_list[(choose * 20000):(choose + 1) * 20000]  # 测试集标签

    for index in range(10, 25):
        corpus = corpora.MmCorpus('../corpus_mm/corpus_{}.mm'.format(index))
        csi_matrix = matutils.corpus2csc(corpus).transpose()
        clf.partial_fit(csi_matrix,
                    label_list[(index * 20000):(index + 1) * 20000],
                    classes=np.array([0, 1]))
        print("第{}次".format(index))
        pre = clf.predict(test_X)
        totalScore(pre, test_y)
        joblib.dump(clf, "../model/BernoulliNB_model_{}.m".format(index))
        # test_corpus = corpora.MmCorpus('../test_corpus/corpus_{}.mm'.format(index))
        # csi_matrix = matutils.corpus2csc(test_corpus).transpose()
        # clf.predict(csi_matrix)


def tfidf_train():
    dictionary = corpora.Dictionary.load('../dictionary/new_dict_filter.dict')
    for index in range(0, 1):
        corpus = corpora.MmCorpus('../corpus_mm/corpus_{}.mm'.format(index))
        tfidf_model = models.TfidfModel(corpus=corpus, dictionary=dictionary)
        corpus_tfidf = np.array([tfidf_model[doc] for doc in corpus])
        # lsi_model = models.LsiModel(corpus=corpus, id2word=dictionary, num_topics=50)
        # corpus_lsi = [lsi_model[doc] for doc in corpus]
        # lsi_model.add_documents(corpus)
        # print corpus_tfidf


def analyse_lable():
    label = read_label()
    # a = label[0:20000]

    print(label[label<0.5].__len__())
    for index in range(0, 25):
        temp = label[index*20000:(index+1)*20000]
        zero = temp[temp<0.5].__len__()
        one = 20000-zero
        print(index, zero, one)



# filter_dictionary()
# read_label()
# corpus = corpora.BleiCorpus('../corpus/corpus_3.blei')
# corpus1 = corpora.BleiCorpus('../corpus/corpus_4.blei')
# print corpus.__len__(), corpus1.__len__()
# csi_matrix = matutils.corpus2csc(corpus)
# csi_matrix1 = matutils.corpus2csc(corpus1)
# print csi_matrix.get_shape, csi_matrix1.get_shape
# # clf = MultinomialNB(alpha=0.001)
# # clf.partial_fit(csi_matrix.transpose(), read_label()[0:20000], classes=np.array([0, 1]))  # 需要对矩阵转置
# # clf.partial_fit(csi_matrix1.transpose(), read_label()[20000:40000])

# save_dict()
# save_corpus()
# nbc()
# this_is_for_fun()
# tfidf_train()
# analyse_lable()
def predict():
    clf = joblib.load("../model/BernoulliNB_model_18.m")
    with open('../data/label2.txt', 'w') as fw:
        for index in range(20):
            print(str(index)+'times')
            test_corpus = corpora.MmCorpus('../test_corpus/corpus_{}.mm'.format(index))
            csi_matrix = matutils.corpus2csc(test_corpus).transpose()
            label = clf.predict(csi_matrix)
            print(label.__len__())
            for l in label:
                fw.writelines(str(l)+'\n')
                print(l)

def write_result():
    now = str(datetime.now()).replace(' ','-').replace(':','-')
    print(now)
    with open('../data/label2.txt', 'r') as fr1,\
        open('../data/testMsgNum.txt','r') as fr2,\
        open('../out/out_{}.csv'.format(now),'w') as fw:
        fr1 = fr1.readlines()
        fr2 = fr2.readlines()
        for index in range(400000):
            line1 = str(fr1[index]).strip()
            line2 = str(fr2[index]).strip()
            if line1=='1':
                line1 = 'POSITIVE'
            else:
                line1 = 'NEGATIVE'
            fw.write("{},{}\n".format(line2,line1))


# this_is_for_fun()
# predict()
write_result()
