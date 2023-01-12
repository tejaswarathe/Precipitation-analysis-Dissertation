from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d



count = 0

cdd_matrix = {'historical': np.zeros([53,113]),
'period1': np.zeros([10,21]),
'period2': np.zeros([10,21])
}

current_cdd_matrix = {'historical': np.zeros([53,113]),
'period1': np.zeros([10,21]),
'period2': np.zeros([10,21])
}

historical = 'chirps data/Annual/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'


newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)


difference = {'first': np.zeros([53,113]),
'second': np.zeros([53,113]),
}

# Lon: 72 -100
# Lat: 25 - 38

model = 'MIROC5'


def calculateCDD(precip, time_period):
    global cdd_matrix
    for i in range(bottomLat, topLat):
        for j in range(leftLon, rightLon):
            if(matrix[i][j]*24 < 1):
                current_cdd_matrix[time_period][i-bottomLat][j-leftLon] += 1
            else:  
                cdd_matrix[time_period][i-bottomLat][j-leftLon] = max(current_cdd_matrix[time_period][i-bottomLat][j-leftLon], cdd_matrix[time_period][i-bottomLat][j-leftLon])
                current_cdd_matrix[time_period][i-bottomLat][j-leftLon] = 0
            cdd_matrix[time_period][i-bottomLat][j-leftLon] = max(current_cdd_matrix[time_period][i-bottomLat][j-leftLon], cdd_matrix[time_period][i-bottomLat][j-leftLon])


fig, axes = plt.subplots(1,3)
minmin = 0
maxmax = 125

print(axes)

################### Historical Plot #########################
time_period = 'historical'
data = historical

with os.scandir(data) as data_files:
    for file in data_files:
        fh = Dataset(data + file.name, mode='r')
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

        for matrix in ppt:
            calculateCDD(matrix, time_period)
  
       

print(cdd_matrix)


# save to npy file
np.save('cdd_historical.npy', cdd_matrix[time_period])


axes[0].set_title('Historical Data - CHIRPS (1981-2020)')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[0])

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, cdd_matrix[time_period], cmap='jet', shading='auto', vmin=minmin, vmax=maxmax)
map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')


# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('days')


################### Future Plot (Period 1) #########################
time_period = 'period1'
data = period1

with os.scandir(data) as data_files:
    for file in data_files:
        fh = Dataset(data + file.name, mode='r')
        count = count + 1
        # print(fh.variables)
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        # print(ppt.shape)
        ppt_units = fh.variables['pr'].units


# Change this according to model
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 38.52105552662436)[0][0]


        for matrix in ppt:
            matrix = matrix*24*60*60
            calculateCDD(matrix, time_period)

            #period break
            # if (count==17337):
            #     break
    

        break

print(cdd_matrix)

oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]

newf = interp2d(oldx, oldy, cdd_matrix[time_period], kind='quintic')

difference['first'] = newf(newx, newy)


axes[1].set_title('Future Data - ' + model + ' (2021-2060)')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[1])

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(newx, newy, difference['first'], cmap='seismic', shading='auto')
map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')


# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('days')


################### Future Plot (Period 2) #########################
time_period = 'period2'
data = period2

with os.scandir(data) as data_files:
    for file in data_files:
        fh = Dataset(data + file.name, mode='r')
        count = count + 1
        # print(fh.variables)
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        # print(ppt.shape)
        ppt_units = fh.variables['pr'].units

# Change this according to model
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 38.52105552662436)[0][0]
    

        for matrix in ppt:
            matrix = matrix*24*60*60
            calculateCDD(matrix, time_period)
            
            #period break
            # if (count==17337):
            #     break
        break


print(cdd_matrix)

oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]

newf = interp2d(oldx, oldy, cdd_matrix[time_period], kind='quintic')

difference['second'] = newf(newx, newy)

axes[2].set_title('Future Data - ' + model + ' (2061-2100)')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[2])

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(newx, newy, difference['second'], cmap='seismic', shading='auto')
map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')


# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('days')






# plotting
plt.suptitle('Consecutive Dry Days')
plt.show()