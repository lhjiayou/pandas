# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 09:41:59 2022

@author: huanghao2
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#习题1：给定一个正整数列表，请找出缺失的最小正整数。
def get_miss(arr):
    #长度，最大值，最小值
    length=len(arr)
    maxv=max(arr)
    minv=min(arr)
    if minv!=1:
        return 1

    if maxv-minv+1==length:
        if minv==1:
            return maxv+1
        else:
            return minv-1
    else:
        arr=np.sort(arr)
        arr_diff=np.diff(arr)
        index=np.where(arr_diff!=1)[0]
        return (arr[index]+1)[0]

arr = np.array([2,3,4])
get_miss(arr)


arr = np.array([6,3,5,1,2])
get_miss(arr)

arr = np.array([5,2,1,3,4])
get_miss(arr)


#习题2：设计一个生成二维NumPy数组的函数get_res()，其输入为正整数n，
# 返回的数组构造方式如下：第1行填入1个1，第2行在上一行填入位置的下一列连续填入2个2，
# 第3行在第二行最后一个填入位置的下一列连续填入3个3，…，第n行在第n-1行最后一个填入位置的下一列连续填入n个n。
def get_res(n):
    A=np.zeros((n,np.arange(1,n+1).cumsum()[-1]))
    #for
    for i in range(n):
        A[i,np.arange(i+1).cumsum()[-1]:np.arange(i+2).cumsum()[-1]]=i+1
        
    #列表解析 ,每一个元素应当是表达式，而赋值是语句
    # [A[i,np.arange(i+1).cumsum()[-1]:np.arange(i+2).cumsum()[-1]]=i+1 for i in range(n)] 这为什么不对呢
    return A
n = 4
get_res(n)


#习题3:
n=5000   #步长
N=1000   #试验次数
k=100    #用于计算期望
random_number=np.random.random((N,k,n)) #1000次试验每次100个用于计算期望，步长为5000
random_number=np.where(random_number>0.5,1,-1)      #(1000,100,5000)

#接下来计算每次最终的sn是多少
terminal=random_number.cumsum(axis=2)[:,:,-1]     #（1000，100）
exception=np.mean(terminal,axis=1)
estimation=exception/np.sqrt(n)-np.sqrt(2/np.pi)
import matplotlib.pyplot as plt
plt.hist(estimation)   #可见几乎接近于正态分布


#习题4：
n, k = 1000, 10  #点数为1000，维度为k也就是具有10维特征
node_xy = np.random.rand(n, 2)
node_fea = np.random.rand(n, k)

def  cal_sigma(node_fea):
    num=node_fea.shape[0]
    sigma=np.zeros((num,num))
    for i in range(num):
        for j in range(num):
            sigma[i,j]=node_fea[i,:].dot(node_fea[j,:])/(np.linalg.norm(node_fea[i,:],2)*(np.linalg.norm(node_fea[j,:],2)))
    return sigma 
def cal_lambda(node_xy):
    #首先计算距离矩阵：
    dist_sq = np.sum((node_xy[:,np.newaxis,:] - node_xy[np.newaxis,:,:]) ** 2, axis=-1)
    nearest = np.argsort(dist_sq, axis=1)
    
    num=node_fea.shape[0]
    lamb=np.zeros((num,num))
    for i in range(num):
        for j in range(num):
            lamb[i,j]=1-2*(np.argwhere(nearest[i,:]==j)+1-1)/(num-1)
    return lamb
    
def get_S(node_xy, node_fea):
    sigma=cal_sigma(node_fea)
    lamb=cal_lambda(node_xy)
    return (sigma+lamb)/2
S=get_S(node_xy, node_fea)
    

