from math import gamma
from operator import index
import numpy as np
from numpy import poly,abs,delete,min
from numpy.lib.function_base import delete
import pandas as pd
from pandas.tseries.offsets import Week
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

indexes=[1,2,3]
data = pd.read_csv("C:/Users/peeyu/OneDrive/Desktop/malben3.csv")
#print(data.head(5))
for i in range (1,4):

    X = data.iloc[:, indexes].values
    y = data.iloc[:, 4].values
    #print(X[:5])
    X_train,X_test,Y_train,Y_test = train_test_split(X,y, test_size=0.5, shuffle=False)
    #print(X_train[-5:])

    model = SVC(C=1, kernel='linear')
    model.fit(X_train,Y_train)

    y_pred = model.predict(X_test)

    con = confusion_matrix(Y_test,y_pred)
            #print(con)

    score = con[0][0]+con[1][1]
    score = (score/len(Y_test)) *100
    weights = model.coef_
    #weights=abs(weights)
    print("Weights:")
    print(weights)

            #print("For C =",i,"and p = ",j,":")
    print("Accuracy: ",score,"%")
    #print(type(weights))
    #print(min(weights))

    #we take the absolute of weights and remove the lowest and re-run for all the features
    weights = np.abs(weights)
    minimumIndex = np.argwhere(weights == np.min(weights))
    #print(minimumIndex)
    print("Recursive Feature elimination, dropping feature:",minimumIndex[0][1])
    indexes.pop(minimumIndex[0][1])

            