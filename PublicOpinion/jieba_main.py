# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 基于主题的情感分析比赛（使用jieba）
# Other:
# '''

from file2dict import file2dict
from datetime import datetime
import jieba
import jieba.posseg as pseg
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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
    jieba.initialize()
    # 分词获得标注
    seg_list = pseg.lcut(sentence)
    # 打印查看分词标注内容
    print ' '.join([w.word + w.flag for w in seg_list])
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
        while pos_tag[temp].flag != 'x':
            if pos_tag[temp].flag.startswith('n'):
                theme = pos_tag[temp].word
                length_forward = temp-offset
                break
            temp += 1
    except Exception, e:
        print 'str(Exception):\t', str(Exception)

    try:
        temp = offset-1
        while pos_tag[temp].flag != 'x':
            if pos_tag[temp].flag.startswith('n'):
                length_back = offset-temp
                if length_forward > length_back:
                    theme = pos_tag[temp].word
                break
            temp -= 1

    except Exception, e:
        print 'str(Exception):\t', str(Exception)

    return theme

def run():
    now = str(datetime.now())
    now = '.'.join(now.split()).replace(':', '-')
    with open('data/in.txt', 'r') as reader, \
            open('out/out'+str(now)+'.csv', 'w') as writer:
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
            writer.write(temp)

        # 打印信息

def main():
    run()

if __name__ == '__main__':
    main()




