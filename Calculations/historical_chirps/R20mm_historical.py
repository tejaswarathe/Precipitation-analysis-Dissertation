from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d


count = 0

R20mm = {'historical': np.zeros([40,53,113]),
'period1': np.zeros([40,53,113]),
'period2': np.zeros([40,53,113])
}


historical = 'chirps data/Annual/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

# Lon: 72 -100
# Lat: 25 - 38
# , vmin=minmin, vmax=maxmax

model = 'MIROC5'

color_map = plt.cm.get_cmap('jet')
reversed_color_map = color_map.reversed()



def calculateR20mm(precip, time_period, year):
    global R20mm
    for i in range(53):
        for j in range(113):
            if(precip[i][j] >= 20):
                R20mm[time_period][year][i][j] += 1




fig, axes = plt.subplots(1,3)
minmin = 0
maxmax = 10000

print(axes)

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
            calculateR20mm(matrix, time_period, year)
        year += 1

print(R20mm)


# save to npy file
# np.save('Calculated Data/R20mm_historical.npy', R20mm[time_period])

