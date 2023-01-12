from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d


count = 0

cwd_matrix = {'historical': np.zeros([53,113]),
'period1': np.zeros([53,113]),
'period2': np.zeros([53,113])
}

current_cwd_matrix = {'historical': np.zeros([53,113]),
'period1': np.zeros([53,113]),
'period2': np.zeros([53,113])
}

historical = 'chirps data/Annual/'
period1 = 'CMIP5/0Major 4/MIROC5/Period 1/'
period2 = 'CMIP5/0Major 4/MIROC5/Period 2/'


newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)


interpolated = {'period1': np.zeros([53,113]),
'period2': np.zeros([53,113]),
}

# Lon: 72 -100
# Lat: 25 - 38
# , vmin=minmin, vmax=maxmax

model = 'MIROC5'

color_map = plt.cm.get_cmap('jet')
reversed_color_map = color_map.reversed()



def calculateCWD(precip, time_period):
    global cwd_matrix
    for i in range(53):
        for j in range(113):
            if(precip[i][j] >= 1):
                current_cwd_matrix[time_period][i][j] += 1
            else:  
                cwd_matrix[time_period][i][j] = max(current_cwd_matrix[time_period][i][j], cwd_matrix[time_period][i][j])
                current_cwd_matrix[time_period][i][j] = 0
            cwd_matrix[time_period][i][j] = max(current_cwd_matrix[time_period][i][j], cwd_matrix[time_period][i][j])


fig, axes = plt.subplots(1,3)
minmin = 0
maxmax = 10000

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
            matrix = matrix[bottomLat:topLat,leftLon:rightLon]
            calculateCWD(matrix, time_period)

       

print(cwd_matrix)


axes[0].set_title('Historical Data - CHIRPS (1981-2020)')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[0])

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, cwd_matrix[time_period], cmap=reversed_color_map, shading='auto')
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
            matrix = matrix*60*60
            calculateCWD(matrix, time_period)

            #period break
            # if (count==17337):
            #     break
    

        break

print(cwd_matrix)


axes[1].set_title('Future Data - ' + model + ' (2021-2060)')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[1])

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, cwd_matrix[time_period], cmap=reversed_color_map, shading='auto')
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
            matrix = matrix*60*60
            calculateCWD(matrix, time_period)
            
            #period break
            # if (count==17337):
            #     break
        break


print(cwd_matrix)


axes[2].set_title('Future Data - ' + model + ' (2061-2100)')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[2])

x, y = np.meshgrid(lons[leftLon:rightLon], lats[bottomLat:topLat])

# Plot Data
cs = map.pcolor(x, y, cwd_matrix[time_period], cmap=reversed_color_map, shading='auto')
map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')


# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('days')






# plotting
plt.suptitle('Consecutive Wet Days')
plt.show()