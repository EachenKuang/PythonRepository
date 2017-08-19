# -*- encoding: utf-8 -*-
"""
Author: Eachen Kuang
Date:  2017.8.7
Goal: store the global variables
Other:保存全局变量名
"""
import re

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


# embedded_numbers(s)与sort_strings_with_embedded_numbers一起使用
# 用于对内嵌的数字list进行排序
def embedded_numbers(s):
    re_digits = re.compile(r'(\d+)')
    pieces = re_digits.split(s)               # 切成数字与非数字
    pieces[1::2] = map(int, pieces[1::2])     # 将数字部分转成整数
    return pieces


def sort_strings_with_embedded_numbers(alist):
    return sorted(alist, key=embedded_numbers)

