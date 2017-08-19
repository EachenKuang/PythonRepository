# -*- encoding: utf-8 -*-

# '''
# Author: Eachen Kuang
# Date:  2017年5月21日15:13:35
# Goal:主题关联计算
# Other:
# '''

import logging
import itertools
from gensim import models
from gensim import corpora

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#把每一年的数据做成一个copus

#example:
# dict1 = Dictionary(some_documents)
# dict2 = Dictionary(other_documents)  # ids not compatible with dict1!
# dict2_to_dict1 = dict1.merge_with(dict2)
# # now we can merge corpora from the two incompatible dictionaries into one
# merged_corpus = itertools.chain(corpus1, corpus2)

#1991 - 2017
merged_corpus = itertools.chain()