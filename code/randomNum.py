#coding=utf-8

import numpy as np
import random

#获得随机数
def getrand(number,group=1):
    if number*group-int(number*group)==0: 
        result=int(number*group)
    else: 
        result=int(number*group)+1 
    #num1 = [1]*result
    num1=[random.uniform(1,10) for i in range(result)]
    num0 = [random.random() for i in range(number-result)]
    num1.extend(num0)
    random.shuffle(num1)
    return num1

#groupin 组内紧密程度  
#groupout 组间紧密程度
groupin = 0.5
groupout = 0.01
list1 = [70,120,200,300]
j=0
alln = list1[-1]
#产生对角线为 1 的矩阵
getmat = np.diag([2]*alln)
#getmat = np.eye(alln)
#将随机数赋值给矩阵
for i in list1:
    lsmat = np.eye(i-j)
    num1 = getrand((i-j)*(i-j-1)/2,groupin)
    lsmat[np.triu_indices(i-j, 1)] = num1
    lsmat[np.tril_indices(i-j, -1)] = num1
    getmat[j:i,j:i] = lsmat
    quar = getrand((i-j)*(alln-i),groupout)
    quar = np.array(quar).reshape(i-j,alln-i)
    getmat[j:i,i:alln] = quar
    j=i
getmat[np.triu_indices(alln, 1)[1],np.triu_indices(alln, 1)[0]] = getmat[np.triu_indices(alln, 1)]

#获得节点形式的矩阵
value = list(getmat[np.triu_indices(alln,1)])
x = list(np.triu_indices(alln,1)[0])
y = list(np.triu_indices(alln,1)[1])
f=open('node','w')
for (a,b,c) in zip(x,y,value):
    if c>=1:
        f.write(str(a+1)+'\t'+str(b+1)+'\t'+str(c)+'\n')
#矩阵写入文件
np.savetxt('juzhen', getmat, delimiter='\t',fmt='%.5f')
print 'Have finished!'
