# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 21:55:58 2022

@author: 18721
"""
import pandas as pd


# 习题1：公司员工数据集  
df = pd.read_csv('data/company.csv')    #[6284 rows x 7 columns]
# df.info() 
# df.head(3)
# df.shape  (6284, 7)



#1.1 分别只使用 query 和 loc 选出年龄不超过四十岁且工作部门为 Dairy 或 Bakery 的男性。
#使用query，其实写法很是灵活  [441 rows x 7 columns]
df.query("(age<=40)" 
         "and (department==['Dairy' , 'Bakery'])"   
         " and (gender=='M') ")

df.query("(age<=40)" 
         "and ((department=='Dairy')"
         "or (department=='Bakery'))"
         " and (gender=='M') ")

df.query("(age<=40)" 
         "and (department in ['Dairy' , 'Bakery'])"   
         " and (gender=='M') ")

#使用loc,可以条件拆分的很清楚
con1=df['age']<=40
con2_1=df['department']=='Dairy' 
con2_2=df['department']=='Bakery'
con2=con2_1 | con2_2
con3=df['gender']=='M'
con=con1 & con2 & con3
df.loc[con]            #[441 rows x 7 columns]
#其实也可以使用isin方法
df.loc[(df.age<40)&(df.department.isin(["Dairy","Bakery"]))&(df.gender=='M')]

#1.2 选出员工 ID 号 为奇数所在行的第1、第3和倒数第2列。
con=df['EmployeeID']%2==1
selected_columns=df.columns[[0,2,-2]]  
#选出来index为Index(['EmployeeID', 'age', 'job_title'], dtype='object')
df.loc[con,selected_columns]  #[3126 rows x 3 columns]

# 1.3 index 的操作
'''把后三列设为索引后交换内外两层'''
selected_columns=list(df.columns[-3:])    #Index(['department', 'job_title', 'gender'], dtype='object')
df_ex1=df.set_index(selected_columns)
df_ex1.head()
#使用swaplevel来交换
df_ex1=df_ex1.swaplevel(0,2)
df_ex1.head()  #[6284 rows x 4 columns]
'''恢复中间层索引'''
df_ex2=df_ex1.reset_index(['job_title'])
df_ex2.head()  #[6284 rows x 5 columns]
'''修改外层索引名为 Gender'''
df_ex3=df_ex2.rename_axis(index={'gender':'Gender'})  
df_ex3_1=df_ex2.rename_axis(index=lambda x:str.title(x) if x=='gender' else x)
'''用下划线合并两层行索引'''
df_ex4=df_ex3.copy()
new_index=df_ex3.index.map(lambda x:(x[0]+'_'+x[1]))
new_index_1=df_ex3.index.map(lambda x:'_'.join(x))
df_ex4.index=new_index_1
df_ex4.head()
'''把行索引拆分为原状态'''
df_ex5=df_ex4.copy()
df_ex5.head()
#                       job_title  EmployeeID birthdate_key  age  city_name
# M_Executive                 CEO        1318      1/3/1954   61  Vancouver
# F_Executive           VP Stores        1319      1/3/1957   58  Vancouver
# F_Executive       Legal Counsel        1320      1/2/1955   60  Vancouver
# M_Executive  VP Human Resources        1321      1/2/1959   56  Vancouver
# M_Executive          VP Finance        1322      1/9/1958   57  Vancouver
new_idx = df_ex4.index.map(lambda x:tuple(x.split('_')))
df_ex5.index=new_idx
df_ex5.head()   #但是可见现在是没有Gender department的
#                       job_title  EmployeeID birthdate_key  age  city_name
# M Executive                 CEO        1318      1/3/1954   61  Vancouver
# F Executive           VP Stores        1319      1/3/1957   58  Vancouver
#   Executive       Legal Counsel        1320      1/2/1955   60  Vancouver
# M Executive  VP Human Resources        1321      1/2/1959   56  Vancouver
#   Executive          VP Finance        1322      1/9/1958   57  Vancouver
# df_ex5.index.names   因为没有了index的name，现在FrozenList([None, None])
'''修改索引名为原表名称'''
df_ex6=df_ex5.copy()
df_ex6=df_ex6.rename_axis(index=['Gender','department'])   #现在完成了重新添加index的名字属性
'''恢复默认索引并将列保持为原表的相对位置'''
#其实也就是恢复默认的整数索引
df_ex7=df_ex6.copy()
df_ex7=df_ex7.rename_axis(index=['gender','department'])
df_ex7=df_ex7.reset_index().reindex(df.columns,axis=1) 

# (df_ex7==df).all().all()  可见各行各列都是完全相同的






#习题2：Ex2：巧克力数据集
import pandas as pd
df = pd.read_csv('data/chocolate.csv')  #[1795 rows x 5 columns]

#2.1 把列索引名中的 \n 替换为空格
#方式一，使用rename函数
df1=df.copy()
df1=df1.rename(columns=lambda x:' '.join(x.split('\n'))) 
df1.head()
#方式二，直接重新赋值
df1=df.copy()
df1.columns=[' '.join(i.split('\n')) for i in df.columns]
df1.head()

#2.2 巧克力 Rating 评分为1至5，每0.25分一档，请选出2.75分及以下且可可含量 Cocoa Percent 高于中位数的样本。
# df1.info()   #2   Cocoa Percent     1795 non-null   object 现在并不是数值型，而是字符串类型
#因此我们需要将这一列先转换成数值型，才能计算中位数
df2=df1.copy()
df2['Cocoa Percent']=df2['Cocoa Percent'].apply(lambda x:float(x[:-1])/100)  #因为-1位置是%
# df2.info()   2   Cocoa Percent     1795 non-null   float64
df2.head()
#接下来的筛选，还使用最简单的query方便实现,
#但是对于含有空格的列名，需要使用 `col name` 的方式进行引用。
#这个符号是反单引号，是esc按键下面的`(英文格式下)
df2.query('Rating<=2.75 & `Cocoa Percent`>`Cocoa Percent`.median()') #[239 rows x 5 columns]


#2.3 将 Review Date 和 Company Location 设为索引后，
# 选出 Review Date 在2012年之后且 Company Location   
# 不属于 France, Canada, Amsterdam, Belgium 的样本
'''解析，要求先设置为index，然后多级索引进行切片，就需要使用IndexSlice对象'''
idx = pd.IndexSlice
exclude = ['France', 'Canada', 'Amsterdam', 'Belgium'] #Company Location要排除的list
df3 = df1.set_index(['Review Date','Company Location']).sort_index()

#然后进行切片  [972 rows x 3 columns]
df3.loc[idx[2012:,~df3.index.get_level_values(1).isin(exclude)],  #行的切片
        :]                                                        #列没有任何的筛选








