import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d




count = 0
total_prcpt_in_the_year = np.zeros([10,21])

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'

def calculateTotalPrcpt(matrix):
    global total_prcpt_in_the_year
    total_prcpt_in_the_year = np.add(matrix, total_prcpt_in_the_year)


with os.scandir(period1) as data_files:
    for file in data_files:
     
        fh = Dataset(period1 + file.name, mode='r')
        lons = np.add(fh.variables['lon'][:], -180)
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        ppt_units = fh.variables['pr'].units

#         print(fh.variables)
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 38.52105552662436)[0][0]



        for matrix in ppt:
            count = count + 1 
            matrix = matrix[bottomLat:topLat,leftLon:rightLon]*24*60*60
            calculateTotalPrcpt(matrix)
            if(count == 365):
                break

        break


print(lons.shape)
print(lats.shape)
print(ppt.shape)

oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]
newf = interp2d(oldx, oldy, total_prcpt_in_the_year, kind='linear')
# newf = interp2d(oldx, oldy, total_prcpt_in_the_year, kind='cubic')
# newf = interp2d(oldx, oldy, total_prcpt_in_the_year, kind='quintic')

data_new = newf(newx, newy)
print(data_new.shape)


map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)


# Plot Data
cs = map.pcolor(oldx, oldy, total_prcpt_in_the_year, cmap='gist_rainbow', shading='auto')
# cs = map.pcolor(newx, newy, data_new, cmap='gist_rainbow', shading='auto')


map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('mm')

plt.title('MIROC5 Original')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.show()
