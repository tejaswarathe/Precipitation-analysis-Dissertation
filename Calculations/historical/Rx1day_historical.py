from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d


count = 0

Rx1day = {'historical': np.zeros([480,53,113]),
'period1': np.zeros([480,53,113]),
'period2': np.zeros([480,53,113])
}


historical = 'CMIP5/0Major 4/MIROC5/historical/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

# Lon: 72 -100
# Lat: 25 - 38
# , vmin=minmin, vmax=maxmax

model = 'MIROC5'

color_map = plt.cm.get_cmap('jet')
reversed_color_map = color_map.reversed()


monthStart = [0,31,59,90,120,151,181,212,243,273,304,334]
monthEnd = [31,59,90,120,151,181,212,243,273,304,334,365]

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

def interpolate(data, oldx, oldy):
    global newx, newy
    newf = interp2d(oldx, oldy, data, kind='quintic')
    new_data = newf(newx, newy)
    return new_data


def calculateRx1day(precip, time_period, month):
    global Rx1day
    for i in range(53):
        for j in range(113):
            Rx1day[time_period][month][i][j] = max(precip[i][j], Rx1day[time_period][month][i][j])



##################### Period 1 #####################################
time_period = 'historical'
data = historical
month = 0

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
        
        if(file.name == 'pr_day_MIROC5_historical_r1i1p1_19800101-19891231.nc'):
            ppt = ppt[365:,bottomLat:topLat,leftLon:rightLon]
        elif(file.name == 'pr_day_MIROC5_rcp85_r1i1p1_20200101-20291231.nc'):
            ppt = ppt[:365,bottomLat:topLat,leftLon:rightLon]
        else:
            ppt = ppt[:,bottomLat:topLat,leftLon:rightLon]
        
        oldx = lons[leftLon:rightLon]
        oldy = lats[bottomLat:topLat]

        print(ppt.shape)
        print(len(ppt)//365)


        for y in range(len(ppt)//365):
            oneYearPPT = ppt[y*365:(y+1)*365]

            for m in range(12):
                oneMonthPPT = oneYearPPT[monthStart[m]:monthEnd[m]]

                # print(oneMonthPPT.shape)

                for matrix in oneMonthPPT:
                    matrix = matrix*60*60*24

                    new_matrix = interpolate(matrix, oldx, oldy)

                    calculateRx1day(new_matrix, time_period, month)
                
                month += 1
           
            
           
        


print(Rx1day[time_period])


# save to npy file
np.save('Calculated Data/Historical/Rx1day_historical.npy', Rx1day[time_period])
    