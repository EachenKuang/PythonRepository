# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.9.20
# Goal: 内容抓取
# Other:
# '''

# 用来验证模型的效果
# 使用前10000条进行训练，后10000条进行
def calculate_f(input_file, verify_file):
    """

    :param input_file:
    :param verify_file:
    :return:
    """
    # 读取评分文件
    with open("input_file",'r') as reader_file:
        reader = reader_file.readlines()

    # 读取扁粉文件
    with open("verify_file", 'r') as reader_file:
        reader = reader_file.readlines()

