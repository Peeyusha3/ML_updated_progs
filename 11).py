import numpy as np
import math

X= np.array(([3.6, 79],[1.8,54],[2.283,62],[3.333,74],[2.883,55],[4.533,85],[1.950,51],[1.833,54],[4.700,88],[3.600,85],[1.600,52],[4.350,85],[3.917,84],[4.2,78],[1.75,62],[1.8,51],[4.7,83],[2.167,52],[4.8,84],[1.75,47])).astype(float)
T = np.array([0.5704, 0.4296]).astype(float)
u= np.array(([2.6269, 63.0160],[3.6756, 75.1981])).astype(float)
s= np.array(([[1.0548, 12.7306],[12.7306,181.5138]],[[1.2119, 14.1108],[14.1108,189.2046]])).astype(float)
u_new= np.empty(shape = (2,2))
s1_new= np.empty(shape = (2,2))
s2_new= np.empty(shape = (2,2))
p = np.zeros(shape=(2,20))

def func(X,u,s):
    t1 = 1/(2*3.14*math.sqrt(np.linalg.det(s)))
    t2 = np.exp(-0.5 * (np.matmul(np.transpose(np.subtract(X,u)), (np.matmul(np.linalg.inv(s) ,np.subtract(X,u))))))
    #print (t1*t2)
    return t1*t2

for i in range(20):
    for j in range(2):
        p[j][i] = (T[j] * func(X[i],u[j],s[j]))/((T[0]* func(X[i],u[0],s[0])) + (T[1]* func(X[i],u[1],s[1])))

for i in range(20):
    for j in range(2):        
        print (f"p{j+1},{i+1}: {p[j][i]:.4f}")
       
for j in range(2):
    sum1=0
    sum2=0
    for i in range(20):
        sum1 += p[j][i]*X[i]
        sum2 += p[j][i]
        u_new[j] = np.divide(sum1 , sum2)
       
print (f"u1 : {u_new[0]}")
print (f"u2 : {u_new[1]}")

for j in range(2):
    sum1=0
    sum2=0
    for i in range(20):
        t1 = np.transpose(np.asmatrix(np.subtract(X[i], u_new[j])))
       
        t2= (np.asmatrix(np.subtract(X[i],u_new[j])))
     
        sum1 += p[j][i] * (np.matmul(t1,t2))
        sum2 += p[j][i]  
    res= np.divide(sum1, sum2)
    print(f"S{j+1}: ")
    print(res)