# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.10.20
# Goal: 测试
# Other:
# '''
import jieba
import nltk
a = jieba.cut('row_id,content,theme,sentiment_word,sentiment_anls,备注说明\
1,给奶奶买的，效果不错，厂家服务也好，给好评[追评],效果;厂家服务;NULL;,不错;好;好评;,1;1;1;,主题词，情感词，情感值一一对应；主题词没有则标为NULL\
2,用了好几个了，很好,NULL;,很好;,1;,\
3,要得要得要得,,,,无意义的评论，直接置空\
4,用了一个月就坏了，太浪费了,NULL;NULL;,坏;浪费;,-1;-1;,主题词没有，但对应的情感词不同时，主题词一一标为NULL\
5,挺好挺好挺好挺好挺好,NULL;,挺好;,1;,主题词，情感词，情感值均相同时，保留一个\
6,外观小巧且时尚,外观;NULL;,小巧;时尚;,1;1;,一个短句中如果出现一个主题词对应多个情感词，则主题词与最近的情感词匹配，剩下的主题词标为NULL\
7,没送，为什么没送？,,,,有情感倾向，但没有明确的情感词时，都置空。\
8,黑人牙膏好用？,黑人牙膏;,好用;,1;,标点符号不作为情感判断。\
9,买了好几次了 觉得面膜挺好的  就是不知道里边德成分好不好,面膜;,挺好;,1;,好不好等表示疑问或反问的词不作为情感词判断')
print(' '.join(a))


t = nltk.word_tokenize('clock on Thursday morning')

print(t)