#-*- coding:utf-8 -*-
#-------------------------------------------------------------
#
#
#
from InterfaceSQL import MSSQL
import os
import re


#从文件中读取停用词，保存在一个list中
def filterByStopWord(path,stopWords):

#   #文件存储格式为每一行一个term
    with open(path,"r") as read:
        for line in read:
            line = line.strip()
            stopWords.append(line)
    return stopWords


def main():
    ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")

#   #用于储存1.txt 格式的 files 数字表示其在数据库中的paperID
    folder = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\SecondPartDataFiles"

#   #用于储存停用词表，可以有多个
    stopWordsFold = "D:\\Kuangyichen\\PythonRepository\\MedicineSCI\\stopWordsFiles\\"
    files = os.listdir(stopWordsFold)

#   #保存停用词列表
    stopWords = []

#   #初始化停用词列表
    for file in files:
        filterByStopWord(stopWordsFold+file,stopWords)
    print  stopWords
    for paperID in range(1,8284):
        # resList = ms.ExecQuery("SELECT standard,type FROM data4 where paperID = '" + str(paperID)+"'")
        resList = ms.ExecQuery("SELECT word,type FROM Table_2016 where paperID = '" + str(paperID) + "'")
        fileName = folder+"\\"+str(paperID)+".txt"
        print paperID
        with open(fileName,"a") as writer:
            # for standard,type in resList:
            #     #print standard
            #     if (standard in stopWords) or (re.search("^\d*$|^\\.*$|^\%.*$|^\*.*$",standard)):
            #         print standard + "delete"
            #     else:
            #         writeString = standard+" "+type+"\n"
            #         writer.write(writeString)
            for word,type in resList:
                #print standard
                if (word in stopWords) or (re.search("^\d*$|^\\.*$|^\%.*$|^\*.*$|^\d*%$|^\d*/\d*$|^/.*$",word)):
                    print word + "delete"
                else:
                    writeString = word+" "+type+"\n"
                    writer.write(writeString)

if __name__ == '__main__':
    main()



