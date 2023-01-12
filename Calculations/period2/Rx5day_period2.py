from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d


count = 0

Rx5day = {'historical': np.zeros([480,53,113]),
'period1': np.zeros([480,53,113]),
'period2': np.zeros([480,53,113])
}


historical = 'chirps data/Monthly/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

# Lon: 72 -100
# Lat: 25 - 38
# , vmin=minmin, vmax=maxmax

model = 'MIROC5'

color_map = plt.cm.get_cmap('jet')
reversed_color_map = color_map.reversed()

daysInMonths = [31,28,31,30,31,30,31,31,30,31,30,31]
monthStart = [0,31,59,90,120,151,181,212,243,273,304,334]
monthEnd = [31,59,90,120,151,181,212,243,273,304,334,365]

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

def interpolate(data, oldx, oldy):
    global newx, newy
    newf = interp2d(oldx, oldy, data, kind='quintic')
    new_data = newf(newx, newy)
    return new_data


def calculateRx5day(precip, time_period, month):
    global Rx5day

    max_of_5day_till_here = np.zeros([len(precip),53,113])

    firstWindowSum = np.zeros([53,113])
    monthlyMax = np.zeros([53,113])

    # first window sum end at index 4
    for k in range(5):
        for i in range(53):
            for j in range(113):
                firstWindowSum[i][j] += precip[k][i][j]

    max_of_5day_till_here[4] = firstWindowSum
    monthlyMax = firstWindowSum

    # from next window ending at index 5
    for m in range(5,len(precip)):
        for i in range(53):
            for j in range(113):
                max_of_5day_till_here[m][i][j] = max_of_5day_till_here[m-1][i][j] - precip[m-5][i][j] + precip[m][i][j]
                monthlyMax[i][j] = max(monthlyMax[i][j], max_of_5day_till_here[m][i][j])

    Rx5day[time_period][month] = monthlyMax         
    


##################### Period 2 #####################################
time_period = 'period2'
data = period2
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
        
        if(file.name == 'pr_day_MIROC5_rcp85_r1i1p1_20600101-20691231.nc'):
            ppt = ppt[365:,bottomLat:topLat,leftLon:rightLon]
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

                new_oneMonthPPT = np.zeros([daysInMonths[m],53,113])

                # interpolate here
                for k in range(daysInMonths[m]):
                    oneMonthPPT[k] = oneMonthPPT[k]*60*60*24
                    new_oneMonthPPT[k] = interpolate(oneMonthPPT[k], oldx, oldy)

                # print(new_oneMonthPPT.shape)
                calculateRx5day(new_oneMonthPPT, time_period, month)
                
                month += 1
    
            
        

print(Rx5day[time_period])


# save to npy file
np.save('Calculated Data/Rx5day_period2.npy', Rx5day[time_period])
    