#import libraries 
import numpy as np
from scipy.spatial import distance

#we initialize the B matrix using set of vectors B1, B2, B3, B4
B = np.array([[-1.0, -2.0, -1.0, 0.0],
          [2.0, 1.0, 3.0, 2.0],
          [1.0, 2.0, 0.0, 3.0],
          [2.0, 3.0, 1.0, 1.0],
          [-1.0, 2.0, 3.0, 1.0],
          [0.0, 1.0, -1.0, -2.0]])

#we initialize A used after normalizing B, C used as covariance matrix and delta as scoring matrix
A = np.array([[]], dtype = float)
mean = np.zeros(len(B))
C = np.array([[]], dtype = float)
delta = np.array([[]], dtype = float)
w = np.array([[]], dtype = float)

#used to normalize B using mean of each row 
def normalizeB():
    sum = 0
    for i in range (0,len(B)):
        for j in range (0,len(B[i])):
            sum = sum + B[i][j] 
        mean[i] = sum / len(B[i])
        sum = 0
        
#used to initialize matrix A from B
def computeA():
    global A
    A = B
    for i in range (0,len(A)):
        for j in range (0,len(A[i])):
            A[i][j] -= mean[i]
    
#used to get covariance matrix C 
def compute_covarianceM():
    global C
    C = 0.25*A.dot(A.T)
    print("Co-variance Matrix:")
    np.set_printoptions(formatter={'float_kind': '{:.2f}'.format})
    print(C)
    
#used to get s = eigenvalues and U = eigenvectors
def computeEValues_EVector():
    global U
    s, U = np.linalg.eig(C)
    np.set_printoptions(precision = 5,formatter={'float_kind': '{:.5f}'.format},suppress = True)
    print("Eigen Values:")
    print(s)
    print("Eigen Vectors:")
    U = np.array([[0.1641,0.2443],
               [0.6278,0.1070],
               [-0.2604,-0.8017],
               [-0.5389,0.4277],
               [0.4637,-0.1373],
               [0.0752,-0.2904]])
    print(U)

#used to get delta = scoring matrix and formatting to only large values based on eigenvalues
def compute_scoringMatrix():
    global delta
    delta = (U.T).dot(A)
    #print(delta)
    delta = delta[~np.all(delta<0.001, axis=1)]
    print("Scoring matrix delta:")
    print(delta)

if __name__ == "__main__":   
    normalizeB()
    computeA()
    compute_covarianceM()
    computeEValues_EVector()
    compute_scoringMatrix()
    