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
sys.setdefaultencoding("utf-8")


# 计算  学科交叉性
# 参考文献 CR
# 所属分类 SC（数据库中保留SC，WC为null，先用SC）
# 需要用到的文件  ESIMasterJournalList.xlsx
# 每个paperID 对应一个主题，对每个主题使用下面这个函数
# 传入参数为一个包含paperID的List
def Interdisciplinary(paperIDs):

    JournalList = {}  #用于保存期刊对应所属类别的字典
    paperIDWithList = {} #用于保存每篇期刊ID对应的引用期刊LIST
    paperIDWithClass = {} #用于保存每篇期刊ID对应的分类LIST
    paperIDWithList = []
    paperIDWithClass = []

   #读取 ESIMasterJournalList.xlsx 文件 将表存在字典中
    data = xlrd.open_workbook("ESIMasterJournalList.xlsx", "r")
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    for i in range(0, nrows):
        rowValues = table.row_values(i)  # 某一行数据
        for item in rowValues[0:3]:
            JournalList[str(item)] = str(rowValues[-1])
    # print(JournalList)


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
                    # if (re.search("^[A-Z\s]*-*[A-Z\s]*$",string)):
                    #     list.append(string.strip())
                    if(string.split(',').__len__()>3):
                        list.append(string.split(',')[2].strip())
            paperIDWithList.append(list)
            #print list,list.__len__()

            for li in list:
                if JournalList.has_key(li):
                    list2.append(JournalList[li])
            paperIDWithClass.append(list2)
            print paperIDWithClass[id]

        except BaseException, Argument: #出现异常跳过，在CR会存在一些非编码字符
            print Argument

    # 保存paperID 对应的 期刊 用分号隔开

    with open("paper_CR_new.txt", 'w') as write:
        for i in range(1, 6):
            write.write(str(i)+";")
            for string in paperIDWithClass[i-1]:
                write.write(string+";")
            write.write("\n")

    print "---------------------------------"

    # listAll = []
    # for ids in range(1, 6):
    #     tempList = paperIDWithClass[ids-1]
    #     for string in tempList:
    #         #print type(string)
    #         if not listAll.__contains__(str(string)):
    #             listAll.append(string)
    # print listAll
    # print "---------------------------------"
    # print paperIDWithClass.keys()


Interdisciplinary(range(1, 6))



