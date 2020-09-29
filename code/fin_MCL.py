#coding=utf-8

#MCL�算法
#adjacencyMat 邻接矩阵
#inflation 膨胀系数
#numIter 迭代次数
#power 扩张系数
#导入包
import time
import random
import numpy as np
from collections import Counter
#随机数产生
begin = time.time()
fl = open('ALLresult4.txt','w')
fl.write('组内' + '\t' + '组间' + '\t' + 'r' +' \t' + 'P'+ '\t' + 'A' + '\t' + 'R'+'\n')
######################################################################
g=sorted([(i+1.0)/100 for i in range(50,100)],reverse=True)
loop = 0
for groupin in g:
    groupout=(1-groupin)
    loop += 1
    print 'loops',loop   
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
    #groupin = 0.9
    #groupout = 0.1
    #inflation = 2
    #fl.write(str(groupin)+'\t'+str(groupout)+'\t'+str(inflation)+'\t')
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
    #value = list(getmat[np.triu_indices(alln,1)])
    #x = list(np.triu_indices(alln,1)[0])
    #y = list(np.triu_indices(alln,1)[1])
    #f=open('node','w')
    #for (a,b,c) in zip(x,y,value):
    #    if c>=1:
    #        f.write(str(a+1)+'\t'+str(b+1)+'\t'+str(c)+'\n')
    #矩阵写入文件
    #print type(getmat)
    np.savetxt('juzhen', getmat, delimiter='\t',fmt='%.5f')
    print 'the ',loop,' randomnum have finished!'
    ######################################################################
    #MCL
    ######################################################################
    def markovCluster(adjacencyMat, numIter, power , inflation):
        #�ڽӾ����һ��
        columnSum = np.sum(adjacencyMat, axis = 0)
        probabilityMat = adjacencyMat / columnSum
        
        #���ž���
        def _expand(probabilityMat, power):
            expandMat = probabilityMat
            for i in range(power - 1):
                expandMat = np.dot(expandMat, probabilityMat)
            return expandMat
        expandMat = _expand(probabilityMat, power)
        
        #���;��� ����ʽ
        def _inflate(expandMat, inflation):
            powerMat = expandMat
            #for i in range(inflation - 1):
            powerMat = powerMat **inflation
            inflateColumnSum = np.sum(powerMat, axis = 0)
            inflateMat = powerMat / inflateColumnSum
            return inflateMat
        inflateMat = _inflate(expandMat, inflation)
        for i in range(numIter):
            expand = _expand(inflateMat, power)
            inflateMat = _inflate(expand, inflation)
        #print 'infalteMat ',inflateMat
        #�������
        def CLuster(inflateMat):
            list1 = []
            size = inflateMat.shape
            for i in range(int(size[0])):
                where = np.where(inflateMat[i,]==1)
                linshi = list(where[0])
                if linshi in list1 or linshi==[]:
                    pass
                else:
                    linshi = [j+1 for j in linshi]
                    list1.append(linshi)
            return list1
        
        ls =  CLuster(inflateMat)
        #print 'number_of_group: ',len(ls)
        #print 'group_list: ',ls
        #print len(ls[0])
        def evaluate(group_list):
            a=[1]*70
            a.extend([2]*50)
            a.extend([3]*80)
            a.extend([4]*100)
            a=np.array(a)
            for i in group_list:
                id = [id-1 for id in i]
                stat = Counter(a[id])
                sort_stat = sorted(stat.iteritems(),key=lambda d:d[1])
                pl = sort_stat.pop(0) 
                label = pl[0]           
                all = len(np.where(a==label)[0])
                TP = float(pl[1])
                FP = float(len(i) - TP) 
                FN = float(all - TP)
                TN = float(300.0 - TP -FP - FN)
                #print "TP:",TP,'FP',FP,'FN',FN,'TN',TN
                #print 'R',TP/(TP+FN),'P',TP/(TP+FP),'A',(TP+TN)/300
                fl.write(str(groupin)+'\t'+str(groupout)+'\t'+str(inflation)+'\t')
                fl.write(str(TP/(TP+FP))+'\t'+str((TP+TN)/300)+'\t'+str(TP/(TP+FN))+'\n')
                
        evaluate(ls)   
    for inflation in range(2,6):    
        if __name__ == "__main__":
            numIter = 30
            '''
            #例子
            adjacencyMat = np.array([[1, 2, 1, 3, 0, 0, 0],
                                     [2, 1, 4, 5, 0, 1, 0],
                                     [1, 4, 1, 6, 0, 0, 0],
                                     [3, 5, 6, 1, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 2, 4],
                                     [0, 1, 0, 0, 2, 1, 3],
                                     [0, 0, 0, 0, 4, 3, 1]],dtype='float')
            '''
            adjacencyMat = np.loadtxt('D:/java-book/PYTHONtest/src/Demo/juzhen')
            markovCluster(adjacencyMat, numIter,2,inflation)
        ########################################################################
    print 'the ',loop,' MCL have finished!'
fl.close()
end = time.time()
print 'Pass time :',end-begin,'(s)'