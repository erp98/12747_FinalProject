#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 08:14:10 2020

@author: Ellen
"""
import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

AllData=pd.read_csv('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIPData.csv')
bad_val=-999.00
AllData=AllData.replace(bad_val,np.nan)
AllData=AllData.dropna()

newind=np.arange(AllData.shape[0])
s = pd.Series(list(newind))
AllData=AllData.set_index([s])

# calculate N*
N_star=(AllData.loc[:,'N']-16*AllData.loc[:,'P']+2.9)*0.87

param=['LAT','LON','PRES','TEMP','SAL','OXY','N']

for i in param:
    
    X = AllData.loc[:, i].values.reshape(-1, 1)
    Y = N_star.values.reshape(-1, 1)
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    
    print(i)
    R = r2_score(Y, Y_pred)
    print('R^2 : ', R)
    
    plt.figure()
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.xlabel(i)
    plt.ylabel('N* (µmol/kg)')

plt.show()