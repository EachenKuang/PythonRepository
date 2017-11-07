# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 基于主题的情感分析比赛（使用StanfordNLP）
# Other:
# '''
import nltk
from stanfordcorenlp import StanfordCoreNLP
from collections import OrderedDict
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

nlp = StanfordCoreNLP(r'D:\\stanford-corenlp-full-2017-06-09', lang='zh')

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

def test():
    """

    测试使用
    :return:
    """

    sentence = '给超级差差差评！无良商家！垃圾！京东也有如此坑人的商家，无语！底坐里面就是用沙子倒成的，' \
               '用了三天就变成这个样子&hellip;&hellip;请大家看图吧！希望可以帮到大家看清这家无良商家的劣质产品！！！'
    sentence = '试用过了，很满意，外观设计很漂亮，人操作起来很方便的，价格也实惠，挺满意的！'
    sentence = '是我见过声音最大的，音质最好的手机。其他的手机我觉得声音真的太小声了。 ' \
               '比我原来的1200万像素的手机拍出来的效果感觉要清晰很多。 非常流畅不卡顿'
    sentence = '发货真的好快 味道是很熟悉的那种 但是不算高档不算亲和的味道 滋润不错 持香也不错'

    # print nlp.word_tokenize(sentence)     #获取分词
    # print nlp.pos_tag(sentence)           #获取词性标注
    # print nlp.ner(sentence)               #获取命名实体识别结果
    # print nlp.parse(sentence)
    # print nlp.dependency_parse(sentence)

    words = nlp.word_tokenize(sentence)
    print ' '.join(words)

    pos_tag = nlp.pos_tag(sentence)
    # pos_dict = OrderedDict(pos_tag)
    # for key, value in pos_dict.iteritems():
    #     print key + ' ' + value
    # print pos_tag

    for offset, (key, value) in enumerate(pos_tag):
        print offset, key, value

    for offset, (key, value) in enumerate(pos_tag):
        if value.__eq__('JJ') or value.__eq__('VA'):
            print offset, key, value

def process(sentence):
    """
    处理评论句子
    :param sentence:
    :return:
    """

    """
    找标注了JJ和VA的词，然后找到其对应的NN
    VA前面有VV，需要加上VV 如'不算'
    VA前面有AD，需要加上AD 如'最'
    PU 标点分长句子成短句
    """

    # 获取 part of speech
    pos_tag = nlp.pos_tag(sentence)
    # print pos_tag

    # 保存主题、情感关键词、情感正负面
    theme_list = []
    word_list = []
    analysis_list = []

    # 遍历句子分词结构
    file_dict = file2dict()
    for offset, (key, value) in enumerate(pos_tag):
        # print offset, key, value
        if key in file_dict.iterkeys():
            if key.encode('utf-8') == '次':
                continue
            word_list.append(key)
            analysis_list.append(file_dict[key.encode('utf-8')])
            theme_list.append(find_nearest_theme(offset, pos_tag))
    # return ';'.join(theme_list)+';,'+';'.join(word_list)+';,'+';'.join(analysis_list)+';'
    return theme_list, word_list, analysis_list

def find_nearest_theme(offset, pos_tag):
    """
    找到最近的主题词
    :param offset:
    :param pos_tag:
    :return:
    """
    theme = 'NULL'
    try:
        if pos_tag[offset][1] == 'JJ':
            # 向后寻找
            offset += 1
            while pos_tag[offset][1] != 'PU':
                if pos_tag[offset][1].startswith('N'):
                    theme = pos_tag[offset][0]
                    break
                offset += 1

        elif pos_tag[offset][1] == 'VA':
            # 向前寻找
            offset -= 1
            while pos_tag[offset][1] != 'PU':
                if pos_tag[offset][1].startswith('N'):
                    theme = pos_tag[offset][0]
                    break
                offset -= 1
        else:
            # 前后一起找
            start_offset = offset
            offset += 1
            while pos_tag[offset][1] != 'PU':
                if pos_tag[offset][1].startswith('N'):
                    theme = pos_tag[offset][0]
                    break
                offset += 1

            offset = start_offset
            offset -= 1
            while pos_tag[offset][1] != 'PU':
                if pos_tag[offset][1].startswith('N'):
                    theme = pos_tag[offset][0]
                    break
                offset -= 1

    except Exception, e:
        print 'str(Exception):\t', str(Exception)

    return theme

def main():
    now = str(datetime.now())
    now = '.'.join(now.split()).replace(':', '-')
    with open('data/in.txt', 'r') as reader, \
            open('out/out_nlp'+str(now)+'.csv', 'w') as writer:
        # 读取信息
        file_content = reader.readlines()
        for index in range(20000):
            print index
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
            print temp
            writer.write(temp.encode('GBK'))

        # 打印信息


if __name__ == '__main__':
    main()



