# -*- coding: utf-8 -*-
from collections import OrderedDict
from gensim import models,corpora


def print_topic(lda_list):
    name = ['2012-2013', '2013-2014', '2014-2015']
    # name = ['1999-2000', '2001-2002', '2003-2004']
    for j in range(3):
        show = lda_list[j].show_topics(num_words=40, formatted=False)
        topic_dict = OrderedDict(show)
        with open('Output/' + name[j] + 'topic_format_4', 'w') as temp:
            # temp.write(str(show))
            for i in range(10):
                # topic_dict[i]  # topic i 中的对应字段 list
                topic_dict_each = OrderedDict(topic_dict[i])
                temp.write('topic' + str(i) + '\n')
                for id, value in topic_dict_each.iteritems():
                    temp.write(id + ' ' + str(value) + '\n')


from collections import OrderedDict

def sort_dict():

    order_dict = {}
    with open("Dictionary/dict2_n_f_text", 'r') as ReadDict:
        for line in ReadDict:
            split_line = line.split('\t')
            order_dict[split_line[1]] = int(split_line[2])

    sorted_x = sorted(order_dict.iteritems(), key=lambda x: x[1])
    with open("Dictionary/dict2_n_f_text_sorted", 'w') as WriteDict:
        for (i, j) in sorted_x:
            WriteDict.write(i+"\t"+str(j)+"\n")

def main():
    lda1 = models.LdaModel.load('Corpus/lda_model_2012-2013')
    lda2 = models.LdaModel.load('Corpus/lda_model_2013-2014')
    lda3 = models.LdaModel.load('Corpus/lda_model_2014-2015')
    # lda1 = models.LdaModel.load('Corpus/lda_model_1999-2000')
    # lda2 = models.LdaModel.load('Corpus/lda_model_2001-2002')
    # lda3 = models.LdaModel.load('Corpus/lda_model_2003-2004')
    lda_list = [lda1, lda2, lda3]
    print_topic(lda_list)


if __name__ == '__main__':
    main()

