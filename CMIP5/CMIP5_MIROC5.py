from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap

count = 0
total_prcpt_in_the_year = np.zeros([10,21])

cdd_matrix = np.zeros([10,21])
current_cdd_matrix = np.zeros([10,21])

def calculateTotalPrcpt(matrix):
    global total_prcpt_in_the_year
    total_prcpt_in_the_year = np.add(matrix, total_prcpt_in_the_year)

def calculateCDD(precip):
    global cdd_matrix
    for i in range(bottomLat, topLat):
        for j in range(leftLon, rightLon):
            if(matrix[i][j]*24*60*60 < 1):
                current_cdd_matrix[i-bottomLat][j-leftLon] += 1
            else:  
                cdd_matrix[i-bottomLat][j-leftLon] = max(current_cdd_matrix[i-bottomLat][j-leftLon], cdd_matrix[i-bottomLat][j-leftLon])
                current_cdd_matrix[i-bottomLat][j-leftLon] = 0
            cdd_matrix[i-bottomLat][j-leftLon] = max(current_cdd_matrix[i-bottomLat][j-leftLon], cdd_matrix[i-bottomLat][j-leftLon])




period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

with os.scandir(period1) as data_files:
    for file in data_files:
        count = count + 1
        fh = Dataset(period1 + file.name, mode='r')
        lons = np.add(fh.variables['lon'][:], -180)
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        ppt_units = fh.variables['pr'].units

        print(lons)
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 38.52105552662436)[0][0]
        print(count)
        break
        # count = count + 1
        for matrix in ppt:
            
            # print(matrix[bottomLat:topLat,leftLon:rightLon])
            # calculateCDD(matrix)
            matrix = matrix[bottomLat:topLat,leftLon:rightLon]*24*60*60
            print(matrix)
            calculateTotalPrcpt(matrix)
            break
            
            # if (count==365):
            #     print(cdd_matrix)
            #     break
        break
     

      

# print(total_prcpt_in_the_year)
# 5 states

map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)


x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, total_prcpt_in_the_year, cmap='gist_rainbow', shading='auto')
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

plt.pyplot.title('Total precipitation')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.pyplot.show()
