# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:08:59 2019

@author: Student
"""

import pandas as pd
from pandas import DataFrame
#import numpy as np
import matplotlib.pyplot as plt


df_irisbd = DataFrame.from_csv(r"iris.data",header=None,index_col=None)
print(df_irisbd)
X = df_irisbd.iloc[:, :-1].values
y = df_irisbd.iloc[:, 4].values
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.8,random_state=100)
print(y_test)
from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors=3)

# Train the model using the training sets
model.fit(X_train,y_train)

predicted= model.predict(X_test) # 0:Overcast, 2:Mild
from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test, predicted))
print(classification_report(y_test, predicted))

plt.scatter(df_irisbd[0],df_irisbd[1],color='red')
plt.title("Scatter plot for Price vs Age")
plt.xlabel('Width(cm)')
plt.ylabel('Height(cm)')
plt.show()

plt.hist(df_irisbd[4],edgecolor='red',bins=3)
plt.title("histogram plot for flower name")
plt.xlabel('Flower names')
plt.ylabel('Frequency')
plt.show()