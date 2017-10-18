# 这是用于Data啊Fountain的《基于主题的文本情感分析》的思路分析

## 赛题背景
近年来，文本情感分析技术在网络营销、企业舆情监控、政府舆论监控等扮演越来越重要的角色。鉴于主题模型在文本挖掘领域的优势，基于主题的文本情感分析技术也成为人们关注的热点，其主要任务是通过挖掘用户评论所蕴含的主题、以及对这些主题的情感偏好，来提高文本情感分析的性能。以网上电商购物评论为例，原始的主题模型主要针对篇幅较大的文档或者评论句子的集合，学习到的主题主要针对整个产品品牌；而现实情形是，用户评论大多针围绕产品的某些特征或内容主题展开（如口味、服务、环境、性价比、交通、快递、内存、电池续航能力、原料、保质期等等，这说明相比于对产品的整体评分， 用户往往更关心产品特征），而且评论文本往往较短。
## 任务描述
本次大赛提供脱敏后的电商评论数据。参赛队伍需要通过数据挖掘的技术和机器学习的算法，根据语句中的主题特征和情感信息来分析用户对这些主题的偏好，并以<主题，情感词>序对作为输出。
## 分词工具
StanfordCoreNLP

## 数据结构
row_id	content-评论内容	theme-主题	sentiment_word-情感关键词	sentiment_anls-情感正负面

## 模型思路
1. 读取评论数据，对评论进行分词
2. 去除停用词
3. 抽取情感词，记录词的位置
4. 寻找其情感词对应的的主题词


## 难点
抽取主题词，与之对应的情感词以及情感分析


## 论文收取
情感依存元组( EDT， Emotional dependency tuple)，它以主题特征词为核心，其他修饰成分依附于核心词。
以句子中含有的主题特征词作为 EDT 的核心构建基于情感依存元组的句子情感判别模型，使得提取的情感紧扣主题且情感值计算更精确。