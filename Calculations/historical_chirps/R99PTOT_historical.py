from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d

count = 0
totalDays = 10950

r99PercentileInterpolated = np.load('Calculated Data/99Percentile_BasePeriod.npy')

historical = 'chirps data/Annual/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

# Lon: 72 -100
# Lat: 25 - 38

r99pTOT = {'historical' : np.zeros([40,53,113]),
                     'period1' : np.zeros([40,53,113]),
                     'period2' : np.zeros([40,53,113]) }


def calculateR99pTOT(precip, time_period, year):
    global r99PercentileInterpolated, r99pTOT
    for i in range(53):
        for j in range(113):
            if(precip[i][j] > r99PercentileInterpolated[i][j]):
                r99pTOT[time_period][year][i][j] += precip[i][j]


################### Historical Plot #########################
time_period = 'historical'
data = historical
year = 0

with os.scandir(data) as data_files:
    for file in data_files:
        fh = Dataset(data + file.name, mode='r')
        count = count + 1
        # print(fh.variables)
        lons = fh.variables['longitude'][:]
        lats = fh.variables['latitude'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precip'][:]
        # print(ppt.shape)
        ppt_units = fh.variables['precip'].units

        leftLon = np.where(lons == 71.875)[0][0]
        rightLon = np.where(lons == 100.125)[0][0]
        bottomLat = np.where(lats == 24.875)[0][0]
        topLat = np.where(lats == 38.125)[0][0]

        print(count)

        for matrix in ppt:
            matrix = matrix[bottomLat:topLat,leftLon:rightLon]
            calculateR99pTOT(matrix, time_period, year)
        year += 1
    

print(r99pTOT[time_period])


# save to npy file
np.save('Calculated Data/R99pTOT_historical.npy', r99pTOT[time_period])

