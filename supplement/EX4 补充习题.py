# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 20:38:32 2022

@author: 18721
"""
# Ex4：删除同样的行
# 现有两张表，请在df1中剔除在df2中出现过的行。
import pandas as pd
df1 = pd.DataFrame({
    "A": [3,2,2,3,1,3],
    "B": [2,1,1,3,6,2],
    "C": [1,2,2,7,7,1],
    "D": [5,6,6,1,2,5],
})
#    A  B  C  D
# 0  3  2  1  5
# 1  2  1  2  6
# 2  2  1  2  6
# 3  3  3  7  1
# 4  1  6  7  2
# 5  3  2  1  5

df2 = pd.DataFrame({
    "A": [2,3,1],
    "B": [1,9,6],
    "C": [2,7,7],
    "D": [6,1,2],
})
#    A  B  C  D
# 0  2  1  2  6
# 1  3  9  7  1
# 2  1  6  7  2


#感觉有点像第三章的4.1节对索引进行集合运算，但是现在的index其实都是自然整数，不合适
df1['all']=['_'.join(str(j) for j in df1.iloc[i].values) for i in range(df1.shape[0])]
df1=df1.set_index('all')


df2['all']=['_'.join(str(j) for j in df2.iloc[i].values) for i in range(df2.shape[0])]
df2=df2.set_index('all')

res=df1.loc[df1.index.difference(df2.index)]
res=res.reset_index(drop=True)
#    A  B  C  D   可见结果在行顺序不重要的时候是对的，但是和结果不完全相同
# 0  3  2  1  5
# 1  3  2  1  5
# 2  3  3  7  1  