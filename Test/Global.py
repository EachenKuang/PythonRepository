# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.7
Goal: store the global variables
Other:保存全局变量名
"""
# variables
TOPIC_NUM = 10

# function


def average_from_list(input_list):
    """
    # 因为需要多次在list中进行加法运算，故使用一个函数来集成
    :param input_list:
    :return: ave 平均数
    """
    sum_of_list = 0.0
    len_list = len(input_list)
    for num in input_list:
        sum_of_list += num
    ave = sum_of_list/len_list
    return ave
