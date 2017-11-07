# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.10.24
# Goal: 分析文本结构
# Other:
# '''

# from stanfordcorenlp import StanfordCoreNLP
# from gensim import models, corpora
import jieba
import jieba.posseg as pseg
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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
    nlp = StanfordCoreNLP(r'D:\\stanford-corenlp-full-2017-06-09', lang='zh')
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
    """

    :return:
    """
    dictionary = corpora.Dictionary.load('data1/dict.dict')
    corpus = corpora.BleiCorpus('data1/corpus_all_in_dict2.blei')
    tfidf_model = models.TfidfModel(corpus=corpus, dictionary=dictionary, id2word=dictionary)
    print tfidf_model.dfs
    print tfidf_model.idfs


def save_theme():
    """
    :param file_path:
    :return:
    """
    theme_dict = {}
    with open("data1/theme.txt", 'r') as reader:
        file_content = reader.readlines()
        for line in file_content:
            line_list = line.strip().split(';')
            for element in line_list:
                if element is "NULL" or element is '':
                    continue
                if element in theme_dict.keys():
                    theme_dict[element] += 1
                else:
                    theme_dict[element] = 1
    for key, value in theme_dict.iteritems():
        print key, value

    print theme_dict.__len__()

def test_jieba():

    jieba.load_userdict("dict/dictforthem.txt")
    with open('data1/trainning_content.txt', 'r') as reader:
        file_content = reader.readlines()
        for index in range(500):
            # seg_list = jieba.cut(file_content[index].strip())
            # print index, ' '.join(seg_list)
            seg_list = pseg.cut(file_content[index].strip())
            print index, ' '.join([w.word+w.flag for w in seg_list])


def main():
    # save_dictionary("data/in.txt")
    # save_model()
    # save_theme()
    test_jieba()


if __name__ == '__main__':
    main()


