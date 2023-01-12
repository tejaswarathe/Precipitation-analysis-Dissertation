import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d

count = 0
total_precipitation = {
    '1' : np.zeros([53,113]),
    '2' : np.zeros([265,565])
                      }
mean_precipitation =  {
    '1' : np.zeros([53,113]),
    '2' : np.zeros([265,565])
                      }

fig, axes = plt.subplots(1,3)
numOfdays = 31


period1 = 'Interpolation validation/p05'
period2 = 'Interpolation validation/p25'


oldx = np.arange(71.875,100.125,.25)
oldy = np.arange(24.875,38.125,.25)

newx = np.arange(71.875,100.125,.05)
newy = np.arange(24.875,38.125,.05)

def calculateTotalPrcpt(matrix, period):
    global total_precipitation
    total_precipitation[period] = np.add(matrix, total_precipitation[period])


def calculateMeanPrcpt(period):
    global mean_precipitation, total_precipitation, numOfdays

    mean_precipitation[period] = np.true_divide(total_precipitation[period], numOfdays)


fhp05 = Dataset('Interpolation validation\p5\chirps-v2.0.2019.12.days_p05.nc', mode='r')
fhp25 = Dataset('Interpolation validation\p25\chirps-v2.0.2019.12.days_p25.nc', mode='r')

lons05 = fhp05.variables['longitude'][:]
lats05 = fhp05.variables['latitude'][:]
time05 = fhp05.variables['time'][:]
ppt05 = fhp05.variables['precip'][:]
print(ppt05.shape)
ppt_units05 = fhp05.variables['precip'].units



lons25 = fhp25.variables['longitude'][:]
lats25 = fhp25.variables['latitude'][:]
time25 = fhp25.variables['time'][:]
ppt25 = fhp25.variables['precip'][:]
print(ppt25.shape)
ppt_units25 = fhp25.variables['precip'].units



leftLon05 = np.where(lons05 == 71.875)[0][0]
rightLon05 = np.where(lons05 == 100.125)[0][0]
bottomLat05 = np.where(lats05 == 24.875)[0][0]
topLat05 = np.where(lats05 == 38.125)[0][0]


leftLon25 = np.where(lons25 == 71.875)[0][0]
rightLon25 = np.where(lons25 == 100.125)[0][0]
bottomLat25 = np.where(lats25 == 24.875)[0][0]
topLat25 = np.where(lats25 == 38.125)[0][0]


for matrix in ppt25:
    count = count + 1 
    matrix = matrix[bottomLat25:topLat25,leftLon25:rightLon25]
    calculateTotalPrcpt(matrix, '1')

    
calculateMeanPrcpt('1')
    
for matrix in ppt05:
    count = count + 1 
    matrix = matrix[bottomLat05:topLat05,leftLon05:rightLon05]
    calculateTotalPrcpt(matrix, '2')

calculateMeanPrcpt('2')


print(mean_precipitation['1'])
print(mean_precipitation['1'].shape)


newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='linear')
# newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='cubic')
# newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='quintic')

data_new = newf(newx, newy)
print(data_new)
print(data_new.shape)


difference = np.subtract(mean_precipitation['2'], data_new)
print(difference)


axes[0].set_title('Linear')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[0])


# Plot Data
# cs = map.pcolor(oldx, oldy, difference, cmap='seismic', shading='auto')
cs = map.pcolor(newx, newy, difference, cmap='seismic', shading='auto', vmin= -4, vmax=4)


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


# newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='linear')
newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='cubic')
# newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='quintic')

data_new = newf(newx, newy)
print(data_new)
print(data_new.shape)


difference = np.subtract(mean_precipitation['2'], data_new)
print(difference)


axes[1].set_title('Cubic')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[1])


# Plot Data
# cs = map.pcolor(oldx, oldy, difference, cmap='seismic', shading='auto')
cs = map.pcolor(newx, newy, difference, cmap='seismic', shading='auto', vmin= -4, vmax=4)


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



# newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='linear')
# newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='cubic')
newf = interp2d(oldx, oldy, mean_precipitation['1'], kind='quintic')

data_new = newf(newx, newy)
print(data_new)
print(data_new.shape)


difference = np.subtract(mean_precipitation['2'], data_new)
print(difference)


axes[2].set_title('Quintic')
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[2])


# Plot Data
# cs = map.pcolor(oldx, oldy, difference, cmap='seismic', shading='auto')
cs = map.pcolor(newx, newy, difference, cmap='seismic', shading='auto', vmin= -4, vmax=4)


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



# plotting
plt.suptitle('Difference(Mean PPT) - Interpolation validation')
plt.show()