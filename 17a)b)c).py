#import libraries 
import numpy as np
import math

#initilaize lambda from question
Lambda_1 = 4.0833
Lambda_2 = 1.2364
Lambda_3 = 0.7428

#initialize eigenvectors from question
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

U3 = np.array([[-0.0710],
               [0.2934],
               [0.3952],
               [0.3439],
               [0.3644],
               [-0.7083]])

#greatest effect on U1
print ("The feature With greatest effect with Positive Correlation On U1 is:")
print (max(U1))
print ("The feature With greatest effect With Negative Correlation On U1 is:")
print (min(U1))
print ("The feature with greatest effect on U1 overall is: ")
print(max(abs(max(U1)), abs(min(U1))))

#Compute Component Loading Vector sqrt(lambda_i)*eigenvector_i
CLV_1 = math.sqrt(Lambda_1)* U1
print("The CLV of U1:")
print (CLV_1)
CLV_2 = math.sqrt(Lambda_2) * U2
print("The CLV of U2:")
print (CLV_2)
CLV_3 = math.sqrt(Lambda_3) * U3
print("The CLV of U3:")
print (CLV_3)

#significant CLV of U1 and U2
significant_CLV = CLV_1 + CLV_2
print("Significant CLV:")
print(significant_CLV)

#used to sort the list with input features
def sort_list(rank_list):
    return sorted(rank_list, key=abs)

#compute the rank list with weights
def compute_Rank_list(significant_CLV):
    feature_list = []
    feature_rank = {}
    order = 1
    rank = 1
    weight = 0
    for i in significant_CLV:
        feature_list.append(float(i[0]))
        feature_rank[float([i][0])] = [order, rank, weight]
        order = order + 1
    feature_list = sort_list(feature_list)
    rank = 6
    for i in feature_list:
        feature_rank[i][1] = rank
        rank = rank - 1
    for i in feature_rank:
        feature_rank[i][2] = (100 / 21) * (7 - feature_rank[i][1])
        print("Rank of", i,":", feature_rank[i][1],"      |     " "Relative Weight:", feature_rank[i][2])

print("The relative important features using Significant CLV Are:")
compute_Rank_list(significant_CLV)