# -*- coding:utf-8 -*-
# !/usr/bin/python2
#将得出的矩阵转化为topic
import pandas as pd
from MedicineSCI.InterfaceSQL import MSSQL

def theta2subset(theta_path, topic_num):
    df = pd.read_csv(filepath_or_buffer=theta_path, sep='\t', header=None, names=range(1, topic_num+1), index_col=False)
    article_topic = df.idxmax(axis=1)   # 每篇文献属于的主题
    file = open("topic_doucment_list.txt",'w')
    for i in range(1, topic_num+1):
        lis = list(article_topic[article_topic == i].index + 1)
        new_lis = [lis[j]+7120 for j in range(0,lis.__len__())]#需要调整
        file.write("topic"+str(i)+"="+str(new_lis)+"\n")


def phi2subset(phi_path, topic_num):
    df = pd.read_csv(filepath_or_buffer=phi_path, sep='\t', header=None, index_col=False)
    df = df.T
    article_topic = df.idxmax(axis=1)  # 每篇文献属于的主题
    file = open("topic_word_list_in_word.txt", 'w')

    index_word_file = open("termList.txt")
    wordlist = []  #保存 index - word
    for line in index_word_file:
        word = line.strip().split(" [")[0]  #只取word
        wordlist.append(word)
    print wordlist.__len__()

    # MH_file = open("MH_word.txt",'w')
    ms = MSSQL(host="localhost:59318", user="eachen", pwd="123456", db="mydata")
    resultList = ms.ExecQuery("SELECT MH FROM MeshStructure")
    word_in_list = []
    for (MH,) in resultList:
        word_in_list.append(str(MH))
        # MH_file.write(str(MH)+"\n")



    for i in range(0, topic_num):
        lis = list(article_topic[article_topic == i].index)
        lis_word = [wordlist[j] for j in lis]
        lis_in_word = list(set(lis_word).intersection(set(word_in_list)))
        # file.write("topic"+str(i+1)+":"+str(lis_word)+"\n")
        file.write("topic"+str(i+1)+"="+str(lis_in_word)+"\n")


theta2subset("lda_1000.theta", 10)
phi2subset("lda_1000.phi", 10)
