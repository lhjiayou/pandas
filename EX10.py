# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 22:38:10 2022

@author: 18721
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Ex1：太阳辐射数据集
df = pd.read_csv('data/solar.csv', usecols=['Data','Time', 'Radiation','Temperature'])  #32686*4
df.columns   #Index(['Data', 'Time', 'Radiation', 'Temperature'], dtype='object')
df.head()
# 1.将 Datetime, Time 合并为一个时间列 Datetime ，同时把它作为索引后排序。
solar_date = df.Data.str.extract('([/|\w]+\s).+')[0]  #利用正则表达式提取前面的日期数据
df['Data'] = pd.to_datetime(solar_date + df.Time)  #将上面获取的日期数据和后面的time时间数据组合成拼接字符串。
#并使用to_datetime转换成时间戳序列
df = df.drop(columns='Time')  #time列不再需要了
df=df.rename(columns={'Data':'Datetime'})  #改一下名字，现在就是合并的列datetime
df=df.set_index('Datetime')  #此列转换成index,现在只剩下两列
df=df.sort_index()  #按照时间的先后顺序完成了排序工作

# 2.每条记录时间的间隔显然并不一致，请解决如下问题：

# 2.a 找出间隔时间的前三个最大值所对应的三组时间戳。
s = df.index  #现在是DatetimeIndex对象，我们将其转换成sries
s=s.to_series() #转换成series之后，index是时间戳，其实并不需要
s=s.reset_index(drop=True)  #将index 变成默认的整数index
s=s.diff()  #作差，就能够得到时间间隔,只不过现在有min也有s不是很好对比
s=s.dt.total_seconds()  #将时间间隔以s为单位
# s.nlargest(3)就能够得到时间间隔最大的三个数据
# 25923    224689.0
# 24522    104100.0
# 7417      86693.0
max_3 = s.nlargest(3).index  #Int64Index([25923, 24522, 7417], dtype='int64')就是index
max_3.union(max_3-1) #Int64Index([7416, 7417, 24521, 24522, 25922, 25923], dtype='int64')就是三组时间戳的index
df.index[max_3.union(max_3-1)]
# DatetimeIndex(['2016-09-29 23:55:26', '2016-10-01 00:00:19',    得到的是时间间隔最大的三组时间戳
#                '2016-11-29 19:05:02', '2016-12-01 00:00:02',
#                '2016-12-05 20:45:53', '2016-12-08 11:10:42'],
#               dtype='datetime64[ns]', name='Datetime', freq=None)

# 2.b是否存在一个大致的范围，使得绝大多数的间隔时间都落在这个区间中？如果存在，请对此范围内的样本间隔秒数画出柱状图，设置 bins=50 。
res = s.mask((s>s.quantile(0.99))|(s<s.quantile(0.01)))   #mask是true的时候会替换成none，也就是大于0.99和小于0.01的替换成nan
res.count()/res.shape # 0.98060332 这就是绝大多数
plt.hist(res, bins=50)

# 3.求如下指标对应的 Series 
# 3.a 温度与辐射量的6小时滑动相关系数
res = df.Radiation.rolling('6H').corr(df.Temperature)
# 3.b 以三点、九点、十五点、二十一点为分割，该观测所在时间区间的温度均值序列
res = df.Temperature.resample('6H', origin='03:00:00').mean()
# 3.c 每个观测6小时前的辐射量（一般而言不会恰好取到，此时取最近时间戳对应的辐射量）
# 非常慢
my_dt = df.index.shift(freq='-6H')
int_loc = [df.index.get_indexer([i], method='nearest') for i in my_dt]
int_loc = np.array(int_loc).reshape(-1)
res = df.Radiation.iloc[int_loc]
res.index = df.index
res.tail(3)
# 纸质版上介绍了merge_asof，性能差距可以达到3-4个数量级
target = pd.DataFrame(
    {
        "Time": df.index.shift(freq='-6H'),
        "Datetime": df.index,
    }
)
res = pd.merge_asof(
    target,
    df.reset_index().rename(columns={"Datetime": "Time"}),
    left_on="Time",
    right_on="Time",
    direction="nearest"
).set_index("Datetime").Radiation



# Ex2：水果销量数据集
df = pd.read_csv('data/fruit.csv')
# 1.统计如下指标：
# 1.a 每月上半月（15号及之前）与下半月葡萄销量的比值
df.Date = pd.to_datetime(df.Date)  #首选转换时间戳
df_grape = df.query("Fruit == 'Grape'")  #选择出葡萄
res = df_grape.groupby([np.where(df_grape.Date.dt.day<=15,'First', 'Second'),df_grape.Date.dt.month])['Sale'].mean()
# Date
# First   1       66.349462    这个就是两级索引的数据
#         2       59.447059
#         3       57.502890
#         4       60.437838
#         5       57.135593
#         6       64.923977
#         7       65.653631
#         8       64.651515
#         9       63.297436
#         10      61.514851
#         11      58.608696
#         12      60.252941
# Second  1       56.467742
#         2       61.355828
#         3       60.443396
#         4       59.206522
#         5       61.366120
#         6       55.798030
#         7       55.407643
#         8       62.047619
#         9       59.117647
#         10      61.170854
#         11      57.108108
#         12      61.976048
res1=res.unstack(0)  #外层index转换成column，12*2
res2=res.unstack()  #默认是内层index转换成column，2*12
# res = df_grape.groupby([np.where(df_grape.Date.dt.day<=15,     参考答案上结果和上面的res1是一样的
#                         'First', 'Second'),df_grape.Date.dt.month]
#                         )['Sale'].mean().to_frame().unstack(0
#                         ).droplevel(0,axis=1)
res1 = (res1.First/res1.Second).rename_axis('Month')
# Month
# 1     1.174998
# 2     0.968890
# 3     0.951351
# 4     1.020797
# 5     0.931061
# 6     1.163553
# 7     1.184920
# 8     1.041966
# 9     1.070703
# 10    1.005624
# 11    1.026276
# 12    0.972197

# 1.b 每月最后一天的生梨销量总和
res=df[df.Date.dt.is_month_end]  #每月最后一天557*3
res=res.query("Fruit == 'Pear'") #进一步挑选出梨子的数据  130*3
res.groupby('Date')['Sale'].sum()
# Date
# 2019-01-31    847
# 2019-02-28    774
# 2019-03-31    761
# 2019-04-30    648
# 2019-05-31    616
# 2019-06-30    179
# 2019-07-31    757
# 2019-08-31    813
# 2019-09-30    858
# 2019-10-31    753
# 2019-11-30    859

# 1.c 每月最后一天工作日的生梨销量总和,不是最后一天，而是最后一个工作日
res=df[df.Date.isin(pd.date_range('20190101', '20191231', freq='BM'))]  #选出最后一个工作日570*3
res=res.query("Fruit == 'Pear'") #126*3 选出梨子
res.groupby('Date').Sale.sum()
# Date
# 2019-01-31     847
# 2019-02-28     774
# 2019-03-29     510
# 2019-04-30     648
# 2019-05-31     616
# 2019-06-28     605
# 2019-07-31     757
# 2019-08-30     502
# 2019-09-30     858
# 2019-10-31     753
# 2019-11-29    1193

# 1.d每月最后五天的苹果销量均值
target_dt = df.drop_duplicates().groupby(df.Date.drop_duplicates(
            ).dt.month)['Date'].nlargest(5).reset_index(drop=True)
res = df.set_index('Date').loc[target_dt].reset_index(
            ).query("Fruit == 'Apple'")
res = res.groupby(res.Date.dt.month)['Sale'].mean(
            ).rename_axis('Month')
# Month
# 1     65.313725
# 2     54.061538
# 3     59.325581
# 4     65.795455
# 5     57.465116
# 6     61.897436
# 7     57.000000
# 8     73.636364
# 9     62.301887
# 10    59.562500
# 11    64.437500
# 12    66.020000

# 2.按月计算周一至周日各品种水果的平均记录条数，行索引外层为水果名称，内层为月份，列索引为星期。
month_order = ['January','February','March','April',
                'May','June','July','August','September',
                'October','November','December']
week_order = ['Mon','Tue','Wed','Thu','Fri','Sat','Sum']
group1 = df.Date.dt.month_name().astype('category').cat.reorder_categories(
        month_order, ordered=True)
group2 = df.Fruit
group3 = df.Date.dt.dayofweek.replace(dict(zip(range(7),week_order))
         ).astype('category').cat.reorder_categories(
         week_order, ordered=True)
res = df.groupby([group1, group2,group3])['Sale'].count().to_frame(
         ).unstack(0).droplevel(0,axis=1)

#3.按天计算向前10个工作日窗口的苹果销量均值序列，非工作日的值用上一个工作日的结果填充。
df_apple = df[(df.Fruit=='Apple')&(
              ~df.Date.dt.dayofweek.isin([5,6]))]
s = pd.Series(df_apple.Sale.values,
              index=df_apple.Date).groupby('Date').sum()
res = s.rolling('10D').mean().reindex(
              pd.date_range('20190101','20191231')).fillna(method='ffill')