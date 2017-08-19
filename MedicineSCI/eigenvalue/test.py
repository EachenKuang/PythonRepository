# -*- coding:utf-8 -*-
# !/usr/bin/python2
import xlrd
import re
from MedicineSCI.InterfaceSQL import *
import numpy as np
import pandas as pd
#加入以下3行是为了防止发生UnicodeEncodeError
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )



# 计算  学科交叉性
# 参考文献 CR
# 所属分类 SC（数据库中保留SC，WC为null，先用SC）
# 需要用到的文件  ESIMasterJournalList.xlsx
# 每个paperID 对应一个主题，对每个主题使用下面这个函数
# 传入参数为一个包含paperID的List
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

            #     referenceString = str(CR)
            #     stringList = referenceString.split(",")
            #     for string in stringList:
            #         if (re.search("^[A-Z\s]*-*[A-Z\s]*$",string)):
            #             list.append(string.strip())
            # paperIDWithList[id] = list
                referenceString = str(CR)
                stringList = referenceString.split(";")
                for string in stringList:
                    # if (re.search("^[A-Z\s]*-*[A-Z\s]*$",string)):
                    #     list.append(string.strip())
                    if (string.split(',').__len__() > 3):
                        list.append(string.split(',')[2].strip())
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

    with open("paper_CR_test.txt",'a') as write:
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


# Interdisciplinary(range(1, 8283))
Interdisciplinary(range(1, 13679))
