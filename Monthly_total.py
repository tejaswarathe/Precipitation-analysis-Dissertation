from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap

numOfdays = {'January': 31,
'February':28,
'March': 31,
'April': 30,
'May': 31,
'June':30,
'July': 31,
'August': 31,
'September': 30,
'October':31,
'November': 30,
'December': 31}

total_precipitation = {
'January': np.zeros([400,450]),
'February':np.zeros([400,450]),
'March': np.zeros([400,450]),
'April': np.zeros([400,450]),
'May': np.zeros([400,450]),
'June':np.zeros([400,450]),
'July': np.zeros([400,450]),
'August': np.zeros([400,450]),
'September': np.zeros([400,450]),
'October': np.zeros([400,450]),
'November': np.zeros([400,450]),
'December': np.zeros([400,450])}


def calculateTotalPrcpt(matrix, month):
    global total_precipitation
    total_precipitation[month] = np.add(matrix, total_precipitation[month])

fig, axes = plt.subplots(3,4)

minmin = 0
maxmax = 2000


######################## PLOT 1 ##########################
month = 'January'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        

axes[0][0].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0][0])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)


######################## PLOT 2 ##########################
month = 'February'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[0][1].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0][1])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 3 ##########################
month = 'March'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        

axes[0][2].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0][2])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 4 ##########################
month = 'April'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[0][3].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[0][3])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 5 ##########################
month = 'May'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[1][0].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[1][0])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 6 ##########################
month = 'June'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[1][1].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[1][1])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 7 ##########################
month = 'July'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[1][2].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[1][2])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 8 ##########################
month = 'August'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[1][3].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[1][3])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 9 ##########################
month = 'September'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[2][0].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[2][0])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 10 ##########################
month = 'October'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[2][1].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[2][1])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 11 ##########################
month = 'November'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[2][2].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[2][2])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)

######################## PLOT 12 ##########################
month = 'December'

with os.scandir('Monthly Data/' + month + '/') as data_files:
    for file in data_files:
        
        fh = Dataset('Monthly Data/' + month + '/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precipitationCal'][0,:]
        ppt_units = fh.variables['precipitationCal'].units
        
        calculateTotalPrcpt(ppt, month) 
        


axes[2][3].set_title(month + '2019')
map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85, ax=axes[2][3])

x, y = np.meshgrid(lats, lons)

# Plot Data
cs = map.pcolor(y, x, total_precipitation[month], cmap='gist_rainbow', shading='auto', vmin=minmin, vmax=maxmax)

map.drawcoastlines()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(ppt_units)





############# Plotting subplots #############
plt.suptitle('Total precipitation')
plt.show()
