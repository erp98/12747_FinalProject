#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 18:47:37 2020

@author: Ellen
"""

import pandas as pd
import numpy as np
import cartopy as ct
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter)
import matplotlib.pyplot as plt

Argofiles='/Users/Ellen/Documents/Python/Index_NAtlantic.txt'
ColNames=['Fname','Date','Lat','Lon','Ocean','ProfType','Inst','Variables','VarDateMode','DateQC']

Data=pd.read_csv(Argofiles, names=ColNames)

LatVals=Data.loc[:,'Lat']
LonVals=Data.loc[:,'Lon']
FName=Data.loc[:,'Fname']
Vars=Data.loc[:,'Variables']

plt.figure(1)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
NA = plt.axes(projection=ct.crs.PlateCarree())

NA.set_extent([0, -80, 0, 65])
        
lonval=-1*np.arange(0,80,10)
latval=np.arange(0,65,10)
        
NA.set_xticks(lonval, crs=ct.crs.PlateCarree())
NA.set_yticks(latval, crs=ct.crs.PlateCarree())
        
lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
        
NA.add_feature(ct.feature.COASTLINE)
NA.add_feature(ct.feature.OCEAN)
        
NA.xaxis.set_major_formatter(lon_formatter)
NA.yaxis.set_major_formatter(lat_formatter)
        
plt.title('Argo Floats w Oxygen')

oxy_count=0
Oxy_Float=0
prevfloat=000
             
for i in np.arange(len(LatVals)):
    
    varslist=Vars[i].split()
    
    j=0
    varcheck=0
    
    while j < len(varslist) and varcheck==0:
        
        if varslist[j] == 'DOXY':
            plt.figure(1)
            plt.plot(LonVals[i], LatVals[i],'ro',markersize=2)
            varcheck=1
            oxy_count=oxy_count+1
            
            floattemp=int(FName[i].split('/')[1])
            
            if floattemp != prevfloat:
                prevfloat=floattemp
                Oxy_Float=Oxy_Float+1
        j=j+1
        
plt.figure(2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
NA = plt.axes(projection=ct.crs.PlateCarree())

NA.set_extent([0, -80, 0, 65])
        
lonval=-1*np.arange(0,80,10)
latval=np.arange(0,65,10)
        
NA.set_xticks(lonval, crs=ct.crs.PlateCarree())
NA.set_yticks(latval, crs=ct.crs.PlateCarree())
        
lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
        
NA.add_feature(ct.feature.COASTLINE)
NA.add_feature(ct.feature.OCEAN)
        
NA.xaxis.set_major_formatter(lon_formatter)
NA.yaxis.set_major_formatter(lat_formatter)
        
plt.title('Argo Floats w Nitrate')

N_count=0
N_Float=0
prevfloat=000
             
for i in np.arange(len(LatVals)):
    
    varslist=Vars[i].split()
    
    j=0
    varcheck=0
    
    while j < len(varslist) and varcheck==0:
        
        if varslist[j] == 'NITRATE':
            plt.figure(2)
            plt.plot(LonVals[i], LatVals[i],'ro',markersize=2)
            varcheck=1
            N_count=N_count+1
            
            floattemp=int(FName[i].split('/')[1])
            
            if floattemp != prevfloat:
                prevfloat=floattemp
                N_Float=N_Float+1
                
        j=j+1

plt.figure(3)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
NA = plt.axes(projection=ct.crs.PlateCarree())

NA.set_extent([0, -80, 0, 65])
        
lonval=-1*np.arange(0,80,10)
latval=np.arange(0,65,10)
        
NA.set_xticks(lonval, crs=ct.crs.PlateCarree())
NA.set_yticks(latval, crs=ct.crs.PlateCarree())
        
lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
        
NA.add_feature(ct.feature.COASTLINE)
NA.add_feature(ct.feature.OCEAN)
        
NA.xaxis.set_major_formatter(lon_formatter)
NA.yaxis.set_major_formatter(lat_formatter)
        
plt.title('Argo Floats w Oxygen and Nitrate')

NO_count=0
Both_Float=0
prevfloat=000
             
for i in np.arange(len(LatVals)):
    
    varslist=Vars[i].split()
    
    j=0
    varcheck1=0
    varcheck2=0
    
    while j < len(varslist) and (varcheck1+varcheck2)<2:
        
        if varslist[j] == 'NITRATE':
            varcheck2=1
        if varslist[j] =='DOXY':
            varcheck1=1
        
        j=j+1
    
    if varcheck1==1 and varcheck2 == 1:
        plt.figure(3)
        plt.plot(LonVals[i], LatVals[i],'ro',markersize=2)
        NO_count=NO_count+1
        
        floattemp=int(FName[i].split('/')[1])
            
        if floattemp != prevfloat:
            prevfloat=floattemp
            Both_Float=Both_Float+1
             
plt.show()
print('Oxygen Floats: ', Oxy_Float)
print('Oxygen profiles: ', oxy_count)
print('Nitrate Floats: ', N_Float)
print('Nitrate profiles: ', N_count)
print('Both Floats: ',Both_Float)
print('Both profiles: ',NO_count)