# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 21:10:39 2022

@author: 18721
"""
import numpy as np
import pandas as pd

# Ex1：房屋信息数据集
df = pd.read_excel('data/house_info.xls', usecols=[
                'floor','year','area','price'])   #31568*4
df.head(3)
#       floor  year    area price
# 0   高层（共6层）  1986  58.23㎡  155万
# 1  中层（共20层）  2020     88㎡  155万
# 2  低层（共28层）  2010  89.33㎡  365万

#1 将 year 列改为整数年份存储。
df['year']=df['year'].str.replace('年建', '', regex=True)  #其实就是把年建替换成''节

#2 将 floor 列替换为 Level, Highest 两列，
#其中的元素分别为 string 类型的层类别（高层、中层、低层）与整数类型的最高层数。
df['Level']=df['floor'].str[:2]
pat = '(\d+)'
df['Highest']=df['floor'].str.extract(pat)

# 3 计算房屋每平米的均价 avg_price ，以 ***元/平米 的格式存储到表中，其中 *** 为整数。
#首先将价格列去掉万
df['price']=df['price'].str.replace('万','',regex=True)
# 然后将价格后面加上四个0转换成元的单位
df['price']=pd.Series([''.join([df['price'][i],'0000']) for i in range(df.shape[0])]).astype(np.float32)
#计算平均价格
df['avg_price']=df['price']/df['area'].str.replace('㎡','',regex=True).astype(np.float32).astype('string')
#加上'元/平米'
df['avg_price']=pd.Series([''.join([df['avg_price'][i],'元/平米']) for i in range(df.shape[0])])

# Ex2：《权力的游戏》剧本数据集
df = pd.read_csv('data/script.csv')
df.head(3)
# 1计算每一个 Episode 的台词条数。
# df.columns  可见这个列的右边其实是有空格的Episode 
df['Episode_num']=df['Episode '].str.extract('e (\d+)')


# 2以空格为单词的分割符号，请求出单句台词平均单词量最多的前五个人。
#先分割sentence
df['Sentence_split']=df['Sentence'].str.split(' ') 
#再求得每个sentence的长度
df['Sentence_split_num']=df['Sentence_split'].str.len()
#再排序求取长度
np.argmax(df['Sentence_split_num'])  #好像最长的是332
idx=np.argsort(df['Sentence_split_num'])[::-1][:5]  #因为默认是降序排列的
result=df['Name'].iloc[idx]
# 6282               talisa  前五长的台词的索引以及人名
# 8736      jaime lannister
# 1300       alliser thorne
# 13542    tyrion lannister
# 14919             brienne
# Name: Name, dtype: object


# 3若某人的台词中含有问号，那么下一个说台词的人即为回答者。若上一人台词中含有n个问号，
# 则认为回答者回答了n个问题，请求出回答最多问题的前五个人。
'''其实找到问问题的问号最多的，然后在其索引上加1就是回答问题的人了'''
df['Sentence_split_?num']=df['Sentence'].str.count('\?')
idx_q=np.argsort(df['Sentence_split_?num'])[::-1][:5]  
# df.loc[idx_q.iloc[0],'Sentence']  确实存在九个问号
idx_a=idx_q+1
result=df['Name'].iloc[idx_a]
# 15420    daenerys targaryen  前五的回答问题最多的人的索引及其人名
# 9747                  davos
# 9827             melisandre
# 23801           sansa stark
# 16741                 tyene
# Name: Name, dtype: object
