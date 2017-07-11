# -*- encoding: utf-8 -*-

# '''
# Author: Eachen Kuang
# Date:  2017年5月21日15:13:35
# Goal:主题关联计算
# Other:
# '''

def cossim(a,b):
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for x, y in zip(a, b):
        dot_product+=x*y
        normA += x**2
        normB += y**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product/((normA*normB)**0.5)

# 直接关联法
def direct_co():
     pass
# 语义关联法
def sematic_co():
    pass
# 综合关联法
def synthesis_co():
    pass


sim(['a','b','c'],['c','a','f'])


select