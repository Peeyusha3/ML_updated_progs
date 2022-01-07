import numpy as np
import random as rd
import matplotlib.pyplot as plt

K = 3
X = np.array([[3.6,79],[1.8,54],[2.283,62],[3.333, 74],[2.883,55],[4.533,85],[1.95,51],[1.833,54],[4.700,88],[3.6,85],[1.6,52],[4.35,85],[3.917,84],[4.2,78],[1.75,62],[1.8,51],[4.7,83],[2.167,52],[4.8,84],[1.75,47]])


m=X.shape[0]
n=X.shape[1]


cent=np.array([]).reshape(n,0)


for i in range(K):
    rand=rd.randint(0,m-1)
    cent=np.c_[cent,X[rand]]


Output={}

dist=np.array([]).reshape(m,0)
for k in range(K):
        d=np.sum((X-cent[:,k])**2,axis=1)
        dist=np.c_[dist,d]
C=np.argmin(dist,axis=1)+1


dict1={}
for i in range(K):
    dict1[i+1]=np.array([]).reshape(2,0)
for i in range(m):
    dict1[C[i]]=np.c_[dict1[C[i]],X[i]]
     
for i in range(K):
    dict1[i+1]=dict1[i+1].T
   
for i in range(K):
      cent[:,i]=np.mean(dict1[i+1],axis=0)
     
for i in range(200):

      dist=np.array([]).reshape(m,0)
      for k in range(K):
          tempDist=np.sum((X-cent[:,k])**2,axis=1)
          dist=np.c_[dist,tempDist]
      C=np.argmin(dist,axis=1)+1

      dict1={}
      for k in range(K):
          dict1[k+1]=np.array([]).reshape(2,0)
      for i in range(m):
          dict1[C[i]]=np.c_[dict1[C[i]],X[i]]
     
      for k in range(K):
          dict1[k+1]=dict1[k+1].T
   
      for k in range(K):
          cent[:,k]=np.mean(dict1[k+1],axis=0)
 
     
print(cent,"\n")
print(dict1,"\n")
     

color=['pink',"lightblue",'lightgreen']
labels=['Cluster-1','Cluster-2','Cluster-3']
for k in range(K):
    plt.scatter(dict1[k+1][:,0],dict1[k+1][:,1],c=color[k],label=labels[k])
plt.scatter(cent[0,:],cent[1,:],s=75,c='black',label='Centroids')
plt.xlabel('Duration')
plt.ylabel('Wait')
plt.legend()
plt.show()