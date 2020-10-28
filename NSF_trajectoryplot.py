#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 18:34:05 2020

@author: Ellen
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 10:05:33 2020

@author: Ellen
"""

import netCDF4
import matplotlib.pyplot as plt
import numpy as np
import cartopy as ct
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter)
import glob
from GetData import GetCDF


#######################
# Plot trajectories of argo floats in designated area
#######################

# Get FloatID
Argofiles='/Users/Ellen/Documents/Python/Argo_NAtlantic.txt'

ArgoNum=[]
count=0

Irm=[]
Lab=[]
BC=[]
Other=[]
AllFloats=[]

print('Start of file reading...')
with open(Argofiles) as fp:
    Lines = fp.readlines()
    for line in Lines:
        count += 1
        x=line.strip()
        ArgoNum=ArgoNum + [x]

#print(ArgoNum)

floatnumlist=ArgoNum[:]
fname_list=[]

for i in floatnumlist:
    floatfname=i
    fname_t=glob.glob('/Users/Ellen/Desktop/ArgoGDAC/dac/'+floatfname+'/*_prof.nc')
    #print('this is f_namet:',fname_t)
    fname_list=fname_list + fname_t

#print(fname_list)
minDate=1000000
maxDate=0
for BGCfile in fname_list:

    # MR - merged file (US) | SR - merged file (?) (FR)
    # B - bio
    # R/D raw/delated

    f = netCDF4.Dataset(BGCfile, mode='r');
    # print(f)        # global attributes

    x=f.variables.keys() ;# get all variable names
    #print(x)
    y=list(x)       #len(y) gives length of list; y[#] = variable

    # Print out varaibles stored in netCDF file
    #print('\n Below are the variables stored in the ARGO float netCDF file \n')
    #print(y)

    fname_complete=BGCfile.split('/')
    titlename=fname_complete[7]

    # Pick variable of interest from list and extract data
    # User input: Variable they want to extract

    # =============================================================================
    # var_int=input('What variable do you want? (Case-sensitive, separate with "," comma & no spaces): ')
    # print(var_int)
    #
    # ### Add Check --> ask for input again if does not exist or error
    #
    # while test_var == 0:
    #
    #     out_value = GetCDF(Var=var_int, Data=f)
    #
    #     if out_value != 'ERROR':
    #         test_var=1
    #
    #     else:
    #         print('*** Sorry that variable does not exist. Please try again. ***')
    #         var_int=input('What variable do you want? (Case-sensitive, separate with "," comma & no spaces): ')
    #         out_value = GetCDF(Var=var_int, Data=f)
    #
    # print('\n Printing out_value...')
    # print(out_value)
    # =============================================================================
    # =============================================================================
    #
    # for i in np.arange(len(y)-1):
    #     print('\n new variable...')
    #     print(f.variables[y[i]])
    #     data = GetCDF(Var=y[i], Data=f)
    #     print('\n Printed data below')
    #     #print(data)
    #     print('end data')
    # =============================================================================

    # Plot trajectory
    # Get Latitidue Data

    LatData = GetCDF(Var='LATITUDE', Data=f)

    # Get Longitude Data
    LonData = GetCDF(Var='LONGITUDE', Data=f)
    dates=GetCDF(Var='JULD', Data=f)
    
    if dates[0] < minDate:
        minDate=dates[0]
    
    if dates[len(dates)-1] > maxDate:
        maxDate=dates[len(dates)-1]

    plt.figure(1)
    #plt.plot(LonData, LatData)

    # Add start and end points?

    #plt.plot(LonData[0],LatData[0],'go',markersize=5)
    #plt.plot(LonData[len(LonData)-1],LatData[len(LonData)-1],'ro',markersize=5)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')


    #gl = NA.gridlines(crs=ct.crs.PlateCarree())
    #gl.xlabels_top = True
    #gl.ylabels_left = True

    #gl.xformatter = LongitudeFormatter()
    #gl.yformatter = LatitudeFormatter()

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

    plt.title(titlename)
    plt.scatter(LonData, LatData,s=2)


plt.show()