from math import gamma
from numpy import poly
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix

#read the datafile
data = pd.read_csv("C:/Users/peeyu/OneDrive/Desktop/malben3.csv")
#print(data.head(5))

#extracting values to x and y
X = data.iloc[:, [1,2,3]].values
y = data.iloc[:, 4].values
#print(X[:5])
X_train,X_test,Y_train,Y_test = train_test_split(X,y, test_size=0.5, shuffle=False)
#print(X_train[-5:])

#train the svm model with kernel poly and C and p for 4 different values
model = SVC(C=3, kernel='poly',degree=4,gamma='auto')
model.fit(X_train,Y_train)

#predict using the model
y_pred = model.predict(X_test)

con = confusion_matrix(Y_test,y_pred)
#print(con)

#computing the accuracy 
score = con[0][0]+con[1][1]
score = (score/40) *100
print("For C = 3 and p = 4 :")
print("Accuracy: ",int(score),"%")
#print(score)