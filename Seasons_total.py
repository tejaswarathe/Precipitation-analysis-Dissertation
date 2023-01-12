from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap

numOfdays = {'Pre Monsoon': 92,
'Monsoon':122,
'Post Monsoon': 61,
'Winter': 91}

total_precipitation = {'Pre Monsoon': np.zeros([400,450]),
'Monsoon': np.zeros([400,450]),
'Post Monsoon': np.zeros([400,450]),
'Winter': np.zeros([400,450])}

def calculateTotalPrcpt(matrix, season):
    global total_precipitation
    total_precipitation[season] = np.add(matrix, total_precipitation[season])

fig, axes = plt.subplots(2,2)
minmin = 0
maxmax = 5000

print(axes)

######################## PLOT 1 ##########################
season = 'Pre Monsoon'

with os.scandir('season data/' + season + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('season data/' + season + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, season) 
        

axes[0][0].set_title(season + '(2019-2020)')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0][0])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[season], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)


######################## PLOT 2 ##########################
season = 'Monsoon'

with os.scandir('season data/' + season + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('season data/' + season + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, season) 
        


axes[0][1].set_title(season + '(2019-2020)')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0][1])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[season], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 3 ##########################
season = 'Post Monsoon'

with os.scandir('season data/' + season + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('season data/' + season + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, season) 
        

axes[1][0].set_title(season + '(2019-2020)')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[1][0])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[season], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 4 ##########################
season = 'Winter'

with os.scandir('season data/' + season + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('season data/' + season + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, season) 
        


axes[1][1].set_title(season + '(2019-2020)')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[1][1])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[season], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)




############# Plotting subplots #############
plt.suptitle('Total precipitation')
plt.show()
