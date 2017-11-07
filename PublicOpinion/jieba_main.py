# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 基于主题的情感分析比赛（使用jieba）
# Other:
# '''

from datetime import datetime
import jieba
import jieba.posseg as pseg
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def file2dict():
    file_path = "data1/training.csv"
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

def process(sentence):
    """
    处理评论句子
    :param sentence:
    :return:
    """

    """
    n 名词
    ns 特有名词
    v 动词
    eng 英语
    r
    d 副词
    a 形容词
    y 语气词
    """
    # 读取用户自定义词库
    jieba.load_userdict("dict/dictforthem.txt")
    # jieba.initialize()
    # 分词获得标注
    seg_list = pseg.lcut(sentence)
    # 打印查看分词标注内容
    print(' '.join([w.word + w.flag for w in seg_list]))
    # print seg_list
    # 保存主题、情感关键词、情感正负面
    theme_list = []
    word_list = []
    analysis_list = []

    # 遍历句子分词结构
    file_dict = file2dict()
    for offset, (key, value) in enumerate(seg_list):
        # print offset, key, value
        if key in file_dict.iterkeys():
            if key.encode('utf-8') == '次':
                continue
            word_list.append(key)
            analysis_list.append(file_dict[key.encode('utf-8')])
            theme_list.append(find_nearest_theme(offset, seg_list))
    return theme_list, word_list, analysis_list

def find_nearest_theme(offset, pos_tag):
    """
    找到最近的主题词
    规则：
    主题词 是 a 先找最近的 n，如果不存在n，就找相邻的v
    :param offset:
    :param pos_tag:
    :return:
    """

    theme = 'NULL'
    length_forward = 100
    try:
        temp = offset+1
        while not(pos_tag[temp].word in ['！', '，', '.']):
            # if pos_tag[temp].flag.startswith('n'):
            if pos_tag[temp].flag == 'n':
                theme = pos_tag[temp].word
                length_forward = temp-offset
                break
            temp += 1
    except Exception as e:
        print('str(Exception):\t', str(e))

    try:
        temp = offset-1
        while not(pos_tag[temp].word in ['！', '，', '.']):
            # if pos_tag[temp].flag.startswith('n'):
            if pos_tag[temp].flag == 'n':
                length_back = offset-temp
                if length_forward > length_back:
                    theme = pos_tag[temp].word
                break
            temp -= 1

    except Exception as e:
        print('str(Exception):\t', str(e))

    return theme

def run():
    now = str(datetime.now())
    now = '.'.join(now.split()).replace(':', '-')
    with open('data/in.txt', 'r') as reader, \
            open('out/jieba_out'+str(now)+'.csv', 'w') as writer:
        # 读取信息
        file_content = reader.readlines()
        for index in range(20000):

            sentence = file_content[index].strip()
            theme_list, word_list, analysis_list = process(sentence)

            theme = ''
            word = ''
            analysis = ''
            if theme_list.__len__() > 0:
                theme = ';'.join(theme_list)+';'
            if word_list.__len__() > 0:
                word = ';'.join(word_list)+';'
            if analysis_list.__len__() > 0:
                analysis = ';'.join(analysis_list) + ';'
            temp = str(index+1)+','+sentence+','+theme+','+word+','+analysis+'\n'
            print(temp)
            writer.write(temp)

if __name__ == '__main__':
    run()




