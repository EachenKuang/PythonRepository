# -*- coding: utf-8 -*-
from collections import OrderedDict
from gensim import models


def print_topic(lda_list):
    name = ['2012-2013', '2013-2014', '2014-2015']
    for j in range(3):
        show = lda_list[j].show_topics(num_words=40, formatted=False)
        topic_dict = OrderedDict(show)
        with open('Output/' + name[j] + 'topic_format', 'w') as temp:
            # temp.write(str(show))
            for i in range(10):
                # topic_dict[i]  # topic i 中的对应字段 list
                topic_dict_each = OrderedDict(topic_dict[i])
                temp.write('topic' + str(i) + '\n')
                for id, value in topic_dict_each.iteritems():
                    temp.write(id + ' ' + str(value) + '\n')


def main():
    lda1 = models.LdaModel.load('Corpus/lda_model_2012-2013')
    lda2 = models.LdaModel.load('Corpus/lda_model_2013-2014')
    lda3 = models.LdaModel.load('Corpus/lda_model_2014-2015')
    lda_list = [lda1, lda2, lda3]
    print_topic(lda_list)


if __name__ == '__main__':
    main()

