# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 内容抓取
# Other:
# '''
from stanfordcorenlp import StanfordCoreNLP
from collections import OrderedDict
from file2dict import file2dict
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

nlp = StanfordCoreNLP(r'D:\\stanford-corenlp-full-2017-06-09', lang='zh')

class Result(object):

    def __init__(self):
        self.theme = ''
        self.sentiment_word = ''
        self.sentiment_analysis = ''

def test():
    """
    测试使用
    :return:
    """

    sentence = '给超级差差差评！无良商家！垃圾！京东也有如此坑人的商家，无语！底坐里面就是用沙子倒成的，用了三天就变成这个样子&hellip;&hellip;请大家看图吧！希望可以帮到大家看清这家无良商家的劣质产品！！！'
    sentence = '试用过了，很满意，外观设计很漂亮，人操作起来很方便的，价格也实惠，挺满意的！'
    sentence = '是我见过声音最大的，音质最好的手机。其他的手机我觉得声音真的太小声了。 比我原来的1200万像素的手机拍出来的效果感觉要清晰很多。 非常流畅不卡顿'
    sentence = '发货真的好快 味道是很熟悉的那种 但是不算高档不算亲和的味道 滋润不错 持香也不错'# print nlp.word_tokenize(sentence)     #获取分词
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
            word_list.append(key)
            analysis_list.append(file_dict[key.encode('utf-8')])
            theme_list.append(find_nearest_theme(offset, pos_tag))
    return ';'.join(theme_list)+';,'+';'.join(word_list)+';,'+';'.join(analysis_list)+';'
    # return theme_list, word_list, analysis_list

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
            while pos_tag[offset][1] != 'PU':
                if pos_tag[offset][1].startswith('N'):
                    theme = pos_tag[offset][0]
                    break
                offset += 1

            offset = start_offset
            while pos_tag[offset][1] != 'PU':
                if pos_tag[offset][1].startswith('N'):
                    theme = pos_tag[offset][0]
                    break
                offset -= 1

    except Exception, e:
        print 'str(Exception):\t', str(Exception)

    return theme

def main():

    with open('data/in.csv', 'r') as reader, \
            open('out/out.csv', 'a') as writer:
        # 读取信息
        file_content = reader.readlines()
        for index in range(20000):
            print index
            sentence = file_content[index].split(',')[1].strip()

            temp = str(index+1)+','+sentence+','+process(sentence)+'\n'
            print temp
            writer.write(temp)

        # 打印信息



if __name__ == '__main__':
    main()




