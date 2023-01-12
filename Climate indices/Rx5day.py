from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap

count = 0
Rx5day = np.zeros([53,113])
Rx5day_matrix = np.zeros([31,53,113])

# Lon: 72 -100
# Lat: 25 - 38

def calculateRx5day(precip):
    global Rx5day, Rx5day_matrix
    for m in range(len(precip)-5):
        for i in range(bottomLat, topLat):
            for j in range(leftLon, rightLon):
                for k in range(5):
                    Rx5day_matrix[m][i-bottomLat][j-leftLon] += precip[m+k][i][j]*24
    
    for m in range(len(Rx5day_matrix)):
        for i in range(len(Rx5day_matrix[m])):
            for j in range(len(Rx5day_matrix[m][i])):
                Rx5day[i][j] = max(Rx5day_matrix[m][i][j], Rx5day[i][j])




with os.scandir('chirps data/Monthly/') as data_files:
    for file in data_files:
        fh = Dataset('chirps data/Monthly/' + file.name, mode='r')
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
        calculateRx5day(ppt)
        if(count == 12):
            break

# print(Rx5day_matrix)
Rx5day = Rx5day*(1/12)
print(Rx5day)

map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, Rx5day, cmap='gist_rainbow', shading='auto')
map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')
# map.drawcoastlines()
# map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('mm')

plt.pyplot.title('Rx5day')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.pyplot.show()
