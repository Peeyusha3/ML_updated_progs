import numpy as np
from scipy.spatial import distance

#we initialize Malware Samples
B_malware = np.array([[1.0, -2.0, 1.0, 2.0],
          [-1.0, 2.0, 3.0, 3.0],
          [1.0, 2.0, 0.0, 1.0],
          [-1.0, -1.0, 1.0, 1.0],
          [-1.0, -2.0, 3.0, -2.0],
          [1.0, 2.0, 1.0, 0.0]])


#we initialize Benign Samples
B_benign = np.array([[-1.0, -2.0, -1.0, 0.0],
          [2.0, 1.0, 3.0, 2.0],
          [1.0, 2.0, 0.0,3.0],
          [2.0, 3.0, 1.0, 1.0],
          [-1.0, 2.0, 3.0, 1.0],
          [0.0, 1.0, -1.0, -2.0]])

#samples to score and classify
Y1 = np.array([1,5,1,5,5,1])
Y2 = np.array([-2,3,2,3,0,2])
Y3 = np.array([2,-3,2,3,0,0])
Y4 = np.array([2,-2,2,2,-1,1])

#we initialize A used after normalizing B
A_malware = np.array([[]], dtype = float)
A_benign = np.array([[]], dtype = float)

#mean for both the samples
mean_malware = np.zeros(shape = len(B_malware))
mean_benign = np.zeros(shape = len(B_benign))

#C used as covariance matrix
C_malware = np.array([[]], dtype = float)
C_benign = np.array([[]], dtype = float)

#delta for scoring
delta_malware = np.array([[]], dtype = float)
delta_benign = np.array([[]], dtype = float)

#eigenvectors
U_malware = np.array([[]], dtype = float)
U_benign = np.array([[]], dtype = float)

#weights
w_malware = np.array([[]], dtype = float)
w_benign = np.array([[]], dtype = float)

#normalize B
def normalizeB():
    sum_malware = 0
    for i in range (0,len(B_malware)):
        for j in range (0,len(B_malware[i])):
            sum_malware = sum_malware + B_malware[i][j] 
        mean_malware[i] = sum_malware / len(B_malware[i])
        sum_malware= 0
    
    sum_benign = 0
    for i in range (0,len(B_benign)):
        for j in range (0,len(B_benign[i])):
            sum_benign = sum_benign + B_benign[i][j] 
        mean_benign[i] = sum_benign / len(B_benign[i])
        sum_benign = 0

#used to initialize matrix A from B
def computeA():
    global A_malware, A_benign
    A_malware = B_malware
    for i in range (0,len(A_malware)):
        for j in range (0,len(A_malware[i])):
            A_malware[i][j] -= mean_malware[i]
    
    A_benign = B_benign
    for i in range (0,len(A_benign)):
        for j in range (0,len(A_benign[i])):
            A_benign[i][j] -= mean_benign[i]


#used to get covariance matrix C   
def compute_covarianceM():
    global C_malware, C_benign
    C_malware = 0.25*A_malware.dot(A_malware.T)
    C_benign = 0.25*A_benign.dot(A_benign.T)
    
#used to get s = eigenvalues and U = eigenvectors
def computeEValues_EVector():
    global U_malware, U_benign
    s_malware, U_malware = np.linalg.eig(C_malware)
    s_benign, U_benign = np.linalg.eig(C_benign)
    np.set_printoptions(formatter={'float_kind': '{:.3f}'.format},suppress = True)
    #re-initialize with values in question
    U_malware = np.array([[0.1641,0.2443],
               [0.6278,0.1070],
               [-0.2604,-0.8017],
               [-0.5389,0.4277],
               [0.4637,-0.1373],
               [0.0752,-0.2904]])
    U_benign = np.array([[0.1641,0.2443],
               [0.6278,0.1070],
               [-0.2604,-0.8017],
               [-0.5389,0.4277],
               [0.4637,-0.1373],
               [0.0752,-0.2904]])
    print("Eigen Values of Malware:")
    print(s_malware)
    print("Eigen Vectors of Malware:")
    print(U_malware)
    print("Eigen Values of Benign:")
    print(s_benign)
    print("Eigen Vectors of Benign:")
    print(U_benign)
    
    

#used to get delta = scoring matrix 
def compute_scoringMatrix():
    global delta_malware, delta_benign
    delta_malware = (U_malware.T).dot(A_malware)
    delta_benign = (U_benign.T).dot(A_benign)
    print("Scoring Matrix of Malware:")
    print(delta_malware)
    print("Scoring Matrix of Benign:")
    print(delta_benign)
    
#used to get weightmatrices and score the sample vectors
def calculate_weightMatrices():
    
    global w_benign,w_malware
    
    #eigenvectors in question
    U1_malware = U_malware[0:6,0:1]
    U2_malware = U_malware[0:6,1:2]
    U1_benign = U_benign[0:6,0:1]
    U2_benign = U_benign[0:6,1:2]
    
    YBar = Y1-mean_malware
    w_malware = np.array([(YBar.T).dot(U1_malware),(YBar.T).dot(U2_malware)])
    result_malware = EuclideanDistMalware()
    
    YBar = Y1-mean_benign
    w_benign = np.array([(YBar.T).dot(U1_benign),(YBar.T).dot(U2_benign)])
    result_benign = EuclideanDistBenign()
    
    classify_sample("Y1",result_malware,result_benign)
    
    YBar = Y2-mean_malware
    w_malware = np.array([(YBar.T).dot(U1_malware),(YBar.T).dot(U2_malware)])
    result_malware = EuclideanDistMalware()
    
    YBar = Y2-mean_benign
    w_benign = np.array([(YBar.T).dot(U1_benign),(YBar.T).dot(U2_benign)])
    result_benign = EuclideanDistBenign()
    
    classify_sample("Y2",result_malware,result_benign)

    YBar = Y3-mean_malware
    w_malware = np.array([(YBar.T).dot(U1_malware),(YBar.T).dot(U2_malware)])
    result_malware = EuclideanDistMalware()
    
    YBar = Y3-mean_benign
    w_benign = np.array([(YBar.T).dot(U1_benign),(YBar.T).dot(U2_benign)])
    result_benign = EuclideanDistBenign()
    
    classify_sample("Y3",result_malware,result_benign)

    YBar = Y4-mean_malware
    w_malware = np.array([(YBar.T).dot(U1_malware),(YBar.T).dot(U2_malware)])
    result_malware = EuclideanDistMalware()
    
    YBar = Y4-mean_benign
    w_benign = np.array([(YBar.T).dot(U1_benign),(YBar.T).dot(U2_benign)])
    result_benign = EuclideanDistBenign()
    
    classify_sample("Y4",result_malware,result_benign)

#calculate distance from malware
def EuclideanDistMalware():
    low = float('inf')
    for i in range(0, 4):
        dist = distance.euclidean(w_malware, delta_malware[:, i: i + 1])
        if dist < low:
            low = dist
    return low

#calculate distance from benign
def EuclideanDistBenign():
    low = float('inf')
    for i in range(0, 4):
        dist = distance.euclidean(w_benign, delta_benign[:, i: i + 1])
        if dist < low:
            low = dist
    return low

#classify based on the score
def classify_sample(sample,malware_score,benign_score):
    if malware_score > benign_score:
        print(sample," is Benign")
    else:
        print(sample," is Malware")

if __name__ == "__main__":   
    normalizeB()
    computeA()
    compute_covarianceM()
    computeEValues_EVector()
    compute_scoringMatrix()
    calculate_weightMatrices()
