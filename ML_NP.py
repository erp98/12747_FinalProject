#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:40:57 2020

@author: Ellen
"""

from sklearn import linear_model
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data 
AllData=pd.read_csv('/Users/Ellen/Documents/Python/ALL_GOSHIPData.csv')

bad_val=-999.00

AllData=AllData.replace(bad_val,np.nan)
print('Initial number of data points:', AllData.shape[0])
AllDataNP=AllData[['LAT','LON','PRES','TEMP','SAL','OXY','N','P']]
AllDataNP=AllDataNP.dropna()
print('Final data set size:', AllData.shape[0])
AllDataTC=AllData[['LAT','LON','PRES','TEMP','SAL','OXY','TC']]
AllDataTC=AllDataTC.dropna()
print('Final data set size:', AllDataTC.shape[0])

X=AllDataNP[['LAT','LON','PRES','TEMP','SAL','OXY']]
N=AllDataNP['N']
P=AllDataNP['P']
N_star=(N-16*P+2.9)*0.87
AllDataNP['NStar']=N_star
Y=AllDataNP['NStar']
trainfrac=0.85

x_r=np.arange(0,25)
y_r=(1/16)*x_r

plt.figure()
plt.scatter(N,P)
plt.plot(x_r,y_r,'k-')
plt.xlabel('Nitrate (µmol/kg)')
plt.ylabel('Phosphate (µmol/kg)')

train = AllDataNP[:(int((len(AllDataNP)*trainfrac)))]
test = AllDataNP[(int((len(AllDataNP)*trainfrac))):]

# Do a linear regression 
regr=linear_model.LinearRegression()

train_x = np.array(train[['LAT','LON','PRES','TEMP','SAL','OXY']])
train_y= np.array(train['NStar'])

test_x = np.array(test[['LAT','LON','PRES','TEMP','SAL','OXY']])
test_y= np.array(test['NStar'])

regr.fit(train_x,train_y)

coeff_data = pd.DataFrame(regr.coef_,X.columns, columns=['Coefficients'])
print(coeff_data)

# Predicted values
Y_pred = regr.predict(test_x)
R = r2_score(test_y, Y_pred)
print('R^2 : ', R)

plt.figure()
plt.scatter(test_y,test_x[:,2])
plt.scatter(Y_pred,test_x[:,2])
plt.gca().invert_yaxis()
plt.xlabel('N* (µmol/kg)')
plt.ylabel('Pressure (dbar)')

# Just Phosphate

trainfrac=0.85


train = AllDataNP[:(int((len(AllDataNP)*trainfrac)))]
test = AllDataNP[(int((len(AllDataNP)*trainfrac))):]

# Do a linear regression 
regr=linear_model.LinearRegression()

train_x = np.array(train[['LAT','LON','PRES','TEMP','SAL','OXY','N']])
train_y= np.array(train['P'])

test_x = np.array(test[['LAT','LON','PRES','TEMP','SAL','OXY','N']])
test_y= np.array(test['P'])

regr.fit(train_x,train_y)

X=AllDataNP[['LAT','LON','PRES','TEMP','SAL','OXY','N']]

coeff_data = pd.DataFrame(regr.coef_,X.columns, columns=['Coefficients'])
print(coeff_data)

# Predicted values
Y_pred = regr.predict(test_x)
R = r2_score(test_y, Y_pred)
print('R^2 : ', R)

plt.figure()
plt.scatter(test_y,test_x[:,2])
plt.scatter(Y_pred,test_x[:,2])
plt.gca().invert_yaxis()
plt.xlabel('Phosphate (µmol/kg)')
plt.ylabel('Pressure (dbar)')

N_pred=Y_pred*16
x_1=np.arange(0,25)
y_1=np.arange(0,25)

# Compare calculated vs. measured nitrate
plt.figure()
plt.scatter(test_x[:,6],N_pred)
plt.plot(x_1,y_1, 'k-')
plt.xlabel('Measure Nitrate (µmol/kg)')
plt.ylabel('Modeled Nitrate (µmol/kg)')

#N_star=(N-16*P+2.9)*0.87

N_star_true=test_x[:,6]-16*test_y
N_star_model=test_x[:,6]-16*Y_pred

x_1=np.arange(-4,4)
y_1=np.arange(-4,4)
plt.figure()
plt.scatter(N_star_true,N_star_model)
plt.plot(x_1,y_1, 'k-')
plt.xlabel('Measured N*')
plt.ylabel('Modeled N*')

print('N* values')
R = r2_score(N_star_true, N_star_model)
print('R^2 : ', R)

# DIC

X=AllDataTC[['LAT','LON','PRES','TEMP','SAL','OXY']]
Y=AllDataTC['TC']

trainfrac=0.80

train = AllDataTC[:(int((len(AllDataTC)*trainfrac)))]
test = AllDataTC[(int((len(AllDataTC)*trainfrac))):]

# Do a linear regression 
regr=linear_model.LinearRegression()

train_x = np.array(train[['LAT','LON','PRES','TEMP','SAL','OXY']])
train_y= np.array(train['TC'])

test_x = np.array(test[['LAT','LON','PRES','TEMP','SAL','OXY']])
test_y= np.array(test['TC'])

regr.fit(train_x,train_y)

X=AllDataNP[['LAT','LON','PRES','TEMP','SAL','OXY']]

coeff_data = pd.DataFrame(regr.coef_,X.columns, columns=['Coefficients'])
print(coeff_data)

# Predicted values
Y_pred = regr.predict(test_x)
R = r2_score(test_y, Y_pred)
print('R^2 : ', R)

plt.figure()
plt.scatter(test_y,test_x[:,2])
plt.scatter(Y_pred,test_x[:,2])
plt.gca().invert_yaxis()
plt.xlabel('DIC (µmol/kg)')
plt.ylabel('Pressure (dbar)')

plt.show()