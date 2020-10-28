#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 10:09:53 2020

@author: Ellen
"""
import glob
import pandas as pd
import numpy as np
import csv
from datetime import datetime
from sklearn import linear_model

# Load all GOSHIP data and store in a large data frame 
# X = GOSHIP (Date, Lat, Lon, Pressure, Temp, Salinity, Oxygen)
# Y = GOSHIP Data (TC)

BoatFileList=glob.glob('/Users/Ellen/Desktop/GOSHIP_Data/*')
df_counter=0

for CruiseFolder in BoatFileList:

# Go into each Cruise Folder and determine what data is there
    ShipData = glob.glob(CruiseFolder+'/*')
    #print(ShipData)

    File=[]
    Folder=[]

    for shipdata in ShipData:
        sdfname=shipdata.split('/')
        sdfname=sdfname[6]

        ftype=sdfname.split('.')

        if len(ftype) > 1:
            # Means file is file
            File=File+[shipdata]
        else:
            # Means file is a folder
            Folder=Folder+[shipdata]

    # Bottle files
    CSVfind = 0
    BottleFile=[]

    for i in File:
        sdfname=i.split('/')
        sdfname=sdfname[6]

        ftype=sdfname.split('.')

        ftag=ftype[1]

        if ftag == 'csv':
            #print('CSV file')
            #print(shipdata)
            CSVfind =CSVfind+1
            BottleFile=BottleFile+[i]

            # these csv bfiles are bottle measurements?

    print('CSV: ',BottleFile)

    # CTD files
    CTDfind=0
    CTDFolder=[]

    for i in Folder:
        sdfname=i.split('/')
        sdfname=sdfname[6]
        ftype=sdfname.split('_')
        ftag=ftype[len(ftype)-1]

        if ftag == 'ct1':
            # CTD measurements at many depths
            # T,S,P, DOXY
            CTDfind=CTDfind+1
            CTDFolder=CTDFolder+[i]

    print('CTD: ', CTDFolder)

# If there are bottle files and/or CTD files
# Open them, find dates, lat-lon, values

    # CSV bottle files
    if CSVfind != 0:

        for botfname in BottleFile:

            rcon=0

            with open(botfname) as csvfile:
                spamreader = csv.reader(csvfile)

                for row in spamreader:

                    if len(row[0]) > 0:
                        #print(row[0][0])

                        if (row[0][0] == '#' or row[0]=='BOTTLE'):
                            rcon=rcon+1
            #print('Row count:',rcon)

            BottleData = pd.read_csv(botfname, skiprows=rcon)
            #print(Data)
            
            # Make sure there is TCarbon data
            # ['TCARBN','PHSPHT','NO2+NO3','NITRAT']
            var_oi1='NITRAT'
            var_oi2='PHSPHT'
            var_check=0
            var_check1=0
            var_check2=0
            z = 0
            while z < len(BottleData.columns)-1 and var_check ==0:
                
                if BottleData.columns[z] == var_oi1:
                    var_check1 = 1
                    
                if BottleData.columns[z] == var_oi2:
                    var_check2=1
                    
                if var_check1==1 and var_check2==1:
                    var_check=1
                    
                z=z+1
            
            if var_check == 1:

                BotLat=BottleData.loc[1:,'LATITUDE']
                BotLat=BotLat[:-1]
                BotLon=BottleData.loc[1:,'LONGITUDE']
                BotLon=BotLon[:-1]
                BotDate=BottleData.loc[1:,'DATE']
                BotDate=BotDate[:-1]
                BotDate=BotDate.astype('int').astype('str')
                
                BotPres=BottleData.loc[1:,'CTDPRS']
                BotPres=BotPres[:-1]
                BotTemp=BottleData.loc[1:,'CTDTMP']
                BotTemp=BotTemp[:-1]
                BotSal=BottleData.loc[1:,'CTDSAL']
                BotSal=BotSal[:-1]
                BotOxy=BottleData.loc[1:,'OXYGEN']
                BotOxy=BotOxy[:-1]
                
                var_check=0 
                z=0
                while z < len(BottleData.columns)-1 and var_check ==0:
                    if BottleData.columns[z] == 'TCARBN':
                        var_check = 1
                    z=z+1
                        
                if var_check==1:
                    BotTC=BottleData.loc[1:,'TCARBN']
                    BotTC=BotTC[:-1]
                
                else:
                    BotTC=[np.NaN]
                    
                BotN=BottleData.loc[1:,'NITRAT']
                BotN=BotN[:-1]
                BotP=BottleData.loc[1:,'PHSPHT']
                BotP=BotP[:-1]
                
                DataType='BOTTLE'
    
                for i in BotDate.index:
                    BotDate[i]=datetime.strptime(BotDate[i],'%Y%m%d')
                    
                for i in np.arange(1,len(BotLat)+1):
                    Date=BotDate[i]
                    CruiseLat=BotLat[i]
                    CruiseLon=BotLon[i]
                    CruisePres=BotPres[i]
                    CruiseTemp=BotTemp[i]
                    CruiseSal=BotSal[i]
                    CruiseOxy=BotOxy[i]
                    
                    if len(BotTC) <= 1:
                        CruiseTC=-999.00 #BotTC[i]
                    else:
                        CruiseTC=BotTC[i]
                        
                    CruiseN=BotN[i]
                    CruiseP=BotP[i]
    
                    to_df={'CRUISE': [CruiseFolder],'FILENAME': [botfname],'DATATYPE': [DataType],'DATE': [Date],'LAT':[CruiseLat],'LON':[CruiseLon],'PRES': [CruisePres],'TEMP':[CruiseTemp], 'SAL':[CruiseSal],'OXY': [CruiseOxy],'TC':[CruiseTC],'P': [CruiseP],'N':[CruiseN]}
                    df_temp=pd.DataFrame(data=to_df)
        
                    if df_counter == 0:
                        GOSHIPData=df_temp
                        df_counter=1
                    else:
                        GOSHIPData=GOSHIPData.append(df_temp, ignore_index=True)
                        
GOSHIPData.to_csv('/Users/Ellen/Documents/Python/ALL_GOSHIPData.csv')


