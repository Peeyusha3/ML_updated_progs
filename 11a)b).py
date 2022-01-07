#import libraries 
import numpy as np
from scipy.spatial import distance

#we initialize the B matrix using set of vectors X1, X2, X3, X4
B = np.array([[2.0, -2.0, -1.0, 3.0],
          [-1.0, 3.0, 3.0, -1.0],
          [0.0, 2.0, 3.0, 0.0],
          [1.0, 3.0, 1.0, 3.0],
          [1.0, 0.0, -1.0, 2.0],
          [-3.0, 2.0, 4.0, -1.0],
          [5.0, -1.0, 5.0, 3.0],
          [2.0, 1.0, 2.0, 0.0]])

#we initialize the matrices Y1, Y2, Y3 and Y4 to score them
Y1 = np.array([1,5,1,5,5,1,1,3])
Y2 = np.array([-2,3,2,3,0,2,-1,1])
Y3 = np.array([2,-3,2,3,0,0,2,-1])
Y4 = np.array([2,-2,2,2,-1,1,2,2])


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
    print("Matrix A:")
    print(A)
    
#used to get covariance matrix C 
def compute_covarianceM():
    global C
    C = 0.25*A.dot(A.T)
    print("Co-variance Matrix:")
    print(C)
    
#used to get s = eigenvalues and U = eigenvectors
def computeEValues_EVector():
    global U
    s, U = np.linalg.eig(C)
    np.set_printoptions(precision = 5,formatter={'float_kind': '{:f}'.format},suppress = True)
    print("Eigen Values:")
    print(s)
    print("Eigen Vectors:")
    print(U)

#used to get delta = scoring matrix and formatting to only large values based on eigenvalues
def compute_scoringMatrix():
    global delta
    delta = (U.T).dot(A)
    #print(delta)
    delta = delta[~np.all(delta<0.001, axis=1)]
    print("Scoring matrix delta:")
    print(delta)

#used to get weightmatrices and score the sample vectors
def calculate_weightMatrices():
    
    #choosing eigenvectors based on eigenvalues
    global w
    U1 = U[:,0:1]
    U2 = U[:,2:3]
    U3 = U[:,3:4]
    print("Minimum Values of Y1, Y2, Y3 and Y4 are:")
    
    YBar = Y1-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2),(YBar.T).dot(U3)])
    print("{0:.2f}".format(EuclideanDist()))
    
    YBar = Y2-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2),(YBar.T).dot(U3)])
    print("{0:.2f}".format(EuclideanDist()))
    
    YBar = Y3-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2),(YBar.T).dot(U3)])
    print("{0:.2f}".format(EuclideanDist()))
    
    YBar = Y4-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2),(YBar.T).dot(U3)])
    print("{0:.2f}".format(EuclideanDist()))
  
def EuclideanDist():
    low = float('inf')
    for i in range(0, 4):
        dist = distance.euclidean(w, delta[:, i: i + 1])
        if dist < low:
            low = dist
    return low
    
if __name__ == "__main__":   
    normalizeB()
    computeA()
    compute_covarianceM()
    computeEValues_EVector()
    compute_scoringMatrix()
    calculate_weightMatrices()

            
            

            
