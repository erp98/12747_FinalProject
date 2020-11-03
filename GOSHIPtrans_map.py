

import matplotlib.pyplot as plt
import numpy as np
import cartopy as ct
from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter)
import numpy as np
import pandas as pd

AllData=pd.read_csv('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIPData.csv')
bad_val=-999.00
AllData=AllData.replace(bad_val,np.nan)
AllData=AllData.dropna()

newind=np.arange(AllData.shape[0])
s = pd.Series(list(newind))
AllData=AllData.set_index([s])

prevLat=0
prevLon=0

Lat=AllData.loc[:,'LAT']
Lon=AllData.loc[:,'LON']
AllData["DATE"] =AllData["DATE"].astype("datetime64")
Date=AllData.loc[:,'DATE']

Cruise=AllData.loc[:,'CRUISE']
Pres=AllData.loc[:,'PRES']
Temp=AllData.loc[:,'TEMP']
Sal=AllData.loc[:,'SAL']
Oxy=AllData.loc[:,'OXY']
Nit=AllData.loc[:,'N']
Phos=AllData.loc[:,'P']

# goodLat=[np.nan]*Lat.shape[0]
# goodLat=np.array(goodLat)
# goodLon=[np.nan]*Lat.shape[0]
# goodLon=np.array(goodLon)

goodLat=[]
goodLon=[]
goodDate=[]

for i in np.arange(len(Lat)):
    
    if Lat[i] != prevLat:
        if Lon[i] != prevLon:
            goodLat=goodLat+[Lat[i]]
            goodLon=goodLon+[Lon[i]]
            goodDate=goodDate+[Date[i]]
            
goodLat=np.array(goodLat)
goodLon=np.array(goodLon)
goodDate=np.array(goodDate)

plt.figure(1)
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

plt.scatter(goodLon, goodLat,s=1,c='r',marker='o')
plt.title('GO-SHIP Transects')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIPTransects.jpg')

## Date Histogram
plt.figure(2)
d=pd.DataFrame({'Date': goodDate})#, 'Lat': goodLat,'Lon': goodLon})
d.groupby([d["Date"].dt.year,d["Date"].dt.month]).count().plot(kind="bar")
plt.xlabel('Date (Year,Month)')
plt.ylabel('Profile Counts')
plt.title('GO-SHIP Date Historgram (Year-Month)')
plt.tight_layout()
plt.savefig('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIP_YM_hist.jpg')

plt.figure(3)
d.groupby(d["Date"].dt.month).count().plot(kind="bar")
plt.xlabel('Date (Month)')
plt.ylabel('Profile Counts')
plt.title('GO-SHIP Date Historgram (Month)')
plt.tight_layout()
plt.savefig('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIP_M_hist.jpg')


####


startind=[0]
endind=[]

prevCruise=Cruise[0]

for i in np.arange(len(Cruise)):
    
    if Cruise[i] != prevCruise:
        
            startind=startind+[i]
            
            if i != 0:
                endind=endind+[i-1]
                
            prevCruise=Cruise[i]
                
            
endind=endind+[i]

StartI=startind[0]
EndI=endind[0]

# CruiseLat=AllData.loc[StartI:EndI,'LAT']
# CruiseLon=AllData.loc[StartI:EndI,'LON']
# CruiseDate=AllData.loc[StartI:EndI,'DATE']
# CruisePres=AllData.loc[StartI:EndI,'PRES']
# CruiseTemp=AllData.loc[StartI:EndI,'TEMP']
# CruiseSal=AllData.loc[StartI:EndI,'SAL']
# CruiseOxy=AllData.loc[StartI:EndI,'OXY']
# CruiseP=AllData.loc[StartI:EndI,'P']
# CruiseN=AllData.loc[StartI:EndI,'N']

cruisedata=AllData.iloc[StartI:EndI,:]
cruisedata['DATE']=cruisedata['DATE'].dt.strftime('%Y-%m-%d')

# Plot cruise trajectory
plt.figure(4)
NA = plt.axes(projection=ct.crs.PlateCarree())
NA.set_extent([0, -80, 0, 65])
lonval=-1*np.arange(0,80,10)
latval=np.arange(0,65,10)
NA.set_xticks(lonval, crs=ct.crs.PlateCarree())
NA.set_yticks(latval, crs=ct.crs.PlateCarree())
lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
NA.add_feature(ct.feature.OCEAN)
NA.xaxis.set_major_formatter(lon_formatter)
NA.yaxis.set_major_formatter(lat_formatter)

plt.scatter(cruisedata.loc[:,'LON'], cruisedata.loc[:,'LAT'],s=2,c='r',marker='o')
plt.title('GO-SHIP Transects')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIP_SampleTransLoc.jpg')



fig, ax = plt.subplots(5,1)
cruisedata.plot(kind='scatter',x='DATE',y='PRES',c='TEMP',vmin=-3, vmax=15,cmap='jet',ax=ax[0],s=1)
ax[0].invert_yaxis()
ax[0].set_xticks([])
cruisedata.plot(kind='scatter',x='DATE',y='PRES',c='SAL',vmin=33, vmax=37,cmap='jet',ax=ax[1],s=1)
ax[1].invert_yaxis()
ax[1].set_xticks([])
cruisedata.plot(kind='scatter',x='DATE',y='PRES',c='OXY',vmin=200, vmax=400,cmap='jet',ax=ax[2],s=1)
ax[2].invert_yaxis()
ax[2].set_xticks([])
cruisedata.plot(kind='scatter',x='DATE',y='PRES',c='N',vmin=0, vmax=20,cmap='jet',ax=ax[3],s=1)
ax[3].invert_yaxis()
ax[3].set_xticks([])
cruisedata.plot(kind='scatter',x='DATE',y='PRES',c='P',vmin=0, vmax=1,cmap='jet',ax=ax[4],s=1)
ax[4].invert_yaxis()
plt.xticks(rotation=45)
plt.savefig('/Users/Ellen/Documents/GitHub/12747_FinalProject/GOSHIP_SampleTransProp.jpg')
plt.tight_layout()

plt.show()
