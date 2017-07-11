# -*- encoding: utf-8 -*-

# '''
# Author: Eachen Kuang
# Date:  2017.6.1
# Goal: new LDA model
# Other:
# '''

import numpy as np
import pandas as pd

#输入，两个文件，输出 一个10*10矩阵 横轴为 第一篇文章，纵轴为第二篇文章
#使用余弦值计算方法 ：
#
file_1 = ""
file_2 = ""


with open(file_1,'r') as first,open(file_2,'r')as second:

