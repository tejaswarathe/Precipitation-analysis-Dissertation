from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d


count = 0
totalDays = 10950
totalPeriod = np.zeros([1,10,21])
r95Percentile = np.zeros([10,21])

r95PercentileInterpolated = np.zeros([53,113])



# Lon: 72 -100
# Lat: 25 - 38

def calculateR95pTOT(precip, year):
    global r95PercentileInterpolated, r95pTOT
    for i in range(bottomLat, topLat):
        for j in range(leftLon, rightLon):
            if(matrix[i][j] >= r95PercentileInterpolated[i][j]):
                r95pTOT[year-1981][i-bottomLat][j-leftLon] += matrix[i][j]



basePeriod = 'CMIP5/0Major 4/MIROC5/basePeriod/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'


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

     
            # if (count==365):
            #     print(cdd_matrix)
            #     break

print(totalPeriod.shape)

r95Percentile = np.percentile(totalPeriod, 95, axis=0)
print(r95Percentile.shape)


newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]

newf = interp2d(oldx, oldy, r95Percentile, kind='quintic')

r95PercentileInterpolated = newf(newx, newy)
print(r95PercentileInterpolated)
print(r95PercentileInterpolated.shape)



with os.scandir('chirps data/Annual/') as data_files:
    for file in data_files:
        fh = Dataset('chirps data/Annual/' + file.name, mode='r')
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
        calculateR20mm(ppt)
        # if(count == 12):
        break

# map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)

# x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# # Plot Data
# cs = map.pcolor(x, y, R20mm, cmap='gist_rainbow', shading='auto')
# map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
# map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
# map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
# map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
# map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')

# # map.drawcoastlines()
# # map.drawcountries()

# # Add Colorbar
# cbar = map.colorbar(cs, location='bottom', pad="10%")
# cbar.set_label('days')

# plt.pyplot.title('R20mm')
# # plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
# plt.pyplot.show()
