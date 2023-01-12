from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap

count = 0
cwd_matrix = np.zeros([53,113])

current_cwd_matrix = np.zeros([53,113])


# Lon: 72 -100
# Lat: 25 - 38



def calculateCWD(precip):
    global cwd_matrix
    for matrix in precip:
        for i in range(bottomLat, topLat):
            for j in range(leftLon, rightLon):
                if(matrix[i][j]*24 >= 1):
                    current_cwd_matrix[i-bottomLat][j-leftLon] += 1
                else:  
                    cwd_matrix[i-bottomLat][j-leftLon] = max(current_cwd_matrix[i-bottomLat][j-leftLon], cwd_matrix[i-bottomLat][j-leftLon])
                    current_cwd_matrix[i-bottomLat][j-leftLon] = 0
                cwd_matrix[i-bottomLat][j-leftLon] = max(current_cwd_matrix[i-bottomLat][j-leftLon], cwd_matrix[i-bottomLat][j-leftLon])



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
        
        calculateCWD(ppt)
        if(count == 12):
            break

print(cwd_matrix)

map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, cwd_matrix, cmap='gist_rainbow', shading='auto')
map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')
# map.drawcoastlines()
# map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('days')

plt.pyplot.title('Consecutive Wet days')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.pyplot.show()
