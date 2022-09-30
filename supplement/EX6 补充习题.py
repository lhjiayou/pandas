# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 21:21:03 2022

@author: 18721
"""

import pandas as pd
# Ex6：捕获非零的行列索引  :给定如下的数据框，请返回非零行列组合构成的多级索引。
df = pd.DataFrame(
    [[0,5,0],[2,1,0],[0,0,6],[0,9,0]],
    index=list("ABCD"), columns=list("XYZ"))
#    X  Y  Z
# A  0  5  0
# B  2  1  0
# C  0  0  6
# D  0  9  0

df=df.T  #先把XYZ转换到index上面
#    A  B  C  D
# X  0  2  0  0
# Y  5  1  0  9
# Z  0  0  6  0

df=df.stack()
# X  A    0
#    B    2
#    C    0
#    D    0
# Y  A    5
#    B    1
#    C    0
#    D    9
# Z  A    0
#    B    0
#    C    6
#    D    0

df[df!=0].index
# MultiIndex([('X', 'B'),
#             ('Y', 'A'),
#             ('Y', 'B'),
#             ('Y', 'D'),
#             ('Z', 'C')],
#            )