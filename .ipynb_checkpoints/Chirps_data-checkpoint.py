from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap

count = 0
total_prcpt_in_the_year = np.zeros([400,1440])
mean_prcpt_in_the_year = np.zeros([400,1440])

numOfdays = {'preMonsoon': 92,
'monsoon':122,
'postMonsoon': 61,
'winter': 91}

def calculateTotalPrcpt(precip):
    global total_prcpt_in_the_year
    for matrix in precip:
        total_prcpt_in_the_year = np.add(matrix, total_prcpt_in_the_year)

def calculateMeanPrecipitation():
    global mean_prcpt_in_the_year, total_prcpt_in_the_year, numOfdays
    mean_prcpt_in_the_year = np.true_divide(total_prcpt_in_the_year, 365)
    print(mean_prcpt_in_the_year)

with os.scandir('chirps data/Monthly') as data_files:
    for file in data_files:
        fh = Dataset('chirps data/Monthly' + file.name, mode='r')
        count = count + 1
        # print(fh.variables)
        lons = fh.variables['longitude'][:]
        lats = fh.variables['latitude'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precip'][:]
        print(ppt.shape)
        ppt_units = fh.variables['precip'].units
        
        calculateTotalPrcpt(ppt) # total precipitation in a day
        if count == 12:
            break
        
        


# calculateMeanPrecipitation()

print(total_prcpt_in_the_year)
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)

x, y = np.meshgrid(lons, lats)

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
cbar.set_label(ppt_units)

plt.pyplot.title('Total precipitation in the year 2019')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.pyplot.show()


