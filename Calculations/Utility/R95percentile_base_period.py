from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d

count = 0
totalDays = 10950

r95Percentile = np.zeros([10,21])

r95PercentileInterpolated = np.zeros([53,113])

basePeriod = 'CMIP5/0Major 4/MIROC5/basePeriod/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

# Lon: 72 -100
# Lat: 25 - 38


totalPeriod = np.zeros([1,10,21])

with os.scandir(basePeriod) as data_files:
    for file in data_files:
        count = count + 1
        fh = Dataset(basePeriod + file.name, mode='r')
        lons = np.add(fh.variables['lon'][:], -180)
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        ppt_units = fh.variables['pr'].units

    
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 38.52105552662436)[0][0]

        print(ppt.shape)
        if(file.name == 'pr_day_MIROC5_historical_r1i1p1_19600101-19691231.nc'):
            totalPeriod = ppt[:,bottomLat:topLat,leftLon:rightLon]*24*60*60
        else:
            totalPeriod = np.vstack((ppt[:,bottomLat:topLat,leftLon:rightLon]*24*60*60, totalPeriod))


print(totalPeriod.shape)


r95Percentile = np.percentile(totalPeriod, 95, axis=0)
print(r95Percentile)

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]

newf = interp2d(oldx, oldy, r95Percentile, kind='quintic')

r95PercentileInterpolated = newf(newx, newy)
print(r95PercentileInterpolated)
print(r95PercentileInterpolated.shape)

np.save('Calculated Data/95Percentile_BasePeriod.npy', r95PercentileInterpolated)
