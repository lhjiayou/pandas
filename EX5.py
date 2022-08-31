# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:21:27 2022

@author: huanghao2
"""

import numpy as np
import pandas as pd

#习题1
'''Ex1：美国非法药物数据集
现有一份关于美国非法药物的数据集，其中 SubstanceName, DrugReports 分别指药物名称和报告数量：'''
# df1 = pd.read_csv('data/drugs(1).csv')
# df2 = pd.read_csv('data/Drugs.csv')
# df1.equals(df2)

df = pd.read_csv('data/drugs.csv').sort_values(['State','COUNTY','SubstanceName'],   #按照这些进行排序
                                               ignore_index=True)   #重新设置index



#1-1 将数据转为如下的形式：也就是将原本的年份 转换到列
df_pivot=df.pivot(index=['State','COUNTY','SubstanceName'], 
         columns='YYYY', 
         values='DrugReports')  #现在其实只有2010-2017的八列，['State','COUNTY','SubstanceName']都是index
df_pivot.head()
# YYYY                        2010  2011  2012  2013  2014  2015  2016  2017
# State COUNTY SubstanceName                                                
# KY    ADAIR  Buprenorphine   NaN   3.0   5.0   4.0  27.0   5.0   7.0  10.0
#              Codeine         NaN   NaN   1.0   NaN   NaN   NaN   NaN   1.0
#              Fentanyl        NaN   NaN   1.0   NaN   NaN   NaN   NaN   NaN
#              Heroin          NaN   NaN   1.0   2.0   NaN   1.0   NaN   2.0
#              Hydrocodone     6.0   9.0  10.0  10.0   9.0   7.0  11.0   3.0
#但事实上好像要求的结果是将这些index也转换到column中，那么还需要使用reset_index()

df_pivot=df.pivot(index=['State','COUNTY','SubstanceName'], 
         columns='YYYY', 
         values='DrugReports').reset_index() 
df_pivot.head()
# YYYY State COUNTY  SubstanceName  2010  2011  ...  2013  2014  2015  2016  2017
# 0       KY  ADAIR  Buprenorphine   NaN   3.0  ...   4.0  27.0   5.0   7.0  10.0
# 1       KY  ADAIR        Codeine   NaN   NaN  ...   NaN   NaN   NaN   NaN   1.0
# 2       KY  ADAIR       Fentanyl   NaN   NaN  ...   NaN   NaN   NaN   NaN   NaN
# 3       KY  ADAIR         Heroin   NaN   NaN  ...   2.0   NaN   1.0   NaN   2.0
# 4       KY  ADAIR    Hydrocodone   6.0   9.0  ...  10.0   9.0   7.0  11.0   3.0

#但是现在还存在YYYY的列名，那么就需要使用rename_axis将列名设置为空值
df_pivot=df.pivot(index=['State','COUNTY','SubstanceName'], 
         columns='YYYY', 
         values='DrugReports').reset_index().rename_axis(columns={'YYYY':''}) 
df_pivot.head()
#   State COUNTY  SubstanceName  2010  2011  2012  2013  2014  2015  2016  2017
# 0    KY  ADAIR  Buprenorphine   NaN   3.0   5.0   4.0  27.0   5.0   7.0  10.0
# 1    KY  ADAIR        Codeine   NaN   NaN   1.0   NaN   NaN   NaN   NaN   1.0
# 2    KY  ADAIR       Fentanyl   NaN   NaN   1.0   NaN   NaN   NaN   NaN   NaN
# 3    KY  ADAIR         Heroin   NaN   NaN   1.0   2.0   NaN   1.0   NaN   2.0
# 4    KY  ADAIR    Hydrocodone   6.0   9.0  10.0  10.0   9.0   7.0  11.0   3.0


#1-2 将第1问中的结果恢复为原表。
'''相当于现在要将宽表再变成长表
长宽表只是数据呈现方式的差异，但其包含的信息量是等价的，前面提到了利用 pivot 把长表转为宽表，
那么就可以通过相应的逆操作把宽表转为长表， melt 函数就起到了这样的作用。'''
df_melted = df_pivot.melt(id_vars = ['State','COUNTY','SubstanceName'],#这些列其实没有发生变化
                    value_vars = df_pivot.columns[-8:],  #需要从列变量转变成行变量
                    var_name = 'YYYY',  #需要从列变量转变成行变量  这个变量的新名字
                    value_name = 'DrugReports')  #需要从列变量转变成行变量  这个变量的值
df_melted.head()
#   State COUNTY  SubstanceName  YYYY  DrugReports
# 0    KY  ADAIR  Buprenorphine  2010          NaN
# 1    KY  ADAIR        Codeine  2010          NaN
# 2    KY  ADAIR       Fentanyl  2010          NaN
# 3    KY  ADAIR         Heroin  2010          NaN
# 4    KY  ADAIR    Hydrocodone  2010          6.0
#上面其实完成了从宽边变成长表，但是df.shape= (24062, 5)  然而由于存在nan，使得df_melted .shape  (49712, 5)
#也就意味着我们还需要删除掉nan

df_melted = df_pivot.melt(id_vars = ['State','COUNTY','SubstanceName'],
                    value_vars = df_pivot.columns[-8:], 
                    var_name = 'YYYY', 
                    value_name = 'DrugReports').dropna()  
df_melted.head()  #现在YYYY列不是第一列；排序和之前也不同；DrugReports列现在是浮点数



#所以完整的流程为：
df_melted = df_pivot.melt(id_vars = ['State','COUNTY','SubstanceName'],
                    value_vars = df_pivot.columns[-8:], 
                    var_name = 'YYYY', 
                    value_name = 'DrugReports').dropna() 
df_melted=df_melted[['YYYY','State','COUNTY','SubstanceName','DrugReports']].sort_values(
    ['State','COUNTY','SubstanceName'],ignore_index=True).astype(
        {'YYYY':'int64', 'DrugReports':'int64'})
df_melted.equals(df)  #下载是true


#1-3 按 State 分别统计每年的报告数量总和，其中 State, YYYY 分别为列索引和行索引，
'''要求分别使用 pivot_table 函数与 groupby+unstack 两种不同的策略实现，并体会它们之间的联系。'''
'''方式一，使用pivot_table，这个函数可以进行聚合'''
df_sum=df.pivot_table(index='YYYY',    #要求这个为行索引
         columns='State',   #要求这个为列索引
         values='DrugReports',
         aggfunc = 'sum')
# State     KY     OH     PA     VA    WV
# YYYY                                   
# 2010   10453  19707  19814   8685  2890
# 2011   10289  20330  19987   6749  3271
# 2012   10722  23145  19959   7831  3376
# 2013   11148  26846  20409  11675  4046
# 2014   11081  30860  24904   9037  3280
# 2015    9865  37127  25651   8810  2571
# 2016    9093  42470  26164  10195  2548
# 2017    9394  46104  27894  10448  1614
'''方式二，使用groupby进行聚合，操作是sum'''
df_sum1=df.groupby(['State', 'YYYY'])['DrugReports'].sum() #df.groupby(分组依据)[数据来源].使用操作    得到的是series，多级索引的
df_sum1=df.groupby(['YYYY','State'])['DrugReports'].sum().to_frame().unstack()#按照['YYYY','State']分组,unstack函数值就默认最内层
#但是现在column是多级的，外边存在DrugReports，这个需要删掉
df_sum1=df.groupby(['YYYY','State'])['DrugReports'].sum().to_frame().unstack().droplevel(0,axis=1)  #删掉level=0的最外层，而且是axis=1的列

df_sum1.equals(df_sum)  #说明相等







#习题2，
#Ex2：特殊的wide_to_long方法
'''从功能上看， melt 方法应当属于 wide_to_long 的一种特殊情况，即 stubnames 只有一类。
请使用 wide_to_long 生成 melt 一节中的 df_melted 。（提示：对列名增加适当的前缀）'''
df = pd.DataFrame({'Class':[1,2],
                  'Name':['San Zhang', 'Si Li'],
                  'Chinese':[80, 90],
                  'Math':[80, 75]})
df
#    Class       Name  Chinese  Math
# 0      1  San Zhang       80    80
# 1      2      Si Li       90    75
'''如果使用melt函数的时候：'''
df_melted = df.melt(id_vars = ['Class', 'Name'],   #这两列仍然保留，而且会生成笛卡尔积
                    value_vars = ['Chinese', 'Math'],   #这一列是变量值，从列变量压缩成行变量
                    var_name = 'Subject',  #给上面的变量  设置的列名
                    value_name = 'Grade')  #给上面的变量值 设置的列名
df_melted 
#    Class       Name  Subject  Grade
# 0      1  San Zhang  Chinese     80
# 1      2      Si Li  Chinese     90
# 2      1  San Zhang     Math     80
# 3      2      Si Li     Math     75
'''回顾wide_to_long函数'''
#先回顾一下这个函数的使用
df = pd.DataFrame({'Class':[1,2],'Name':['San Zhang', 'Si Li'],
                   'Chinese_Mid':[80, 75], 'Math_Mid':[90, 85],
                   'Chinese_Final':[80, 75], 'Math_Final':[90, 85]})
df
#    Class       Name  Chinese_Mid  Math_Mid  Chinese_Final  Math_Final
# 0      1  San Zhang           80        90             80          90
# 1      2      Si Li           75        85             75          85
#把 values_name 对应的 Grade 扩充为两列分别对应语文分数和数学分数，只把期中期末的信息压缩
df1=pd.wide_to_long(df,
                stubnames=['Chinese', 'Math'],  #这两列并不会被压缩，仍然以这个为列
                i = ['Class', 'Name'],  #形成index
                j='Examination',  #新增的index
                sep='_',  #上面df中的分隔符为_
                suffix='.+')
#                              Chinese  Math  这两列就是stubnames
# Class Name      Examination               
# 1     San Zhang Mid               80    90
#                 Final             80    90
# 2     Si Li     Mid               75    85
#                 Final             75    85
#这儿对应的是i    这儿对应j        只是压缩了期中期末为一列，但是数学和语文仍然是两列的
#就需要将原来的四个列给拆分开来
'''回到本题上来，用 wide_to_long 实现'''
#首先给列名增加适当的前缀，因为上面的例子中说明后面的mid和final会被压缩，但是前缀不会被压缩
df = pd.DataFrame({'Class':[1,2],
                  'Name':['San Zhang', 'Si Li'],
                  'Chinese':[80, 90],
                  'Math':[80, 75]})
df=df.rename(columns={'Chinese':'pre_Chinese',
                      'Math':'pre_Math'})  #可以使用sep='_'
df
#    Class       Name  pre_Chinese  pre_Math
# 0      1  San Zhang           80        80
# 1      2      Si Li           90        75

df_wtl=pd.wide_to_long(df,
                stubnames=['pre'],  #以这个为列
                i = ['Class', 'Name'],  #形成index
                j='Subject',  #新增的index
                sep='_',  #上面df中的分隔符为_
                suffix='.+')
df_wtl
#                          pre
# Class Name      Subject     
# 1     San Zhang Chinese   80
#                 Math      80
# 2     Si Li     Chinese   90
#                 Math      75
'''对照的df_melted 可见需要将三级索引全部转换到column，而且将列名从pre转换到grade,另外按照subject列排序
#    Class       Name  Subject  Grade
# 0      1  San Zhang  Chinese     80
# 1      2      Si Li  Chinese     90
# 2      1  San Zhang     Math     80
# 3      2      Si Li     Math     75'''
df_wtl=pd.wide_to_long(df,
                stubnames=['pre'],  #以这个为列
                i = ['Class', 'Name'],  #形成index
                j='Subject',  #新增的index
                sep='_',  #上面df中的分隔符为_
                suffix='.+').rename(columns={'pre':'Grade'}).sort_values('Subject').reset_index()
df_wtl
#    Class       Name  Subject  Grade  那么现在就和df_melted给出的结果完全相同了
# 0      1  San Zhang  Chinese     80
# 1      2      Si Li  Chinese     90
# 2      1  San Zhang     Math     80
# 3      2      Si Li     Math     75








































































