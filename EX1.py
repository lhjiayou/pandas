# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 22:55:58 2022

@author: 18721
"""
import numpy as np
np.random.seed(0)

#习题1：利用列表推导式写矩阵乘法
M1 = np.random.rand(2,3)
M2 = np.random.rand(3,4)
res = np.empty((M1.shape[0],M2.shape[1]))
for i in range(M1.shape[0]):
    for j in range(M2.shape[1]):
        item = 0
        for k in range(M1.shape[1]):
            item += M1[i][k] * M2[k][j]
        res[i][j] = item
(np.abs((M1@M2 - res) < 1e-15)).all() # 排除数值误差返回的是true

'''我的写法'''
my_solution=np.array([M1[i,:].dot(M2[:,j]) for i in range(M1.shape[0]) for j in range(M2.shape[1])]).reshape(M1.shape[0],M2.shape[1])
(np.abs((M1@M2 - my_solution) < 1e-15)).all()  #同样也是可以返回true
'''参考答案'''
res1 = np.array([[sum([M1[i][k] * M2[k][j] for k in range(M1.shape[1])]) for j in range(M2.shape[1])] for i in range(M1.shape[0])])
(np.abs((M1@M2 - res1) < 1e-15)).all()
'''解法对比，我的解法中使用了dot，也就是k的循环没有用列表解析写，而是直接dot了
另外，如果在我的写法中不用reshape，但是保留dot的话，也应该像参考答案一样写两个[]嵌套
'''
my_solution2=np.array([[M1[i,:].dot(M2[:,j]) for j in range(M2.shape[1])]for i in range(M1.shape[0]) ])
(np.abs((M1@M2 - my_solution2) < 1e-15)).all()  




#习题2：更新矩阵
#首先我们可以不使用numpy的向量化操作，就使用for循环得到结果,虽然是最耗时但却是最直观的方式
A=np.arange(1,10).reshape(3,-1)
B=np.zeros(shape=A.shape) 
for i in range(A.shape[0]):
     for j in range(A.shape[1]):
         B[i,j]=A[i,j]*np.sum(1/A[i,:])
# B[1,1]=3.0833333333333335,就是37/12

'''我的写法'''
B1=np.array([A[i,j]*np.sum(1/A[i,:]) for i in range(A.shape[0]) for j in range(A.shape[1])]).reshape(A.shape[0],A.shape[1])
(B==B1).all()  #返回的就是true
'''参考答案'''
B2 = A*   (1/A).sum(1).reshape(-1,1)
(B==B2).all() 
'''分析答案，对比差距
 (1/A).sum(1).reshape(-1,1)就是求和部分的内容，其shape为[3,1]

按照广播的规则是[3,1]广播成[3,3]然后再与A进行逐元素的乘积
B4=A*np.repeat((1/A).sum(1).reshape(-1,1),3,axis=1)，这是手动实现的广播
(B==B4).all()
'''

#习题3，卡方统计量
np.random.seed(0)
A = np.random.randint(10, 20, (8, 5))
#首先按照常规思路写一下
B=np.zeros(shape=A.shape)
for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        B[i,j]=np.sum(A[:,j])*np.sum(A[i,:])/np.sum(A)
x2=np.sum((A-B)**2/B)  #11.842696601945802

'''我的写法'''
B1=np.array([np.sum(A[:,j])*np.sum(A[i,:])/np.sum(A) for i in range(A.shape[0]) for j in range(A.shape[1])]).reshape(A.shape[0],A.shape[1])
(B==B1).all() #返回的是true
x22=np.sum((A-B)**2/B)
(x2==x22).all()  #返回的也是true
'''参考答案'''
B = A.sum(0)*A.sum(1).reshape(-1, 1)/A.sum()
x222 = ((A-B)**2/B).sum()
'''对比差距
我的写法中还是使用了列表解析，但其实对于矩阵的特定维度求和，没这个必要，需要改进
A.sum(0) 维度是(5,)
A.sum(1).reshape(-1, 1)  维度是(8,1)
那么按照广播，A.sum(0) 维度会从(5,)变成(1,5)再广播成(8,5)
             A.sum(1).reshape(-1, 1)从(8,1)广播成(8,5)
             然后它们之间逐元素乘积即可

'''

#习题4，改进矩阵计算效率
np.random.seed(0)
m, n, p = 100, 80, 50   #设置三个维度
#下面的三个矩阵其实都是0/1稀疏矩阵
B = np.random.randint(0, 2, (m, p))
U = np.random.randint(0, 2, (p, n))
Z = np.random.randint(0, 2, (m, n))
def solution(B=B, U=U, Z=Z):
    L_res = []
    for i in range(m):  #计算R的两层循环
        for j in range(n):
            norm_value = ((B[i]-U[:,j])**2).sum()  #计算向量的2范数
            L_res.append(norm_value*Z[i][j])   #2范数再乘上Zij
    print(len(L_res))  #输出的就是m*n=8000
    return sum(L_res)
solution(B, U, Z)  #100566

'''我的写法'''
%timeit -n 30 sum([sum((B[i,:]-U[:,j])**2)*Z[i,j] for i in range(m) for j in range(n)]).astype('int32') #100566
# 95.5 ms ± 6.81 ms per loop (mean ± std. dev. of 7 runs, 30 loops each)
'''参考答案
在计算效率上比较好，但是不是很好理解
'''
%timeit -n 30 (((B**2).sum(1).reshape(-1,1) + (U**2).sum(0) - 2*B@U)*Z).sum()
# 467 µs ± 30.6 µs per loop (mean ± std. dev. of 7 runs, 30 loops each)


#习题5，连续整数的最大长度
#考虑使用 nonzero, diff 函数，其实diff比较好理解，如果是连续整数的话必然得到1，但是nonzero有什么用？
a=[1,2,5,6,7]  #应该输出的是3
b=[3,2,1,2,3,4,6]   #应该输出的是4

'''我的写法'''
def continuou_len(lis):
    '''返回输入的数组lis的连续整数最大长度'''
    lis=np.array(lis)  
    lis_diff=np.diff(lis)  #连续出现的1的数目+1 就是所求
    lis_diff=(lis_diff==1)
    count=0         #一旦出现false，就立马将count变成0
    count_max=0   #用来计算连续的1的数目
    for i in range(len(lis_diff)):
        if lis_diff[i]==True:
            count+=1
            if count>count_max:
                count_max=count
        else:
            count=0
    return count_max+1
continuou_len(a) #输出的是3
continuou_len(b) #输出的是4
#但是很明显上面的流程很麻烦

'''参考答案'''
f = lambda x:np.diff(np.nonzero(np.r_[1,np.diff(x)!=1,1])).max()
f(a)
f(b)
'''答案解析
x=a
np.diff(x)  array([1, 3, 1, 1])
np.diff(x)!=1  array([False,  True, False, False])
np.r_[1,np.diff(x)!=1,1]  加上左右的1之后，变成array([1, 0, 1, 0, 0, 1], dtype=int32)
np.nonzero(np.r_[1,np.diff(x)!=1,1]) 找到非0的位置 (array([0, 2, 5], dtype=int64),)
np.diff(np.nonzero(np.r_[1,np.diff(x)!=1,1]))    array([[2, 3]], dtype=int64)
'''

























