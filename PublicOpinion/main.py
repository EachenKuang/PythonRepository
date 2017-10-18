# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 内容抓取
# Other:
# '''
from stanfordcorenlp import StanfordCoreNLP
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

nlp = StanfordCoreNLP(r'D:\\stanford-corenlp-full-2017-06-09', lang='zh')

sentence = '热水器加热时间太长，安装费太贵，预留太阳能口摆设，根本用不到，没有水位指示器，加满热水的指示灯放在了最侧面，不方便用户看指示灯，必须斜着看才能看到，'
sentence = '很满意，噪音控制很好，很安静，制冷效果不错，制热还没试。安装师傅很尽心，比格力的安装师傅服务好太多!'
# print nlp.word_tokenize(sentence)
# print nlp.pos_tag(sentence)
# print nlp.ner(sentence)
# print nlp.parse(sentence)
# print nlp.dependency_parse(sentence)

words =  nlp.word_tokenize(sentence)
print words

for word in words:
    print word