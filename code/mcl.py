#coding=utf-8

#MCL算法
#adjacencyMat 邻接矩阵
#inflation 膨胀系数
#numIter 迭代次数
#power 扩张系数

import numpy as np

def markovCluster(adjacencyMat, numIter, power = 2, inflation =3):
    
    #邻接矩阵归一化
    columnSum = np.sum(adjacencyMat, axis = 0)
    probabilityMat = adjacencyMat / columnSum
    
    #扩张矩阵
    def _expand(probabilityMat, power):
        expandMat = probabilityMat
        for i in range(power - 1):
            expandMat = np.dot(expandMat, probabilityMat)
        return expandMat
    expandMat = _expand(probabilityMat, power)
    
    #膨胀矩阵 见公式
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
    #聚类分析
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
    print 'number_of_group: ',len(ls)
    print 'group_list: ',ls
    print len(ls[0])
    
if __name__ == "__main__":
    numIter = 50
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
    adjacencyMat = np.loadtxt('D:/java-book/PYTHONtest/src/Demo/101/juzhen')
    markovCluster(adjacencyMat, numIter)
