# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 23:22:17 2022

@author: 18721
"""

import numpy as np
import pandas as pd
# Ex3：统计商品的审核情况
# 在data/supplement/ex3中存放了两个有关商品审核的信息表，“商品信息.csv”中记录了每个商品的ID号，
# 唯一的识别码以及商品所属的类别，“申请与审核记录.csv”中记录了每个商品的审核信息。
# 已知商品的审核流程如下：由申请人发起商品审核的申请，然后由审核人审核，审核的结果包括通过与不通过两种情况，
# 若商品不通过审核则可以由另一位申请人再次发起申请，直到商品的审核通过。
path=r'D:\！datawhale学习\pandas\exercise\data\ex3/'
df_info = pd.read_csv(path+'商品信息.csv')
df_info.head()
#          ID号      识别码  类别
# 0  ID 000001  CRtXJUK  T1
# 1  ID 000002  RGSxifC  Q1
# 2  ID 000003  AboduTp  S1
# 3  ID 000004  zlpUeMl  S2
# 4  ID 000005  IVQqhIK  S3
df_record = pd.read_csv(path+'申请与审核记录.csv')
df_record.head()
#          ID号         申请人        申请时间         审核人        审核时间   结果
# 0  ID 000001  \#+3((52\{  2020-04-19  ~1=6\*183|  2020-05-03  未通过
# 1  ID 000001  8@75[1|2\*  2020-05-10  15![3\({59  2020-07-17  未通过
# 2  ID 000001  }!7)(#^0*7  2020-07-28  3`}04}%@75  2020-08-23   通过
# 3  ID 000002  |*{20#9|}5  2020-01-05  ={`8]03*4+  2020-03-09  未通过
# 4  ID 000002  4~6%)455`[  2020-03-14  =$-36[)|8]  2020-04-21  未通过
'''再次回顾一下申请流程：
已知商品的审核流程如下：由申请人发起商品审核的申请，然后由审核人审核，审核的结果包括通过与不通过两种情况，
若商品不通过审核则可以由另一位申请人再次发起申请，直到商品的审核通过。'''

# 3-1有多少商品最终通过审核？
np.sum(df_record['结果']=='通过')  #10848

# 3-2 各类别商品的通过率分别为多少？
df_pass=df_record[df_record['结果']=='通过']   #所有通过的记录
df_pass=df_pass[['ID号','结果']]
df_info_copy=df_info.merge(df_pass,on='ID号',how='left')
#将通过的设置为1，没通过的设置为0
def pas(x):
    if type(x)==float:
        return 0
    else:
        return 1
df_info_copy['结果']=df_info_copy['结果'].apply(pas)
# type(df_info_copy.loc[0,'结果']) 是str
# type(df_info_copy.loc[1,'结果']) 是float
#然后分组计算通过率
df_info_copy.groupby('类别')['结果'].mean()
# 类别
# Q1    0.395866
# Q2    0.406604
# S1    0.402618
# S2    0.408443
# S3    0.414896
# T1    0.398679
# T2    0.402781
# Name: 结果, dtype: float64

# 3-3 对于类别为“T1”且最终状态为通过的商品，平均审核次数为多少？
#首先选出类别为“T1”且最终状态为通过的商品
df_record_copy=df_record.merge(df_info,on='ID号',how='left')
condition1=df_record_copy['类别']=='T1'
condition2=df_record_copy['结果']=='通过'
condition= condition1 & condition2
df_record_copy=df_record_copy[condition]  #总共有1509条记录
print('平均审核次数为：',np.array([
    df_record[df_record['ID号']==i].shape[0] for i in df_record_copy['ID号']]).mean())
# 平均审核次数为： 5.547382372432074

# 3-4 是否存在商品在上一次审核未完成时就提交了下一次审核申请？
df_record_copy=df_record[['ID号','申请时间','审核时间']]
df_record_copy['申请时间']=pd.to_datetime(df_record_copy['申请时间'])
df_record_copy['审核时间']=pd.to_datetime(df_record_copy['审核时间'])
#下面外层是26832条记录，内层虽然记录数目不一致，但是可以得知实际将要执行147500-26832判断，很慢
#这个应该有什么比较好的解决方法，需要关注！！！
for i in df_record_copy['ID号'].unique():
    record=np.array(df_record_copy[df_record_copy['ID号']==i].index)  #这条商品的记录
    for j in range(len(record)-1):  #最后一个不需要      
        if df_record_copy.loc[record[j],'审核时间'] > df_record_copy.loc[record[j+1],'申请时间']:
            print('出现了商品在上一次审核未完成时就提交了下一次审核申请')
            print(i)
#上面没有输出任何结果，表明不存在商品在上一次审核未完成时就提交了下一次审核申请情况的发生
            
# 3-5 请对所有审核通过的商品统计第一位申请人和最后一位审核人的信息，返回格式如下：
# ID号   类别         申请人         审核人
# 1    ID 000001   T1  \#+3((52\{  3`}04}%@75
# 2          ...  ...         ...         ...
# 3          ...  ...         ...         ...
# ...        ...  ...         ...         ...
df_pass=df_record[df_record['结果']=='通过'] 
df_pass=df_pass.merge(df_info,on='ID号',how='left')
df_pass=df_pass[['ID号'   ,'类别'     ,   '申请人'    ,     '审核人']]  #但是现在的申请人并不是第一位申请人
for i in df_pass['ID号']:
    record=np.array(df_record[df_record['ID号']==i].index)[0]  #这条商品的第一条记录
    df_pass.loc[df_pass['ID号']==i,'申请人']=df_record.loc[record,'申请人']











