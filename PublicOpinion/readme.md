# 这是用于Data啊Fountain的《基于主题的文本情感分析》的思路分析

## 分词工具
StanfordCoreNLP

## 数据结构
row_id	content-评论内容	theme-主题	sentiment_word-情感关键词	sentiment_anls-情感正负面

## 模型思路

预处理过程

## 难点
抽取主题词，与之对应的情感词以及情感分析


## 论文收取
情感依存元组( EDT， Emotional dependency tuple)，它以主题特征词为核心，其他修饰成分依附于核心词。
以句子中含有的主题特征词作为 EDT 的核心构建基于情感依存元组的句子情感判别模型，使得提取的情感紧扣主题且情感值计算更精确。
