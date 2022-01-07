from math import gamma
from numpy import poly
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

#running for i from 1 to 4 and j from 2 to 5
best_res=0
for i in range(1,5):
    for j in range(2,6):
        data = pd.read_csv("C:/Users/peeyu/OneDrive/Desktop/malben3.csv")
        #print(data.head(5))
        X = data.iloc[:, [1,2,3]].values
        y = data.iloc[:, 4].values
        #print(X[:5])
        X_train,X_test,Y_train,Y_test = train_test_split(X,y, test_size=0.5, shuffle=False)
        #print(X_train[-5:])

        #train the svm model
        model = SVC(C=i, kernel='rbf', gamma=j)
        model.fit(X_train,Y_train)

        #prediction using the model
        y_pred = model.predict(X_test)

        con = confusion_matrix(Y_test,y_pred)
        #print(con)

        score = con[0][0]+con[1][1]
        score = (score/len(Y_test)) *100
        print("For C =",i,"and p = ",j,":")
        print("Accuracy: ",score,"%")
        #print(score)
        best_res = score if score>best_res else best_res
print("Best result is:", best_res,"%")