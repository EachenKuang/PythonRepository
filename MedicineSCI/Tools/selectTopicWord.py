# -*- coding:utf-8 -*-
# !/usr/bin/python2

#输入一个phi矩阵
#输出每个topic的前20词。
import numpy as np
import pandas as pd

def phi2subset(phi_path, topic_num):

    wordlist = []  # 保存 index - word
    index_word_file = open("termList.txt")
    for line in index_word_file:
        word = line.strip().split(" [")[0]  # 只取word
        wordlist.append(word)
    print wordlist.__len__()

    df = pd.read_csv(filepath_or_buffer=phi_path, sep='\t', header=None, names=wordlist, index_col=False)

    # article_topic = df.idxmax(axis=1)  # 每篇文献属于的主题
    for i in range(0,10):
        topic = []
        max = df.idxmax()
        print max
        #  topic
        # df.d
    max = df.idxmax()
    print max
    # file = open("topic_word_list_in_word.txt", 'w')


# phi2subset('lda_1000.phi',10)
# arraylist = []
# N_max_in_list([10.0,11.0,1.0,2.3,3.4,5.3,53.5,25.5,355.35,3535.3,555,4,33.2],10,[])

#用于从list中提取前N个最大的值以及其下标，保存在一个字典中
#arraylist  输入的List
#n          提取前n个
#equip_list 保存被占用的下标
def N_max_in_list(phi_path,  n):


    wordlist = []  # 保存 index - word
    index_word_file = open("termList.txt")
    for line in index_word_file:
        word = line.strip().split(" [")[0]  # 只取word
        wordlist.append(word)
    print wordlist.__len__()


    # df_pd = pd.read_csv(filepath_or_buffer=phi_path, sep='\t', header=None,  index_col=False)
    # df_np = df_pd.as_matrix()
    # print df_pd.shape
    df_np = np.loadtxt(phi_path)
    for i in range(0,10):
        print df_np[i].__len__()

    topics = [[] for i in range(10)]
    for k in range(0, n):
        # topic_n = []
        # print "topic" + str(k)
        for i in range(0, 10):
            max_index = df_np[i].argmax()
            print df_np[i].max()
            topics[i].append(wordlist[max_index])
            # topic_n.append(max_index)
            # df_np[0][max_index] = -1
            # 将每一列的对应都置为-1

            for j in range(0, 10):
                df_np[j][max_index] = -1

    ''' 换一种排列方式 '''
    # topic = []
    # for k in range(0,10):
    #     topic_n = []
    #     print "topic"+str(k)
    #     for i in range(0,n):
    #         max_index = df_np[k].argmax()
    #         print df_np[k].max()
    #         topic_n.append(wordlist[max_index])
    #         # topic_n.append(max_index)
    #         # df_np[0][max_index] = -1
    #         #将每一列的对应都置为-1
    #         topics = [[] for i in range(10)]
    #         for k in range(0, n):
    #             # topic_n = []
    #             # print "topic" + str(k)
    #             for i in range(0, 10):
    #                 max_index = df_np[k].argmax()
    #                 print df_np[k].max()
    #                 topics[i].append(wordlist[max_index])
    #                 # topic_n.append(max_index)
    #                 # df_np[0][max_index] = -1
    #                 # 将每一列的对应都置为-1
    #
    #                 for j in range(0, 10):
    #                     df_np[j][max_index] = -1
    #             topic.append(topic_n)
    #         for j in range(0, 10):
    #             df_np[j][max_index] = -1
    #     topic.append(topic_n)

    for i in range(0,10):
        print "topic"+str(i)+":"
        print topics[i]

                # array = np.array(arraylist, dtype=float)
    # max_index = array.argmax()
    # array.__len__()
    # array[max_index] = -1





N_max_in_list('lda_1000.phi',20)