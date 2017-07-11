# -*- encoding: utf-8 -*-
import logging
from gensim import models
from gensim import corpora
import numpy as np
import os
from pprint import pprint

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def save_dict():
    # open file()
    data_path_in_folds = "D:\\Kuangyichen\\JavaRepository\\LDAGibbsSampling-master\\data\\LdaOriginalDocs\\"
    data_in_folds_filenames = os.listdir(data_path_in_folds)
    # data_in_folds_filenames.sort()
    texts = []
    for date_in_file in data_in_folds_filenames:
        with open(data_path_in_folds+date_in_file,'r') as doc:
            text = []
            for line in doc:
                text.append(line.strip())
        texts.append(text)

    dictionary = corpora.Dictionary(texts)
    dictionary.save('./tmp/all_doucment.dict.txt')
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./tmp/corpus.mm', corpus)
    dictionary.filter_extremes()

# v1 = [(1,2),(2,3)]
# v2 = [(1,4),(2,5)]

#v1,v2输入的形式为 [(index1,value1),(index2,value2),……]
# cos_sum = models.interfaces.matutils.cossim(v1,v2)
# print cos_sum
# dictionary = corpora.Dictionary.load('./tmp/all_doucment.dict')
# corpus = corpora.MmCorpus('./tmp/corpus.mm')


# corpora.BleiCorpus.serialize('./tmp/corpus.blei', corpus)
def load():
    dictionary = corpora.Dictionary.load('./tmp/all_doucment.dict')
    corpus = corpora.BleiCorpus('./tmp/corpus.blei')

    lda = models.LdaModel(corpus,id2word=dictionary,num_topics=10,per_word_topics=True)
    print lda.id2word
    print '----------------------------------------------------'
    list = lda.get_document_topics(corpus,per_word_topics=True)
    pprint(list[2])



# print dictionary.token2id
# print dictionary.id2token

# lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=10)
# print lda_model.show_topics(5,10)
# print "--------------------------------------"
# lda_model.print_topics(10,10)
# print lda_model.get_document_topics()


# hdp_model = models.HdpModel(corpus, id2word=dictionary)
#
# for i in range(0, 10):
#      hdp_model.show_topic(i, 50, True, True)
#
# with open('./out/topic1.txt', 'a') as write:
#     write.write((str)(hdp_model.show_topics(10, 50, True, True)))
# lda_model = hdp_model.suggested_lda_model()
# print lda_model.num_topics
# pprint(hdp_model.show_topics(10,10,True))

# models.interfaces.matutils.cossim()

# dictionary = corpora.Dictionary.load('./tmp/all_doucment.dict')
# dict1 = corpora.Dictionary('')
# dict2 = corpora.Dictionary('')  # ids not compatible with dict1!
# dict2_to_dict1 = dict1.merge_with(dict2)
# # now we can merge corpora from the two incompatible dictionaries into one
# merged_corpus =corpora..chain(some_corpus_from_dict1, dict2_to_dict1[some_corpus_from_dict2])itertools
# corpora.Dictionary.abstracts
# models.interfaces.matutils
# models.interfaces.utils.
def cossim(a,b):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for x, y in zip(a, b):
        dot_product+=x*y
        normA += x**2
        normB += y**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product/((normA*normB)**0.5)
'''
lda1 = models.LdaModel.load('./temp/_2000-2001lda_moedel')
lda2 = models.LdaModel.load('./temp/_2002-2003lda_moedel')
lda3 = models.LdaModel.load('./temp/_2004-2005lda_moedel')
lda4 = models.LdaModel.load('./temp/_2006-2007lda_moedel')

phi1 = np.array(lda1.expElogbeta)
phi2 = np.array(lda2.expElogbeta)
phi3 = np.array(lda3.expElogbeta)
phi4 = np.array(lda4.expElogbeta)

# phi1 = np.array(lda1.state.sstats)
# phi2 = np.array(lda2.state.sstats)

show1 = lda1.show_topics(num_words=30,formatted=False)
# show100 = lda.show_topics(num_words=100,formatted=False)
topic_dict1 = dict(show1)

show2 = lda2.show_topics(num_words=50,formatted=False)
# show100 = lda.show_topics(num_words=100,formatted=False)
topic_dict2 = dict(show2)

show3 = lda3.show_topics(num_words=50,formatted=False)
# show100 = lda.show_topics(num_words=100,formatted=False)
topic_dict3 = dict(show3)

show4 = lda4.show_topics(num_words=50,formatted=False)
# show100 = lda.show_topics(num_words=100,formatted=False)
topic_dict4 = dict(show4)
# topic_dict100 = dict(show100)
'''
# print models.interfaces.matutils.cossim(topic_dict[0],topic_dict[1])
# print cossim(phi[0],phi[1])
#
# print models.interfaces.matutils.cossim(topic_dict[2],topic_dict[1])
# print cossim(phi[2],phi[1])
'''
for i in range(10):
    for j in range(10):
        print(i,j)
        print models.interfaces.matutils.cossim(topic_dict1[i], topic_dict2[j])
        # print models.interfaces.matutils.cossim(topic_dict100[i], topic_dict100[j])
        print(cossim(phi1[i],phi2[j]))
for i in range(10):
    for j in range(10):
        print(i,j)
        print models.interfaces.matutils.cossim(topic_dict3[i], topic_dict4[j])
        # print models.interfaces.matutils.cossim(topic_dict100[i], topic_dict100[j])
        print(cossim(phi3[i],phi4[j]))
'''
# topic = lda.show_topics(num_topics=10, num_words=40,formatted=False)
# di = dict(topic)
# print di
# models.LdaModel.show_topics()

# dictionary = corpora.Dictionary.load('./temp/all_doucment.dict')
# dictionary.save_as_text('./temp/dict_old', sort_by_word=True)
# dictionary.filter_extremes(no_below=10, no_above=0.5, keep_n=None, keep_tokens=None)
# dictionary.save_as_text('./temp/dict', sort_by_word=True)
# dictionary.save('./temp/dict.dict')

#------------------------------------------------------------------------
'''
dictionary = corpora.Dictionary.load('./temp/dict.dict')
print dictionary.id2token
print dictionary.token2id
# corpora.Dictionary.items()
# dict.iterkeys()
with open("item_list.txt",'w')as ww:
    for i in dictionary.token2id.iterkeys():
        ww.write(i+'\n')
'''

lda1 = models.LdaModel.load('./temp/_2000-2001lda_moedel')
show = lda1.show_topics(num_words=400, formatted=False)
dict_show = dict(show)
#dict_show[i] 第i个主题
list = []
for i in dict(dict_show[0]).iterkeys():
    list.append(str(i))
    print i
print list
set(list)
