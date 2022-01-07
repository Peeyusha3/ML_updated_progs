#import libraries 
import numpy as np
from scipy.spatial import distance

#we initialize the matrices malware samples m1,m2,m3 and m4 to Y1, Y2, Y3 and Y4 respectively
Y1 = np.array([[1],[-1],[1],[-1],[-1],[1]])
Y2 = np.array([[-2],[2],[2],[-1],[-2],[2]])
Y3 = np.array([[1],[3],[0],[1],[3],[1]])
Y4 = np.array([[2],[3],[1],[1],[-2],[0]])

#we initialize mean, delta as scoring matrix from the question
mean = np.array([[7/4],[7/4],[5/4],[2],[2],[1]])
delta = np.array([[-1.1069, 1.2794, -2.6800, 2.5076],
                  [1.5480, 0.5484, -1.2085, -0.8879]])
w = np.array([[]], dtype = float)

#used to get delta = scoring matrix 
def compute_scoringMatrix():
    global delta
    print("Scoring matrix delta:")
    print(delta)

#used to get weightmatrices and score the sample vectors
def calculate_weightMatrices():
    
    #choosing eigenvectors based on eigenvalues, here from the question 
    global w
    U1 = np.array([[0.1641],
               [0.6278],
               [-0.2604],
               [-0.5389],
               [0.4637],
               [0.0752]])
    U2 = np.array([[0.2443],
               [0.1070],
               [-0.8017],
               [0.4277],
               [-0.1373],
               [-0.2904]])
    print("Minimum Values of Y1, Y2, Y3 and Y4 are:")
    
    YBar = Y1-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2)])
    print("{0:.2f}".format(EuclideanDist()))
    
    YBar = Y2-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2)])
    print("{0:.2f}".format(EuclideanDist()))
    
    YBar = Y3-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2)])
    print("{0:.2f}".format(EuclideanDist()))
    
    YBar = Y4-mean
    w = np.array([(YBar.T).dot(U1),(YBar.T).dot(U2)])
    print("{0:.2f}".format(EuclideanDist()))
    
#used to get euclidean distance
def EuclideanDist():
    low = float('inf')
    for i in range(0, 4):
        dist = distance.euclidean(w, delta[:, i: i + 1])
        if dist < low:
            low = dist
    return low
    
if __name__ == "__main__":   
    compute_scoringMatrix()
    calculate_weightMatrices()