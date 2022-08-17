# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 20:47:06 2022

@author: 18721
"""

'''*******************************习题1，口袋妖怪数据集*****************************************'''
#数据说明
# 代表全国图鉴编号，不同行存在相同数字则表示为该妖怪的不同状态
# 妖怪具有单属性和双属性两种，对于单属性的妖怪， Type 2 为缺失值
# Total, HP, Attack, Defense, Sp. Atk, Sp. Def, Speed 分别代表种族值、体力、物攻、防御、特攻、特防、速度，其中种族值为后6项之和
import numpy as np
import pandas as pd
import math
df = pd.read_csv('data/pokemon.csv')   #(800,11)
df.head(3)

'''Q1：对 HP, Attack, Defense, Sp. Atk, Sp. Def, Speed 进行加总，验证是否为 Total 值。'''
#我的写法
df_demo=df[df.columns[-6:]]  #提取一些列，这个是参考的第45个输入df = df[df.columns[:7]]的写法
df_demo['sum']=df_demo.sum(axis=1)
(df_demo['sum']==df['Total']).all()  #确实返回true
#答案写法，从不等的角度能够输出0
(df[['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].sum(1)!=df['Total']).mean()


'''Q2: 对于 # 重复的妖怪只保留第一条记录，解决以下问题：'''
df1=df.drop_duplicates(['#'])    #默认的keep就是first，现在是[721 rows x 11 columns]，也即是存在79条重复
'''Q2a:求第一属性的种类数量和前三多数量对应的种类'''
df1['Type 1'].nunique()     #输出18
df1['Type 1'].value_counts()
            # 由于默认是降序的，因此可以得知前三多数量对应的种类为：
            # Water       112
            # Normal       98
            # Grass        70
#当然也可以直接输出Index(['Water', 'Normal', 'Grass'], dtype='object')
df1['Type 1'].value_counts().index[:3]


'''Q2b:求第一属性和第二属性的组合种类'''
df2= df1.drop_duplicates(['Type 1', 'Type 2']) #现在是[143 rows x 11 columns]，因此组合种类就是143个
df2.shape[0]#输出143


'''Q2c:求尚未出现过的属性组合'''
df['Type 1'].nunique()  #18
# df['Type 1'].unique() 
# array(['Grass', 'Fire', 'Water', 'Bug', 'Normal', 'Poison', 'Electric',
#        'Ground', 'Fairy', 'Fighting', 'Psychic', 'Rock', 'Ghost', 'Ice',
#        'Dragon', 'Dark', 'Steel', 'Flying'], dtype=object)
df['Type 2'].nunique()  #18
# df['Type 2'].unique()  
# array(['Poison', nan, 'Flying', 'Dragon', 'Ground', 'Fairy', 'Grass',
#        'Fighting', 'Psychic', 'Steel', 'Ice', 'Rock', 'Dark', 'Water',
#        'Electric', 'Fire', 'Ghost', 'Bug', 'Normal'], dtype=object)
#而且其中的nan是float类型，其它的是str类型
#在python中可以使用isinstance()函数来判断是否为字符串，
# 语法格式“isinstance(object, basestring)”；isinstance()函数是用于判断一个对象是否是一个已知的类型。
#因此组合就是18*18=324,可以写出所有可能的组合情况
L_full = [i+' '+j if i!=j else i for i in df['Type 1'].unique() for j in df['Type 1'].unique()] #如果双属性的话就是i+' '+j，否则就是i
len(L_full)  #长度为324

#现在已有的组合情况为：
L_part = [i+' '+j if isinstance(j, str) else i    for i, j in zip(df['Type 1'], df['Type 2'])]
#答案中写的是：
L_part1 = [i+' '+j if not isinstance(j, float) else i for i, j in zip(df['Type 1'], df['Type 2'])]
# L_part==L_part1确实是true
# len(L_part) 现在是800
# len(set(L_part))  现在是154，因此还有324-154=170种
res=set(L_full).difference(set(L_part))  #用集合的差集进行计算



'''Q3:按照下述要求，构造 Series ：'''
'''Q3a:取出物攻，超过120的替换为 high ，不足50的替换为 low ，否则设为 mid'''
#可以使用逻辑替换mask，mask 在传入条件为 True 的对应行进行替换
%timeit df['Attack'].mask(df['Attack']>120, 'high').mask(df['Attack']<50, 'low').mask((50<=df['Attack'])&(df['Attack']<=120), 'mid')
# 1.35 ms ± 75.3 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)

#当然我们也可以使用自定义函数，然后使用apply
def trans(a):
    if a>120:
        return 'high'
    elif a<50:
        return 'low'
    else:
        return 'mid'
%timeit df['Attack'].apply(trans)    
# 291 µs ± 13 µs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)这个竟然更快


'''Q3b:取出第一属性，分别用 replace 和 apply 替换所有字母为大写'''
#如果用repalce，最好的方式就是字典构造
df['Type 1'].replace({i:str.upper(i) for i in df['Type 1'].unique()})
#如果用apply，可以使用lambda匿名函数
df['Type 1'].apply(lambda i:str.upper(i))

'''Q3c:求每个妖怪六项能力的离差，即所有能力中偏离中位数最大的值，添加到 df 并从大到小排序'''
df['Deviation'] = df[['HP', 'Attack', 'Defense', 'Sp. Atk','Sp. Def', 'Speed']].apply(
    lambda x:np.max((x-x.median()).abs()), axis=1)  #这个是每个妖怪，因此是按照行的，axis=1才可
df.sort_values('Deviation', ascending=False)  #按值降序

'''*******************************习题2：指数加权窗口*****************************************'''
'''1.作为扩张窗口的 ewm 窗口'''
#在扩张窗口中，用户可以使用各类函数进行历史的累计指标统计，
# 但这些内置的统计函数往往把窗口中的所有元素赋予了同样的权重。
# 事实上，可以给出不同的权重来赋给窗口中的元素，指数加权窗口就是这样一种特殊的扩张窗口。

#对于 Series 而言，可以用 ewm 对象如下计算指数平滑后的序列：
np.random.seed(0)
s = pd.Series(np.random.randint(-1,2,30).cumsum())   #np.random.randint(-1,2,30)生成的是-1,0,1三种可能的整数

s.ewm(alpha=0.2).mean()#用 expanding 窗口实现
#也就是要如何用expanding实现ewm(alpha=0.2)
#人工定义ewm函数
def my_ewm(x,alpha=0.2):
    weight=(1-alpha)**np.arange(x.shape[0])[::-1]
    #由于x是从0开始的，所以权重是从(1-alpha)t,一直到(1-alpha)0,也就是说指数是逆序的
    y=(x*weight).sum()/(weight.sum())
    return y
s.expanding().apply(my_ewm)


'''2.滑动窗口'''
# 从第1问中可以看到， ewm 作为一种扩张窗口的特例，只能从序列的第一个元素开始加权。
# 现在希望给定一个限制窗口 n ，只对包含自身的最近的 n 个元素作为窗口进行滑动加权平滑。
# 请根据滑窗函数，给出新的  与  的更新公式，并通过 rolling 窗口实现这一功能。
#事实上只需要把s.expanding().apply(my_ewm)的expanding()改成rolling(n)就能够实现只对包含自身的最近的 n 个元素作为窗口进行滑动加权平滑
def rolling_n(s,n):
    return s.rolling(n).apply(my_ewm)
rolling_n(s,4)

