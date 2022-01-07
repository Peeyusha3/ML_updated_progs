#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt

lambda_new = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
lambda_old = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
epi = 0.00001
X = np.array([[3,3],[3,4],[2,3],[1,1],[1,3],[2,2]])
bias = 0
b = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
C = 2.5
z = np.array([1,1,1,-1,-1,-1])
F = np.array([0.0,0.0,0.0,0.0,0.0,0.0])
E = np.array([0.0,0.0,0.0,0.0,0.0,0.0])

#to use random i,j pairs
list_of_pairs = [[]]

while(len(list_of_pairs)<1000):
    for i in range(6):
        j = i
        while i == j:
            j = random.randrange(0,6)

        pair = []
        pair.insert(0,i)
        pair.insert(1,j)
        list_of_pairs.append(pair)

list_of_pairs = list_of_pairs[2:]
list_of_pairs = list_of_pairs[:1000]

#run from 1 to n of choice
for passes in range(0,10):
    for pair in range(0,len(list_of_pairs)):
        i = list_of_pairs[pair][0]
        j = list_of_pairs[pair][1]
        d = 2.0*(np.dot(X[i],X[j])) - np.dot(X[i],X[i]) - np.dot(X[j],X[j])
        if(i!=j):

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
                lambda_new[j] = lambda_new[j]-(z[j]*(E[i]-E[j]))/d

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
                b[i] = bias - E[i] - z[i]*(lambda_new[i] - lambda_old[i])*(np.dot(X[i],X[i])) - z[j]*(lambda_new[j] - lambda_old[j])*(np.dot(X[i],X[j]))
                b[j] = bias - E[j] - z[i]*(lambda_new[i] - lambda_old[i])*(np.dot(X[i],X[j])) - z[j]*(lambda_new[j] - lambda_old[j])*(np.dot(X[j],X[j]))

                if lambda_new[i] > 0 and lambda_new[i]<C:
                    bias = b[i]
                elif lambda_new[j] > 0 and lambda_new[j]<C:
                    bias = b[j]
                else:
                    bias = (b[i]+b[j])/2


    if(np.equal(lambda_new, lambda_old).all()):
        print(lambda_new)
        print(lambda_old)
        print("Both Lambdas are equal at Pass:",passes)
        break

np.set_printoptions(precision=3)
print("Old Lambdas",lambda_old)
print("new Lambdas:",lambda_new)
print("b:",bias)

def W(lambda_new, Z, X):
    temp = 0.0
    for i in range(len(X)):
        temp += lambda_new[i]*Z[i]*X[i]
    return temp

W = W(lambda_new, z, X)
print(W)

color = ['red' if c == -1. else 'blue' for c in z]
plt.scatter(X[:, 0], X[:, 1], c=color)

# Create the hyperplane
a = -W[0] / W[1]
xx = np.linspace(0, 4)
yy = a * xx - (bias) / W[1]

plt.plot(xx, yy)
plt.axis("on"), plt.show()


