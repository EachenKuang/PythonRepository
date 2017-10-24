# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.10.20
# Goal: 将文件转化为字典
# Other:
# '''

def file2dict():
    file_path = "data/training.csv"
    list_word = []
    list_score = []
    with open(file_path, 'r') as read_file:
        read_file.readline()  # 读取第一行
        file_content = read_file.readlines()
        for line in file_content:

            if line == ',\n':
                continue

            line = line.strip()  # 去除'\n'
            words = line.split(',')[0].split(';')[:-1]
            scores = line.split(',')[1].split(';')[:-1]
            for word in words:
                list_word.append(word)
            for score in scores:
                list_score.append(score)

    my_dict = zip(list_word, list_score)
    dict_final = dict(my_dict)
    # print dict(my_dict)
    # print dict_final.__len__()
    # for key, value in dict_final.iteritems():
    #     print key, value

    return dict_final

