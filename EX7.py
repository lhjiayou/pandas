# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:24:18 2022

@author: 18721
"""

import numpy as np
import pandas as pd
#习题1
'''Ex1：缺失值与类别的相关性检验
在数据处理中，含有过多缺失值的列往往会被删除，除非缺失情况与标签强相关。
下面有一份关于二分类问题的数据集，其中 X_1, X_2 为特征变量， y 为二分类标签。'''
df = pd.read_csv('data/missing_chi.csv')  #1000*3
df.head()
#     X_1  X_2  y
# 0   NaN  NaN  0
# 1   NaN  NaN  0
# 2   NaN  NaN  0
# 3  43.0  NaN  0
# 4   NaN  NaN  0
df.isna().mean()  #可以查看每一列是na的比例，可见其实特征中有很多的缺失值，但是y标签的缺失数目为0
# X_1    0.855
# X_2    0.894
# y      0.000
# dtype: float64
df.y.value_counts(normalize=True)  #这是对y列的标签数目进行统计，而且归一化为0-1之间
# 0    0.918
# 1    0.082
# Name: y, dtype: float64
df.y.value_counts()   #这是对y列的标签数目进行统计
# 0    918
# 1     82
# Name: y, dtype: int64

'''下面是一个很好的问题：
事实上，有时缺失值出现或者不出现本身就是一种特征，并且在一些场合下可能与标签的正负是相关的。
关于缺失出现与否和标签的正负性，在统计学中可以利用卡方检验来断言它们是否存在相关性。
按照特征缺失的正例、 n11
    特征缺失的负例、 n10
    特征不缺失的正例、 n01
    特征不缺失的负例， n00
    可以分为四种情况，设它们分别对应的样例数为  。
    假若它们是不相关的，那么特征缺失中正例的理论值，就应该接近于特征缺失总数  总体正例的比例，即：
    n11特征缺失正值=(n11+n10)特征缺失总数*     (n11+n01)/(n11+n10+n01+n00)正值数/总数
    
    可以计算四个E/F
    进而计算S=(E-F)/F的和，应该服从X2(1)
    一般认为当此概率小于 0.05时缺失情况与标签正负存在相关关系，即不相关条件下的理论值与实际值相差较大。
    概率为2*2列联表检验问题的p值
    scipy.stats.chi2.sf(S, 1)计算概率值
    '''
# def calF(i,j):
#     F
from scipy.stats import chi2
def jianyan(column='X_1'):
    '''分别对两列进行检验'''
    E=pd.DataFrame(np.zeros((2,2)),
               index=['特征不缺失','特征缺失'],
               columns=['负例','正例'])
    F=pd.DataFrame(np.zeros((2,2)),
                   index=['特征不缺失','特征缺失'],
                   columns=['负例','正例'])
    n11=df[df['y']==1][column].isna().sum()  #y==1表示的正例，isna表示存在缺失，缺失的70个
    n10=df[df['y']==0][column].isna().sum() #y==0表示的负例，isna表示存在缺失
    n01=pd.Series(~df[df['y']==1][column].isna()).sum()  #y==1表示的正例，不缺失的12个
    n00=pd.Series(~df[df['y']==0][column].isna()).sum() #y==0表示的负例，isna表示存在缺失
    sumvalue=n11+n10+n01+n00
    
    E.iloc[0,0]=n00
    E.iloc[0,1]=n01
    E.iloc[1,0]=n10
    E.iloc[1,1]=n11
    
    F.iloc[0,0]=(n00+n01)*(n00+n10)/(sumvalue) #不缺失总数*负例总数/总数
    F.iloc[0,1]=(n00+n01)*(n01+n11)/(sumvalue) #不缺失总数*正例总数/总数
    F.iloc[1,0]=(n10+n11)*(n00+n10)/(sumvalue) #缺失总数*负例总数/总数
    F.iloc[1,1]=(n11+n10)*(n11+n01)/(sumvalue) #缺失总数*正例总数/总数
    
    #计算S
    S=((E-F)**2/F).sum().sum()
    
    #计算p值
    p=chi2.sf(S, 1) 
    
    return p
#一般认为当此概率小于0.05时缺失情况与标签正负存在相关关系，即不相关条件下的理论值与实际值相差较大。
p_x1=jianyan()  #0.9712760884395901，说明不存在相关关系
p_x2=jianyan(column='X_2')    #7.459641265637543e-166 ，说明存在相关关系



#习题2
'''Ex2：用回归模型解决分类问题
KNN 是一种监督式学习模型，既可以解决回归问题，又可以解决分类问题。
对于分类变量，利用 KNN 分类模型可以实现其缺失值的插补，
思路是度量缺失样本的特征与所有其他样本特征的距离，
当给定了模型参数 n_neighbors=n 时，
计算离该样本距离最近的 n个样本点中最多的那个类别，
并把这个类别作为该样本的缺失预测类别，
具体如下图所示，未知的类别被预测为黄色：'''
df = pd.read_excel('data/color.xlsx')
df.dtypes
# X1       float64
# X2       float64
# Color     object
# dtype: object
df = df.convert_dtypes() 
df.dtypes
# X1       Float64
# X2       Float64
# Color     string   实现object转化成str类型
# dtype: object
df.head(3)  #23*3个数据

from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=6)  #实例化分类器
clf.fit(df.iloc[:,:2].values,    df.Color.values) #前两列作为特征x
clf.predict([[0.8, -0.2]])  
#为什么必须要两个[]，外层的[]表示的是数据点列表，内层的[]表示数据必须为(sample,2)的排列

'''2-1:
对于回归问题而言，需要得到的是一个具体的数值，因此预测值由最近的 n个样本对应的平均值获得。
请把上面的这个分类问题转化为回归问题，仅使用 KNeighborsRegressor 
来完成上述的 KNeighborsClassifier 功能。'''

def trans(x):
    if x=='Blue':
        return 0
    elif x=='Yellow':
        return 1
    else :
        return 2
df_copy=df.copy()
df_copy['Color']=df_copy['Color'].apply(trans)

from sklearn.neighbors import KNeighborsRegressor 
reg=KNeighborsRegressor(n_neighbors=6)
reg.fit(df_copy.iloc[:,:2].values,    df_copy.Color.values)
reg.predict([[0.8, -0.2]]).round() #1，因此也就是yellow

'''2-2
请根据第1问中的方法，对 audit 数据集中的 Employment 变量进行缺失值插补。
也就是使用KNN进行插补'''
df = pd.read_csv('data/audit.csv')  #2000*7
# df.head(3)
df.isna().mean() 
# ID            0.00
# Age           0.00
# Employment    0.05   可见employment存在缺失值
# Marital       0.00
# Income        0.00
# Gender        0.00
# Hours         0.00
# dtype: float64
# df.dtypes
df = df.convert_dtypes() 

emp=df.Employment.unique()    #Employment列的情况
#建立映射，转换成整数编码
dict_emp=dict([(emp[i],i) for i in range(len(emp))])

df_copy=df.copy()
df_copy.Employment=df_copy.Employment.apply(lambda x:dict_emp[x])


reg=KNeighborsRegressor(n_neighbors=6)
reg.fit(df_copy.loc[:,['Income','Hours']].values,    df_copy.Employment.values)

df_copy.loc[df_copy.Employment==dict_emp[pd.NA],'Employment']=reg.predict(
    df_copy.loc[df_copy.Employment==dict_emp[pd.NA],['Income','Hours']].values).round()
#加上values可以避免warning：
 # X has feature names, but KNeighborsRegressor was fitted without feature names
