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

color_map = plt.cm.get_cmap('jet')
reversed_color_map = color_map.reversed()

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

def interpolate(data, oldx, oldy):
    global newx, newy
    newf = interp2d(oldx, oldy, data, kind='quintic')
    new_data = newf(newx, newy)
    return new_data

def calculateR99pTOT(precip, time_period, year):
    global r99PercentileInterpolated, r99pTOT
    for i in range(53):
        for j in range(113):
            if(precip[i][j] > r99PercentileInterpolated[i][j]):
                r99pTOT[time_period][year][i][j] += precip[i][j]


##################### Period 1 #####################################
time_period = 'period1'
data = period1
year = 0

with os.scandir(data) as data_files:
    for file in data_files:
        count = count + 1
        fh = Dataset(data + file.name, mode='r')
        lons = np.add(fh.variables['lon'][:], -180)
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        ppt_units = fh.variables['pr'].units

    
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 41.322575870623126)[0][0]
        
        if(file.name == 'pr_day_MIROC5_rcp85_r1i1p1_20200101-20291231.nc'):
            ppt = ppt[365:,bottomLat:topLat,leftLon:rightLon]
        elif(file.name == 'pr_day_MIROC5_rcp85_r1i1p1_20600101-20691231.nc'):
            ppt = ppt[:365,bottomLat:topLat,leftLon:rightLon]
        else:
            ppt = ppt[:,bottomLat:topLat,leftLon:rightLon]
        
        oldx = lons[leftLon:rightLon]
        oldy = lats[bottomLat:topLat]

        print(ppt.shape)
        print(len(ppt)//365)

        for y in range(len(ppt)//365):
            oneYearPPT = ppt[y*365:(y+1)*365]

            print(oneYearPPT.shape)
            
            for matrix in oneYearPPT:
                matrix = matrix*60*60*24

                new_matrix = interpolate(matrix, oldx, oldy)

                
                calculateR99pTOT(new_matrix, time_period, year)
                
            year += 1
            
           
        


print(r99pTOT[time_period])


# save to npy file
np.save('Calculated Data/R99pTOT_period1.npy', r99pTOT[time_period])
      