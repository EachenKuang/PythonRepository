#-*- coding:utf-8 -*-
# 将数据库中WordList中相同词根、单复数词合并统一
#
#
#
from InterfaceSQL import MSSQL #调用自己封装的接口
from collections import defaultdict
global null
null = None

#读取合并词表，保存在一个字典中
def readDict(filePath):
    dict = defaultdict(str)
    with open(filePath) as read:
        value = None
        for line in read:
            line = line.strip()
            if value == None:
                if line.startswith("**"):
                    value = line[2:]
                else:
                    pass
            else:
                if line.startswith("**"):
                    value = line[2:]
                elif line:
                    key = line.split(" ", 2)[2]
                    key = key[1:len(key) - 1]
                    dict[key] = value
    return  dict


def main():
    ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    dict = readDict("C:\\Users\\xmu\\Desktop\\Keyword.the")
    dictWord = defaultdict(str)
    print dict
    print '\n'
    resList = ms.ExecQuery("SELECT id,word FROM data4 where standard is NULL")
    #print resList
    for (id,word) in resList:
        if  dict.has_key(word):
           dictWord[id] = dict[word]
        else:
           dictWord[id] = word
        #print(dictWord[id])
        #print("----------------------------")
        sqlString = "update data4 set standard='"+ dictWord[id] +"'where id ="+str(id)

        ms.ExecNonQuery(sqlString)
        # if id%10000==0:
        #     print(id)
        #     print(' finished')
        # print '\n'

if __name__ == '__main__':
    main()
