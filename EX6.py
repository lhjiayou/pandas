# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 10:37:14 2022

@author: huanghao2
"""

import numpy as np
import pandas as pd

#习题1：
'''Ex1：美国疫情数据集
现有美国4月12日至11月16日的疫情报表（在 /data/us_report 文件夹下），
请将 New York 的 Confirmed, Deaths, Recovered, Active 合并为一张表，
索引为按如下方法生成的日期字符串序列：'''
date = pd.date_range('20200412', '20201116').to_series()
date = date.dt.month.astype('string').str.zfill(2)    +'-'+ date.dt.day.astype('string').str.zfill(2)     +'-'+ '2020'
#实现了日期的拼接，zfill(2)的作用应该是在个位数的月份和日期前面补上0
date = date.tolist()

#上面的data是list，每个元素都是一个时间，而且每个时间其实在路径中都是有一个excel的，
# 每一行是province（包括newyork），每一列是特征（包括Confirmed, Deaths, Recovered, Active）
#其实我最直观的做法就是直接赋值进去，比较好理解
def fun1():
    df=pd.DataFrame(np.zeros(shape=(len(date),4)),index=date,columns=['Confirmed', 'Deaths','Recovered', 'Active' ])
    for i in range(len(date)):
        df1=pd.read_csv('./data/us_report/'+date[i]+'.csv')
        df1=df1[df1['Province_State']=='New York'].loc[:,['Confirmed', 'Deaths','Recovered', 'Active' ]]   #选取列
        df.iloc[i,:]=df1
    return df
df1=fun1()
df1=df1.astype(np.int)

#但是好像放在本章的目的是要使用concat的append方法
def fun2():
    df=pd.DataFrame(columns=['Confirmed', 'Deaths','Recovered', 'Active' ])  #先创建空的dataframe，0*4
    for d in date:
        df1 = pd.read_csv('data/us_report/' + d + '.csv', index_col='Province_State')  #现在是17行
        s1=df1.loc['New York',['Confirmed', 'Deaths','Recovered', 'Active' ]]
        # df=df.append(s1,ignore_index=True)  #使用append方法的时候其实会warning
        df=pd.concat([df,s1.to_frame().T])
    df.index=date
    return df
df2=fun2()
df2=df1.astype(np.int)

df1.equals(df2)   #全部转化成整数之后现在返回的是true


#习题2：这意思是手工写join函数是么？
'''Ex2：实现join函数   
请实现带有 how 参数的 join 函数

假设连接的两表无公共列

调用方式为 join(df1, df2, how="left")

给出测试样例'''
df1 = pd.DataFrame({'col1':list('01234')}, index=list('AABCD'))
# df1
#   col1
# A    0
# A    1
# B    2
# C    3
# D    4
df2 = pd.DataFrame({'col2':list('opqrst')}, index=list('ABBCEE'))
# df2
#   col2
# A    o
# B    p
# B    q
# C    r
# E    s
# E    t
df1.join(df2, how='outer')  #调用官方的join函数实现的并集
#   col1 col2
# A    0    o
# A    1    o
# B    2    p
# B    2    q
# C    3    r
# D    4  NaN
# E  NaN    s
# E  NaN    t
df1.join(df2, how='left')  #官方的join函数
#   col1 col2
# A    0    o
# A    1    o
# B    2    p
# B    2    q
# C    3    r
# D    4  NaN

#下面开始手工实现join函数
def join(df1, df2, how='left'):
    res_col = df1.columns.tolist() +  df2.columns.tolist()   #列名
    dup = df1.index.unique().intersection(df2.index.unique())  #index的交集
    res_df = pd.DataFrame(columns = res_col)  #0*2  空的dataframe
    for label in dup:
        cartesian = [list(i)+list(j) for i in df1.loc[label].values for j in df2.loc[label].values]
        dup_df = pd.DataFrame(cartesian, index = [label]*len(cartesian), columns = res_col)
        res_df = pd.concat([res_df,dup_df])
    if how in ['left', 'outer']:
        for label in df1.index.unique().difference(dup):
            if isinstance(df1.loc[label], pd.DataFrame):
                cat = [list(i)+[np.nan]*df2.shape[1] for i in df1.loc[label].values]
            else:
                cat = [list(i)+[np.nan]*df2.shape[1] for i in df1.loc[label].to_frame().values]
            dup_df = pd.DataFrame(cat, index = [label]*len(cat), columns = res_col)
            res_df = pd.concat([res_df,dup_df])
    if how in ['right', 'outer']:
        for label in df2.index.unique().difference(dup):
            if isinstance(df2.loc[label], pd.DataFrame):
                cat = [[np.nan]+list(i)*df1.shape[1] for i in df2.loc[label].values]
            else:
                cat = [[np.nan]+list(i)*df1.shape[1] for i in df2.loc[label].to_frame().values]
            dup_df = pd.DataFrame(cat, index = [label]*len(cat), columns = res_col)
            res_df = pd.concat([res_df,dup_df])
    return res_df
join(df1, df2, how="left")  #可见与df1.join(df2, how='left')  #官方的join函数相同
#   col1 col2 
# A    0    o
# A    1    o
# B    2    p
# B    2    q
# C    3    r
# D    4  NaN
