import numpy as np
import math

X = [[3.6, 79],
    [1.8, 54],
    [2.283, 62],
    [3.333, 74],
    [2.883, 55],
    [4.533, 85],
    [1.950, 51],
    [1.833, 54],
    [4.7, 88],
    [3.6, 85],
    [1.600, 52],
    [4.350, 85],
    [3.917, 84],
    [4.2, 78],
    [1.750, 62],
    [1.8, 51],
    [4.7, 83],
    [2.167, 52],
    [4.800, 84],
    [1.750, 47]]

mew_1 = [2.5, 68.0]
S_1 = [[1.0, 5.0],
      [5.0, 103.0]]
mew_2 = [3.5, 70.0]
S_2 = [[2.0, 10.0],
      [10.0, 200.0]]
tow_1 = 0.6
tow_2 = 0.4
p_1 = []
p_2 = []
iterations = 0

def Clusters():
    global X,mew_1,S_1,S_2,tow_1,tow_2,iterations,p_1,p_2,mew_2
    while iterations < 100:
        inter_tow_1 = 0.0
        inter_tow_2 = 0.0
        inter_mew_1 = 0.0
        inter_mew_2 = 0.0
        inter_S_1 = [[0.0, 0.0],[0.0, 0.0]]
        inter_S_2 = [[0.0, 0.0],[0.0, 0.0]]
        
        det_S_1 = np.linalg.det(S_1)
        det_S_2 = np.linalg.det(S_2)
    
        inv_S_1 = np.linalg.inv(S_1)
        inv_S_2 = np.linalg.inv(S_2)
        
        for i in range(len(X)):
            inter_p_1 = tow_1 * ((1 / (2 * math.pi * math.sqrt(det_S_1))) * 
            (math.e ** (-0.5 * np.dot(np.dot(np.subtract(X[i], mew_1), inv_S_1), np.transpose(np.subtract(X[i], mew_1))))))
            inter_p_2 = tow_2 * ((1 / (2 * math.pi * math.sqrt(det_S_2))) * 
            (math.e ** (-0.5 * np.dot(np.dot(np.subtract(X[i], mew_2), inv_S_2), np.transpose(np.subtract(X[i], mew_2))))))
    
            p_1.append(inter_p_1 / (inter_p_1 + inter_p_2))
            p_2.append(inter_p_2 / (inter_p_1 + inter_p_2))
            inter_tow_1 += p_1[i]
            inter_tow_2 += p_2[i]
            inter_mew_1 += np.dot(p_1[i], X[i])
            inter_mew_2 += np.dot(p_2[i], X[i])
    
        tow_1 = inter_tow_1 / len(X)
        tow_2 = inter_tow_2 / len(X)
        mew_1 = np.divide(inter_mew_1, inter_tow_1)
        mew_2 = np.divide(inter_mew_2, inter_tow_2)
        
        for i in range(len(X)):
            inter_S_1 = np.add(inter_S_1, np.dot(np.dot(p_1[i], np.atleast_2d(np.subtract(X[i], mew_1)).T),np.atleast_2d(np.subtract(X[i], mew_1))))
            inter_S_2 = np.add(inter_S_2, np.dot(np.dot(p_2[i], np.atleast_2d(np.subtract(X[i], mew_2)).T),np.atleast_2d(np.subtract(X[i], mew_2))))
    
        S_1 = np.divide(inter_S_1, inter_tow_1)
        S_2 = np.divide(inter_S_2, inter_tow_2)
        p_1.clear()
        p_2.clear()
        iterations += 1
    
    print("Cluster related values are:\n")
    print("Tow-1:",tow_1)
    print("Tow-2:",tow_2,"\n")
    print("Mew-1:\n",np.atleast_2d(mew_1).T,"\n")
    print("Mew-2:\n",np.atleast_2d(mew_2).T,"\n")
    print("S-1")
    print(S_1,"\n")
    print("S-2")
    print(S_2,"\n")
    
Clusters()