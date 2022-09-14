# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 23:03:06 2022

@author: 18721
"""

import numpy as np
import pandas as pd

#习题1
# Ex1：统计未出现的类别
# 在第五章中介绍了 crosstab 函数，在默认参数下它能够对两个列的组合出现的频数进行统计汇总：
df = pd.DataFrame({'A':['a','b','c','a'],
                   'B':['cat','cat','dog','cat']})


pd.crosstab(df.A, df.B)
'''
结果为：
B  cat  dog
A          
a    2    0  表明a-cat出现了两次
b    1    0  表明b-cat出现了一次
c    0    1  表明c-dog出现了一次
'''
'''但事实上有些列存储的是分类变量，列中并不一定包含所有的类别，此时如果想要对这些未出现的类别在 crosstab 结果中也进行汇总，
则可以指定 dropna 参数为 False ：'''

df.B = df.B.astype('category').cat.add_categories('sheep')  #应用了cat对象
pd.crosstab(df.A, df.B, dropna=False)
'''
B  cat  dog  sheep  这是新增的列，但其实这一列是没有的
A                 
a    2    0      0
b    1    0      0
c    0    1      0
'''
pd.crosstab(df.A, df.B, dropna=True)
'''
B  cat  dog  因为dropna设置为了true，所以sheep不会保留
A          
a    2    0
b    1    0
c    0    1
'''
#本题要求：请实现一个带有 dropna 参数的 my_crosstab 函数来完成上面的功能。




#习题2
# Ex2：钻石数据集
# 现有一份关于钻石的数据集，其中 carat, cut, clarity, price 分别表示克拉重量、切割质量、纯净度和价格，样例如下：
df = pd.read_csv('data/diamonds.csv')
df.head(3)
'''Out[76]: 
   carat      cut clarity  price
0   0.23    Ideal     SI2    326
1   0.21  Premium     SI1    326
2   0.23     Good     VS1    327'''
#2-1分别对 df.cut 在 object 类型和 category 类型下使用 nunique 函数，并比较它们的性能。

#2-2钻石的切割质量可以分为五个等级，由次到好分别是 Fair, Good, Very Good, Premium, Ideal ，纯净度有八个等级，由次到好分别是 I1, SI2, SI1, VS2, VS1, VVS2, VVS1, IF ，请对切割质量按照 由好到次 的顺序排序，相同切割质量的钻石，按照纯净度进行 由次到好 的排序。

#2-3分别采用两种不同的方法，把 cut, clarity 这两列按照 由好到次 的顺序，映射到从0到n-1的整数，其中n表示类别的个数。

#2-4对每克拉的价格分别按照分位数（q=[0.2, 0.4, 0.6, 0.8]）与[1000, 3500, 5500, 18000]割点进行分箱得到五个类别 Very Low, Low, Mid, High, Very High ，并把按这两种分箱方法得到的 category 序列依次添加到原表中。

#2-5第4问中按照整数分箱得到的序列中，是否出现了所有的类别？如果存在没有出现的类别请把该类别删除。

#2-6对第4问中按照分位数分箱得到的序列，求每个样本对应所在区间的左右端点值和长度。