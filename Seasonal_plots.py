from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap

numOfdays = {'Pre Monsoon': 92,
'Monsoon':122,
'Post Monsoon': 61,
'Winter': 91}

season = 'Winter'

def calculateTotalPrcpt(matrix):
    global total_precipitation
    total_precipitation = np.add(matrix, total_precipitation)

def calculateMeanPrecipitation():
    global mean_precipitation, total_precipitation, numOfdays
    print(numOfdays[season])
    mean_precipitation = np.true_divide(total_precipitation, numOfdays[season])


count = 0
total_precipitation = np.zeros([400,450])
mean_precipitation = np.zeros([400,450])

with os.scandir('season data/' + season + '/') as data_files:
    for file in data_files:
        count = count + 1
        
        fh = Dataset('season data/' + season + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt) 
        

calculateMeanPrecipitation()


fig, axes = plt.subplots(1,2)

# PLOT 1

axes[0].set_title('Total precipitation in ' + season + '(2019-2020)')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation, cmap='gist_rainbow', shading='auto')

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

# PLOT 2
axes[1].set_title('Mean precipitation in ' + season + '(2019-2020)')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85,  ax=axes[1])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, mean_precipitation, cmap='gist_rainbow', shading='auto')

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

# plt.savefig(season + '(2019-2020)')
plt.show()




