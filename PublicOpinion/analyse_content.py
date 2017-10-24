# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.10.24
# Goal: 分析文本结构
# Other:
# '''

from stanfordcorenlp import StanfordCoreNLP
from gensim import models, corpora
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

nlp = StanfordCoreNLP(r'D:\\stanford-corenlp-full-2017-06-09', lang='zh')

# with open("data/trainning_content.txt", 'r') as reader:
#     file_content = reader.readlines()
#     for line in file_content:
#         line = line.strip()
#         words = nlp.word_tokenize(line)
#         print ' '.join(words)

def save_dictionary(file_path):
    """
    保存原始字典文件以及所有词库
    :return:
    """
    texts = []
    with open(file_path, 'r') as reader:
        file_content = reader.readlines()
        for line in file_content:
            line = line.strip()
            words = nlp.word_tokenize(line)
            texts.append(words)

    dictionary = corpora.Dictionary(texts)
    dictionary.save('data1/dict.dict')
    dictionary.save_as_text('data1/dict_text.txt', False)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize("data1/corpus_all_in_dict2.blei", corpus, id2word=dictionary)

def save_model():

    dictionary = corpora.Dictionary.load('data1/dict.dict')
    corpus = corpora.BleiCorpus('data1/corpus_all_in_dict2.blei')
    tfidf_model = models.TfidfModel(corpus=corpus, dictionary=dictionary, id2word=dictionary)
    print tfidf_model.dfs
    print tfidf_model.idfs

def main():
    # save_dictionary("data/trainning_content.txt")
    save_model()

if __name__ == '__main__':
    main()


