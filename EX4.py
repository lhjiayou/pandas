# -*- coding: utf-8 -*-
"""
Created on Sun Aug 28 21:55:34 2022

@author: 18721
"""
import pandas as pd
import numpy as np


#习题1
# Ex1：汽车数据集
# 现有一份汽车数据集，其中 Brand, Disp., HP 分别代表汽车品牌、发动机蓄量、发动机输出。
df = pd.read_csv('data/car.csv')  #[60 rows x 9 columns]
# df.columns
# ['Brand', 'Price', 'Country', 'Reliability', 'Mileage', 'Type', 'Weight',   'Disp.', 'HP']

#1.先过滤出所属 Country 数超过2个的汽车，即若该汽车的 Country 在总体数据集中出现次数不超过2则剔除，
gb = df.groupby('Country')
df1=gb.filter(lambda x:x.shape[0]>2)  #现在是55*9
# 再按 Country 分组计算价格均值、价格变异系数、该 Country 的汽车数量，其中变异系数的计算方法是标准差除以均值，并在结果中把变异系数重命名为 CoV 。
'''df.groupby(分组依据)[数据来源].使用操作'''
df1.groupby('Country')['Price'].agg([('CoV', lambda x: x.std()/x.mean()),   
    #如果想要对聚合结果的列名进行重命名，只需要将上述函数的位置改写成元组，元组的第一个元素为新的名字，第二个位置为原来的函数，
                                     'mean', 
                                     'count'])
#输出结果为
#                 CoV          mean  count(使用的操作)
# Country(分组依据)                                 
# Japan      0.387429  13938.052632     19 (这儿的数据来源就是Price列的)
# Japan/USA  0.240040  10067.571429      7
# Korea      0.243435   7857.333333      3
# USA        0.203344  12543.269231     26


# 2.按照表中位置的前三分之一、中间三分之一和后三分之一分组，统计 Price 的均值。
def idx(i):
    # idx1=np.array(x.index.to_list())
    # for i in idx1:
    if i<20:
        return 'head'
    elif i>=40:
        return 'tail'
    else:
        return 'median'
condition=pd.Series(df.index).apply(idx)     
# (condition=='head').sum()   
# (condition=='median').sum()   
# (condition=='tail').sum()  
df.groupby(condition)['Price'].mean()  
# head       9069.95
# median    13356.40
# tail      15420.65
# Name: Price, dtype: float64   


# 3.对类型 Type 分组，对 Price 和 HP 分别计算最大值和最小值，结果会产生多级索引，
# 请用下划线把多级列索引合并为单层索引。
'''对特定的列要使用特定的聚合函数，可以使用agg方法'''
df.groupby('Type').agg({
    'Price':'max',   
    'HP':'min'
    })
#          Price   HP  字典以列名为键，以聚合字符串或字符串列表为值
# Type                 但是以字符串为值的时候，也就是一个聚合函数，并不会产生多级索引 
# Compact  18900   95
# Large    17257  150
# Medium   24760  110
# Small     9995   63
# Sporty   13945   92
# Van      15395  106
'''如果想要产生多级索引，就将聚合函数用字符串列表形式展现'''
df3=df.groupby('Type').agg({
    'Price':['max'],   
    'HP':['min']
    })
#          Price   HP   
#            max  min
# Type               
# Compact  18900   95
# Large    17257  150
# Medium   24760  110
# Small     9995   63
# Sporty   13945   92
# Van      15395  106  
'''接下来对column的多级index进行拼接，这儿使用的是第三章的3.2节的索引属性的修改
关于 map 的另一个使用方法是对多级索引的压缩''' 
df3.columns =df3.columns.map(lambda x:'_'.join(x))
#          Price_max  HP_min  用map可以很好地实现多级索引的压缩
# Type                      
# Compact      18900      95
# Large        17257     150
# Medium       24760     110
# Small         9995      63
# Sporty       13945      92
# Van          15395     106



# 4.对类型 Type 分组，对 HP 进行组内的 min-max 归一化。
'''看见组内，就知道要使用的是变换函数transform
变换函数的返回值为同长度的序列'''
df.groupby('Type')['HP'].transform(lambda x:(x-x.min())/(x.max()-x.min()))  #返回等长度的series


# 5.对类型 Type 分组，计算 Disp. 与 HP 的相关系数。
df.groupby('Type')[['HP', 'Disp.']].apply(
   lambda x:np.corrcoef(x['HP'].values, x['Disp.'].values)[0,1])
'''np.corrcoef(df['HP'].values, df['Disp.'].values)
计算的是整列的协方差矩阵，而两列的相关系数位于[0,1]或者[1,0]的位置上
array([[1.       , 0.8181881],
        [0.8181881, 1.       ]])'''
# Type
# Compact    0.586087
# Large     -0.242765
# Medium     0.370491
# Small      0.603916
# Sporty     0.871426
# Van        0.819881
# dtype: float64



# Ex2：实现transform函数
# groupby 对象的构造方法是 my_groupby(df, group_cols)
# 支持单列分组与多列分组
# 支持带有标量广播的 my_groupby(df)[col].transform(my_func) 功能
# pandas 的 transform 不能跨列计算，请支持此功能，即仍返回 Series 但 col 参数为多列
# 无需考虑性能与异常处理，只需实现上述功能，在给出测试样例的同时与 pandas 中的 transform 对比结果是否一致
class my_groupby:
    '''比较难，就先不看了'''
    def __init__(self, my_df, group_cols):
        '''实例化的时候需要传入df以及列名'''
        self.my_df = my_df.copy()
        self.groups = my_df[group_cols].drop_duplicates()
        if isinstance(self.groups, pd.Series):
            self.groups = self.groups.to_frame()
        self.group_cols = self.groups.columns.tolist()
        self.groups = {i: self.groups[i].values.tolist(
                       ) for i in self.groups.columns}
        self.transform_col = None
    def __getitem__(self, col):
        self.pr_col = [col] if isinstance(col, str) else list(col)
        return self
    def transform(self, my_func):
        self.num = len(self.groups[self.group_cols[0]])
        L_order, L_value = np.array([]), np.array([])
        for i in range(self.num):
            group_df = self.my_df.reset_index().copy()
            for col in self.group_cols:
                group_df = group_df[group_df[col]==self.groups[col][i]]
            group_df = group_df[self.pr_col]
            if group_df.shape[1] == 1:
                group_df = group_df.iloc[:, 0]
            group_res = my_func(group_df)
            if not isinstance(group_res, pd.Series):
                group_res = pd.Series(group_res,
                                      index=group_df.index,
                                      name=group_df.name)
            L_order = np.r_[L_order, group_res.index]
            L_value = np.r_[L_value, group_res.values]
        self.res = pd.Series(pd.Series(L_value, index=L_order).sort_index(
                   ).values,index=self.my_df.reset_index(
                   ).index, name=my_func.__name__)
        return self.res
#1.实现单列分组
def f(s):
    '''max-min归一化'''
    res = (s-s.min())/(s.max()-s.min())
    return res
my_groupby(df, 'Type')['Price'].transform(f).head()
# 0    0.733592
# 1    0.372003
# 2    0.109712
# 3    0.186244
# 4    0.177525
# Name: f, dtype: float64
df.groupby('Type')['Price'].transform(f).head()  #这就是pandas官方提供的transform函数
# 0    0.733592
# 1    0.372003
# 2    0.109712
# 3    0.186244
# 4    0.177525
# Name: Price, dtype: float64


#2.实现多列分组，按照'Type','Country'这两列进行分组，数据是price列
my_groupby(df, ['Type','Country'])['Price'].transform(f).head()
# 0    1.000000
# 1    0.000000
# 2    0.000000
# 3    0.000000
# 4    0.196357
# Name: f, dtype: float64
df.groupby(['Type','Country'])['Price'].transform(f).head()  #这就是pandas官方提供的transform函数
# 0    1.000000
# 1    0.000000
# 2    0.000000
# 3    0.000000
# 4    0.196357
# Name: Price, dtype: float64


# 3.标量广播，下面以返回mean广播为例
my_groupby(df, 'Type')['Price'].transform(lambda x:x.mean()).head()
df.groupby('Type')['Price'].transform(lambda x:x.mean()).head()


#4.pandas 的 transform 不能跨列计算，请支持此功能，即仍返回 Series 但 col 参数为多列
#跨列计算，这是个很好的功能
a=my_groupby(df, 'Type')['Disp.', 'HP'].transform(lambda x: x['Disp.']/x.HP)
b=df['Disp.']/df['HP']
a.equals(b)  #所以可能transform的跨列计算应用场景不是太多
