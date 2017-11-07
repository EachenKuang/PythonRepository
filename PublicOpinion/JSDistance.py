# -*- coding: utf-8 -*-
# '''
# Author: Eachen Kuang
# Date:  2017.10.20
# Goal: 将文件转化为字典
# Other:
# '''

import string
from math import log
import numpy as np


def KLD(p,q):
    p,q=zip(*filter(lambda (x,y): x!=0 or y!=0, zip(p,q))) #去掉二者都是0的概率值
    p=p+np.spacing(1)
    q=q+np.spacing(1)
    print p, q
    return sum([_p * log(_p/_q,2) for (_p,_q) in zip(p,q)])
# p=np.ones(5)/5.0
# q=[0,0,0.5,0.2,0.3]
# print KLD(p,q)

def JSD_core(p, q):
    p, q = zip(*filter(lambda[x,y]: x != 0 or y != 0, zip(p, q)))  # 去掉二者都是0的概率值
    M = [0.5 * (_p + _q) for _p, _q in zip(p, q)]
    p = p + np.spacing(1)
    q = q + np.spacing(1)
    M = M + np.spacing(1)
    #     print p,q,M
    return 0.5 * KLD(p, M) + 0.5 * KLD(q, M)


reg = lambda x: [x.count(i) for i in string.lowercase]  # 频数分布
rate = lambda y: [round(i * 1.0 / sum(reg(y)), 4) for i in reg(y)]  # 概率分布
s1 = 'KuangYichen1raf'
s2 = 'YichenKuang2'

print JSD_core(rate(s1), rate(s2))

