# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 17:21:36 2022

@author: 18721
"""
import pandas as pd
import numpy as np

# Ex2：统计学生的成绩情况
# 在data/supplement/ex2目录下存放了某校高三第一学期的学生成绩情况，包含16次周测成绩、期中考试成绩和期末考试成绩，
# 科目一栏的成绩表示学生选课的成绩。所有的表中，相同的行表示的是同一位同学。请完成以下练习：
file_path=r'D:\！datawhale学习\pandas\exercise\data\ex2/第1次周测成绩.csv'
df = pd.read_csv(file_path)  #896*7的数据
# df.head()
#    班级   姓名  选科   语文  数学   英语  科目
# 0   1   吴刚  地理   93  95   82  69
# 1   1   卢楠  物理  108  77   90  94
# 2   1  唐秀兰  历史   88  72   95  85
# 3   1   张刚  化学   85  88  102  76
# 4   1   姜洋  历史  104  99   84  86

# 2-1 该校高三年级中是否存在姓名相同的学生？
len(df['姓名'])  #=896,因为我们存在896条记录
len(df['姓名'].unique()) #也等于896，那么就表明不存在姓名的重复

# 2-2在第一次周测中，请求出每个班级选修物理或化学同学的语数英总分的平均值。哪个班级最高？
'''解析：这好像是需要按照班级进行分组'''
'''step1:可以首先将会语数英三门课总分计算出来'''
df_copy=df.copy()
df_copy['total']=df[df.columns[3:6]].sum(axis=1)
'''step2:选出选课为物理或者化学的'''
df_copy_wuli=df_copy[df_copy['选科']=='物理']  #131
df_copy_huaxue=df_copy[df_copy['选科']=='化学']  #246
df_selected=pd.concat([df_copy_wuli,df_copy_huaxue],axis=0)  #377
result2=df_selected.groupby('班级')['total'].mean()
# 输出结果为：
# 班级
# 1     274.727273
# 2     281.818182
# 3     269.794118
# 4     265.522727
# 5     268.676471
# 6     272.894737
# 7     270.818182
# 8     268.162162
# 9     270.071429
# 10    268.675676
# 11    262.076923
# Name: total, dtype: float64
result2[result2==result2.max()].index 
#可见是二班的选修物理或化学同学的语数英总分的平均值最高


# 2-3学生在该学期的总评计算方式是各次考试总分的加权平均值，
# 其中周测成绩权重为50%（每次测验权重相等，即3.125%），期中权重为20%，期末权重为30%。
# 请结合nlargest函数找出年级中总评前十的同学。
'''总共有16次周测，一次期中，一次期末'''
#step1:读取数据
import os
path = r'D:\！datawhale学习\pandas\exercise\data\ex2/'
#os.listdir(path)可以返回这个路径下的所有文件
df_list=[]
for file_name in os.listdir(path):
    df_list.append(pd.read_csv(path+file_name))
#step2：计算加权分数
for idx in range(len(df_list)):
    df_list[idx]['total']=df_list[idx][df_list[idx].columns[-4:]].sum(axis=1)
    if idx==0:
        df_list[idx]['weighted_total']=0.2*df_list[idx]['total']
    elif idx==1:
        df_list[idx]['weighted_total']=0.3*df_list[idx]['total']
    else:
        df_list[idx]['weighted_total']=0.03125*df_list[idx]['total']
#step3：拼接成一张表并计算最高的分数
df_total=df_list[0][['姓名','weighted_total']]
for idx in range(1,len(df_list)):
    df_total=df_total.merge(df_list[idx][['姓名','weighted_total']],
                            on='姓名')
df_total.columns=['姓名']+list(range(18))
df_total['weighted_score']=df_total[df_total.columns[1:]].sum(axis=1)
df_result=df_total[['姓名','weighted_score']].set_index('姓名')
df_result.nlargest(10,columns='weighted_score')
#分数最高的十个人为：
#      weighted_score
# 姓名                 
# 王想        427.20000
# 黄萍        413.24375
# 黄文        413.00000
# 黎玉        412.13750
# 王淑英       410.63125
# 慕阳        410.62500
# 张欢        410.47500
# 杨凤兰       410.47500
# 吕雪        410.18750
# 孙桂珍       409.64375


# 2-4 请统计1班到8班文理科（物化生为理科，政史地为文科）期末考试总分前5的学生，
# 结果格式如下，括号内的为选科分数
#  1班（文） 1班（理） 2班（文）  ... 8班（理）
# 0  王大锤：历史（102）   ...   ...  ...   ...
# 1          ...   ...   ...  ...   ...
# 2          ...   ...   ...  ...   ...
# 3          ...   ...   ...  ...   ...
# 4          ...   ...   ...  ...   ...：
#step1:首先区分文理科，计算总分
file_path=r'D:\！datawhale学习\pandas\exercise\data\ex2/期末考试成绩.csv'
df = pd.read_csv(file_path)
def wenlike(x):
    if x in ['物理' , '化学','生物']:
        return '理'
    else:
        return '文'
df['文理科']=df['选科'].apply(wenlike)
df['total']=df[df.columns[3:7]].sum(axis=1)

#step2:先将结果以名字为result的dataframe写出来
columns=[str(i)+'班('+j+')' for i in range(1,9) for j in ['文','理']]
result=pd.DataFrame(np.zeros((5,16)),columns=columns)

for i in range(1,9):
    for j in ['文', '理']:    
        condition1=df['班级']==i
        condition2=df['文理科']==j
        condition= condition1 & condition2
        df_selected=df.loc[condition]   # 选出班级和文理科
        df_selected=df_selected.nlargest(5,columns='total').reset_index(drop=True)
        for k in range(5):
            result.loc[k,str(i)+'班('+j+')']=df_selected.loc[
                k,'姓名']+':'+df_selected.loc[k,'选科']+'('+str(
                    df_selected.loc[k,'科目'])+')'

# 2-5 学生成绩的稳定性可以用每次考试在全年级相同选科学生中的总分排名标准差来度量，
# 请计算每个班级的各科学生成绩稳定性的均值，结果格式如下：
result=pd.DataFrame(
    np.random.rand(11, 6),
    index=pd.Index(range(1, 12), name="班级"),
    columns=pd.Index(
        ["物理", "化学", "生物", "历史", "地理", "政治"],
        name="选科",  #这是给column设置的列名
    )
)
path=r'D:\！datawhale学习\pandas\exercise\data\ex2/'
file_name=['第'+str(i)+'次周测成绩.csv' for i in range(1,17)]+['期中考试成绩.csv','期末考试成绩.csv']
df_list=[pd.read_csv(path+i) for i in file_name]
#计算总分
for i in df_list:
    i['total']=i[i.columns[-4:]].sum(axis=1)
#计算每次考试所有人的分数
score=pd.DataFrame(
    
    index=pd.Index(range(18), name="考试"),
    columns=pd.Index(
        ["物理", "化学", "生物", "历史", "地理", "政治"],
        name="选科",  #这是给column设置的列名
    )
)
for i in range(len(df_list)):
    for j in ["物理", "化学", "生物", "历史", "地理", "政治"]:
        score.loc[i,j]=np.sort(df_list[i][df_list[i]['选科']==j]['total'].values)[::-1]  #降序排列
#计算排名  
for i in range(len(df_list)):  #i是哪一次考试
    for j in range(896):   #j是哪个人
        df_list[i].loc[j,'rank']=np.argwhere(score.loc[i,df_list[i].loc[j,'选科']]==df_list[i].loc[j,'total']
                                             ).mean()  #同分数排名取均值
#计算每个人的标准差
std=pd.read_csv(path+file_name[0],usecols=['班级','姓名','选科'])
for j in range(896):
    ranks=np.array([df_list[i].loc[j,'rank'] for i in range(18)])
    std.loc[j,'stds']=ranks.std()
#计算最终结果
for i in range(1,12):  #每个班
    for j in ["物理", "化学", "生物", "历史", "地理", "政治"]: #每个学科
        con1=std['班级']==i  
        con2=std['选科']==j
        condition=con1 & con2    #某班级的某科目的这些人选出来     
        result.loc[i,j]=std[condition]['stds'].mean() 
#结果为：
# 班级	物理	化学	生物	历史	地理	政治
# 1	35.19977012705938	69.12004965720925	46.52959297328492	36.631958485576725	33.961217635452115	26.12882219134848
# 2	37.80881536714125	68.00804118149925	47.02914502021832	38.39597106513746	34.471399392131325	25.91717420044679
# 3	37.631964290319274	72.88546351019244	45.75805759044808	37.217393942637486	37.424588638773656	26.877795200604343
# 4	37.14841681218041	68.91972345353315	46.231277476229224	37.42759665143528	35.515790390374896	27.487126190225545
# 5	37.303735780317545	70.01900267545591	46.10280959052551	35.8343978838266	35.49784675032034	23.911957805984876
# 6	35.76703194119874	66.2712526982197	47.89402637447265	37.28284575023341	34.13434103203581	27.409160341649095
# 7	37.171084532037426	69.10947474175354	45.83085625911735	36.72872193859634	35.22172564589509	26.63923633826787
# 8	37.6422587201179	69.95619460863266	48.2365598346402	35.84816932503859	35.488483846227695	26.831655781130866
# 9	35.35991462906696	63.79289177042855	45.737982217726284	38.382912685477464	36.82818034561264	26.362862318143012
# 10	36.178005502313404	68.79581434247977	44.102319796268276	38.55929404073579	35.66685031488418	25.824683292988553
# 11	34.391404272714524	69.23845264073638	42.813169943272605	34.37803491255943	36.62963405454347	25.778698687410245









