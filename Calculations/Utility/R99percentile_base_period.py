from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d

count = 0
totalDays = 10950

r99Percentile = np.zeros([10,21])

r99PercentileInterpolated = np.zeros([53,113])

basePeriod = 'CMIP5/0Major 4/MIROC5/basePeriod/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

# Lon: 72 -100
# Lat: 25 - 38


def calculateR99pTOT(precip, year, period):
    global r99PercentileInterpolated, r99pTOT
    for i in range(topLat-bottomLat):
        for j in range(rightLon-leftLon):
            if(matrix[i][j] >= r99PercentileInterpolated[i][j]):
                r99pTOT[period][year][i][j] += matrix[i][j]


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


r99Percentile = np.percentile(totalPeriod, 99, axis=0)
print(r99Percentile)

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]

newf = interp2d(oldx, oldy, r99Percentile, kind='quintic')

r99PercentileInterpolated = newf(newx, newy)
print(r99PercentileInterpolated)
print(r99PercentileInterpolated.shape)

np.save('Calculated Data/99Percentile_BasePeriod.npy', r99PercentileInterpolated)
