# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 21:03:02 2022

@author: 18721
"""

# Ex5：统计每个学区的开课数量
# 某个城市共有4个学区，每个学区有若干学校，学校之间名字互不相同。每一条记录为该学校开设的课程，
# 一个学校可能有多条记录，每一条记录内部的课程不会重复，但同一学校不同记录之间的课程可能重复。
import pandas as pd
df = pd.read_csv('D:\！datawhale学习\pandas\exercise\data\ex5/school_course.csv')
df.shape  #(1921, 3)

# 课程的种类共有100门，编号为”school_1”到”school_100”。现要统计每个学区各项课程的开设学校数量，
#这个是不是写错了，应该是course把？

df['course_some']=[df['Course'].iloc[i].split(' ') for i in range(df.shape[0])]
#然后怎么把这一列，现在是课程列表给展开呢

