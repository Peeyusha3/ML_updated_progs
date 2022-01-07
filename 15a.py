#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

lambda_new = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
lambda_old = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
epi = 0.00001
#taking lambda as rows given in question
lArray = [[0,1],[1,2],[2,3],[3,4],[4,5],[0,2],[1,3],[2,4],[3,5],[0,3],[1,4],[2,5],[0,4],[1,5],[0,5],
          [1,0],[2,1],[3,2],[4,3],[5,4],[2,0],[3,1],[4,2],[5,3],[3,0],[4,1],[5,2],[4,0],[5,1],[5,0]]

X = np.array([[3,3],[3,4],[2,3],[1,1],[1,3],[2,2]])
bias = 0
b = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
C = 2.5
z = np.array([1,1,1,-1,-1,-1])
F = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
E = np.array([0.0,0.0,0.0,0.0,0.0,0.0])

#SSMO
for passes in range(10):
    for pair in range(0,len(lArray)):
        i = lArray[pair][0]
        j = lArray[pair][1]
        if(i!=j):
            d = 2.0*(np.dot(X[i],X[j])) - np.dot(X[i],X[i]) - np.dot(X[j],X[j])

            if(abs(d)>epi):

                F[i] = 0
                for k in range(len(X)):
                    F[i] += lambda_new[k]*z[k]*(np.dot(X[k],X[i]))
                F[i] += bias


                F[j] = 0
                for k in range(len(X)):
                    F[j] += lambda_new[k]*z[k]*(np.dot(X[k],X[j]))
                F[j] += bias

                E[i],E[j] = F[i]-z[i],F[j]-z[j]
                lambda_old[i],lambda_old[j] = lambda_new[i], lambda_new[j]
                lambda_new[j] = lambda_new[j]-((z[j]*(E[i]-E[j]))/d)

                if z[i] == z[j]:
                    l = max(0, lambda_new[i]+lambda_new[j]-C)
                    h = min(C,lambda_new[i]+lambda_new[j])
                else:
                    l = max(0,lambda_new[j]-lambda_new[i])
                    h = min(C,C+lambda_new[j]-lambda_new[i])

                if lambda_new[j]>h:
                    lambda_new[j] = h
                elif lambda_new[j]>=l and lambda_new[j] <=h:
                    lambda_new[j] = lambda_new[j]
                elif lambda_new[j]<l:
                    lambda_new[j] = l

                lambda_new[i] += z[i]*z[j]*(lambda_old[j] - lambda_new[j])
                b[i] = bias - E[i] - (z[i]*(lambda_new[i] - lambda_old[i])*(np.dot(X[i],X[i]))) - (z[j]*(lambda_new[j] - lambda_old[j])*(np.dot(X[i],X[j])))
                b[j] = bias - E[j] - (z[i]*(lambda_new[i] - lambda_old[i])*(np.dot(X[i],X[j]))) - (z[j]*(lambda_new[j] - lambda_old[j])*(np.dot(X[j],X[j])))

                if lambda_new[i] > 0 and lambda_new[i]<C:
                    bias = b[i]
                elif lambda_new[j] > 0 and lambda_new[j]<C:
                    bias = b[j]
                else:
                    bias = (b[i]+b[j])/2


    if(np.equal(lambda_new, lambda_old).all()):
        print("Lambda is not changing after Pass:",passes)
        break

print("Old Lambda",lambda_old)
print("New Lambda:",lambda_new)
print("b:",bias)
print("f(x) and z:")
for i in range(len(X)):
    print(F[i],z[i])

def W(lambda_new, Z, X):
    temp = 0.0
    for i in range(len(X)):
        temp += lambda_new[i]*Z[i]*X[i]
    return temp

W = W(lambda_new, z, X)
print("weights:")
print(W)
print("support vectors are :")
print(X[2],X[4],X[5])

color = ['red' if c == -1. else 'blue' for c in z]
plt.scatter(X[:, 0], X[:, 1], c=color)

# Create the hyperplane
a = -W[0] / W[1]
xx = np.linspace(0, 4)
yy = a * xx - (bias) / W[1]

plt.plot(xx, yy)
plt.axis("on"), plt.show()
