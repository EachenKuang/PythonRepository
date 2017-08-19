# -*- encoding: utf-8 -*-

# '''
# Author: Eachen Kuang
# Date:  2017.6.4
# Goal: new LDA model
# Other:计算余弦相似度
# '''
import logging
from gensim import models
from gensim import corpora
import numpy as np
import os
import xlwt
from pprint import pprint

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# 计算余弦值
# 传入参数：  a = [num1,num2,num3,...] b = [num1,num2,num3,...]


def cossim(a, b):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for x, y in zip(a, b):
        dot_product+=x*y
        normA += x**2
        normB += y**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product/((normA*normB)**0.5)


# lda0 = models.LdaModel.load('./timewindow_in3/_1999-2000lda_model')
# lda1 = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')
#
# phi0 = np.array(lda0.expElogbeta)
# phi1 = np.array(lda1.expElogbeta)
#
# show0 = lda0.show_topics(num_words=40, formatted=False)
# show1 = lda1.show_topics(num_words=40, formatted=False)
#
# topic_dict0 = dict(show0)
# topic_dict1 = dict(show1)
#
# wbk = xlwt.Workbook()
# sheet = wbk.add_sheet("sheet 1")
# for i in range(10):
#     for j in range(10):
#         print(i, j)
#         sim1 = models.interfaces.matutils.cossim(topic_dict0[i], topic_dict1[j])
#         sheet.write(i + 1, j + 1, str(sim1))
#         sim2 = cossim(phi0[i], phi1[j])
#         sheet.write(i + 1, j + 14, str(sim2))
#
# wbk.save("test_on1999.xls")


def main():
    # 读取lda模型
    lda1 = models.LdaModel.load('./timewindow_in3/_2000-2001-2002lda_model')
    lda2 = models.LdaModel.load('./timewindow_in3/_2002-2003-2004lda_model')
    lda3 = models.LdaModel.load('./timewindow_in3/_2004-2005-2006lda_model')
    lda4 = models.LdaModel.load('./timewindow_in3/_2006-2007-2008lda_model')
    lda5 = models.LdaModel.load('./timewindow_in3/_2008-2009-2010lda_model')
    lda6 = models.LdaModel.load('./timewindow_in3/_2010-2011-2012lda_model')
    lda7 = models.LdaModel.load('./timewindow_in3/_2012-2013-2014lda_model')
    lda8 = models.LdaModel.load('./timewindow_in3/_2014-2015-2016lda_model')
    lda9 = models.LdaModel.load('./timewindow_in3/_2016-2017lda_model')

    # 读取phi矩阵，用于全矩阵运算
    phi1 = np.array(lda1.expElogbeta)
    phi2 = np.array(lda2.expElogbeta)
    phi3 = np.array(lda3.expElogbeta)
    phi4 = np.array(lda4.expElogbeta)
    phi5 = np.array(lda5.expElogbeta)
    phi6 = np.array(lda6.expElogbeta)
    phi7 = np.array(lda7.expElogbeta)
    phi8 = np.array(lda8.expElogbeta)
    phi9 = np.array(lda9.expElogbeta)

    # 截取topic前40个进行计算
    show1 = lda1.show_topics(num_words=40, formatted=False)
    topic_dict1 = dict(show1)
    show2 = lda2.show_topics(num_words=40, formatted=False)
    topic_dict2 = dict(show2)
    show3 = lda3.show_topics(num_words=40, formatted=False)
    topic_dict3 = dict(show3)
    show4 = lda4.show_topics(num_words=40, formatted=False)
    topic_dict4 = dict(show4)
    show5 = lda5.show_topics(num_words=40, formatted=False)
    topic_dict5 = dict(show5)
    show6 = lda6.show_topics(num_words=40, formatted=False)
    topic_dict6 = dict(show6)
    show7 = lda7.show_topics(num_words=40, formatted=False)
    topic_dict7 = dict(show7)
    show8 = lda8.show_topics(num_words=40, formatted=False)
    topic_dict8 = dict(show8)
    show9 = lda9.show_topics(num_words=40, formatted=False)
    topic_dict9 = dict(show9)


    # topic_dict100 = dict(show100)
    # print models.interfaces.matutils.cossim(topic_dict[0],topic_dict[1])
    # print cossim(phi[0],phi[1])
    #
    # print models.interfaces.matutils.cossim(topic_dict[2],topic_dict[1])
    # print cossim(phi[2],phi[1])

    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("sheet 1")
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict1[i], topic_dict2[j])
            sheet.write(i+1, j+1, str(sim1))
            sim2 = cossim(phi1[i], phi2[j])
            sheet.write(i + 1, j + 14, str(sim2))
            # print(cossim(phi1[i],phi2[j]))

    sheet = wbk.add_sheet('sheet 2')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict2[i], topic_dict3[j])
            sheet.write(i+1, j+1, str(sim1))
            sim2 = cossim(phi2[i], phi3[j])
            sheet.write(i + 1, j + 14, str(sim2))

    sheet = wbk.add_sheet('sheet 3')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict3[i], topic_dict4[j])
            sheet.write(i + 1, j + 1, str(sim1))
            sim2 = cossim(phi3[i], phi4[j])
            sheet.write(i + 1, j + 14, str(sim2))

    sheet = wbk.add_sheet('sheet 4')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict4[i], topic_dict5[j])
            sheet.write(i + 1, j + 1, str(sim1))
            sim2 = cossim(phi4[i], phi5[j])
            sheet.write(i + 1, j + 14, str(sim2))

    sheet = wbk.add_sheet('sheet 5')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict5[i], topic_dict6[j])
            sheet.write(i + 1, j + 1, str(sim1))
            sim2 = cossim(phi5[i], phi6[j])
            sheet.write(i + 1, j + 14, str(sim2))

    sheet = wbk.add_sheet('sheet 6')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict6[i], topic_dict7[j])
            sheet.write(i + 1, j + 1, str(sim1))
            sim2 = cossim(phi6[i], phi7[j])
            sheet.write(i + 1, j + 14, str(sim2))

    sheet = wbk.add_sheet('sheet 7')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict7[i], topic_dict8[j])
            sheet.write(i + 1, j + 1, str(sim1))
            sim2 = cossim(phi7[i], phi8[j])
            sheet.write(i + 1, j + 14, str(sim2))

    sheet = wbk.add_sheet('sheet 8')
    for i in range(10):
        for j in range(10):
            print(i, j)
            sim1 = models.interfaces.matutils.cossim(topic_dict8[i], topic_dict9[j])
            sheet.write(i + 1, j + 1, str(sim1))
            sim2 = cossim(phi8[i], phi9[j])
            sheet.write(i + 1, j + 14, str(sim2))

    wbk.save("topic_evolution2.xls")


