# -*- encoding:utf-8 -*-
#用于对文件排序
dictIDF = {}
with open('./FilterDataFiles/IDF.txt','r') as read,  open("./FilterDataFiles/IDF_sort[only word].txt",'a') as write:
    for line in read:
        line = line.strip()
        result = line.split()
        frequence = float(result[-1])
        key = " ".join(line.split()[:-2])
        #print key
        dictIDF[key] = frequence
    sort_dict = sorted(dictIDF.items(), key=lambda d:d[1])
    for key,value in sort_dict:
        write.write(key+'\n')

    read.close()
    write.close()