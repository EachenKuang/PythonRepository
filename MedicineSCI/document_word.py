# -*- encoding: utf-8 -*-
import numpy as np
import pandas as pd

def generate_documents_words_matrix():
    f1 = open('TF.txt', 'r')        # Documents
    f2 = open('termList.txt', 'r')  # Words
    # 词表
    words_list = []
    for line in f2.readlines():
        words_list.append(line.strip())
    documents_words_matrix = pd.DataFrame(np.zeros((8283, len(words_list))), columns=words_list, index=range(1, 8284))
    article_index = None
    for line in f1.readlines():
        splits = line.split()
        if len(splits) == 1 and article_index is None:
            article_index = int(line.split('\\')[-1].split('.')[0])
            article_words_frequency = [0] * len(words_list) # 每篇文章初始化列表
            print article_index
        elif len(splits) == 1 and article_index is not None:
            documents_words_matrix.loc[article_index,] = article_words_frequency
            article_index = int(line.split('\\')[-1].split('.')[0])
            article_words_frequency = [0] * len(words_list)  # 每篇文章初始化列表
            print article_index
        else:
            word = " ".join(splits[:-1])
            frequency = int(splits[-1])
            article_words_frequency[words_list.index(word)] = frequency
    documents_words_matrix[documents_words_matrix>0] = 1
    documents_words_matrix.to_csv('documents_words_matrix_0_1.csv', header=True, index=True)
    f1.close()
    f2.close()


def multiply_document_word_matrix():
    df = pd.read_csv('documents_words_matrix_0_1.csv', index_col=0)
    result = np.matrix(df.T)*np.matrix(df)
    pd.DataFrame(result).to_csv('result_0_1.csv')


def select_topic_from_matrix():
    topic1 = open('topic8', 'r')
    topic2 = open('topic6', 'r')
    termList = open('termList.txt', 'r')
    words_list = []
    for line in termList.readlines():
        words_list.append(line.strip())
    df = pd.read_csv('result_0_1.csv', index_col=0)
    print df.head(3)
    topic1_index = []
    for line in topic1:
        word = " ".join(line.split()[:-1])
        topic1_index.append(words_list.index(word))
    topic2_index = []
    for line in topic2:
        word = " ".join(line.split()[:-1])
        topic2_index.append(words_list.index(word))
    print topic1_index
    print topic2_index
    words_list = np.array(words_list)
    topic1_self_df = np.matrix(df.loc[topic1_index, np.array(topic1_index).astype(str)])
    topic2_self_df = np.matrix(df.loc[topic2_index, np.array(topic2_index).astype(str)])
    topic1_topic2_df = np.matrix(df.loc[topic1_index, np.array(topic2_index).astype(str)])
    topic1_self_df = pd.DataFrame(topic1_self_df, index=words_list[topic1_index], columns=words_list[topic1_index])
    topic2_self_df = pd.DataFrame(topic2_self_df, index=words_list[topic2_index], columns=words_list[topic2_index])
    topic1_topic2_df = pd.DataFrame(topic1_topic2_df, index=words_list[topic1_index], columns=words_list[topic2_index])
    topic1_self_df.to_csv('topic1.csv',index=True,header=True)
    topic2_self_df.to_csv('topic2.csv',index=True,header=True)
    topic1_topic2_df.to_csv('topic1_topic2.csv',index=True,header=True)

def main():
    # generate_documents_words_matrix()
    # multiply_document_word_matrix()
    select_topic_from_matrix()

if __name__ == '__main__':
    main()