# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 15:17:44 2019

@author: Student
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

cars_data=pd.read_csv('Toyota.csv',index_col=0,na_values=['??','????'])
print(cars_data)
cars_data.dropna(axis=0,inplace=True)
print(cars_data)

plt.scatter(cars_data['Age'],cars_data['Price'],color='red')
plt.title("Scatter plot for Price vs Age")
plt.xlabel('Age(Years)')
plt.ylabel('Price(Dollars)')
plt.show()

plt.hist(cars_data['KM'],color='green',edgecolor='white',bins=20)
plt.title("histogram plot for KM")
plt.xlabel('KM')
plt.ylabel('Frequency')
plt.show()

counts=[979,120,12]
fuelType=['petrol','diesel','CNG']
index=np.arange(len(fuelType))
print(index)

plt.bar(index,counts,color=['red','blue','cyan'])
plt.title("Bar graph for fuel types")
plt.xlabel('Flue types')
plt.ylabel('Frequency')
plt.xticks(index,fuelType,rotation=45)
plt.show()