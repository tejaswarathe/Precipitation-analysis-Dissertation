import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d

count = 0
total_precipitation = {
    'chirps' : np.zeros([53,113]),
    'model' : np.zeros([6,11])
                      }
mean_precipitation =  {
    'chirps' : np.zeros([53,113]),
    'model' : np.zeros([6,11])
                      }

newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

def calculateTotalPrcpt(matrix, model):
    global total_precipitation
    total_precipitation[model] = np.add(matrix, total_precipitation[model])


def calculateMeanPrcpt(model, days):
    global mean_precipitation, total_precipitation
    mean_precipitation[model] = np.true_divide(total_precipitation[model], days)
       


chirps = 'chirps data/Annual/'

totalDaysInChirps = 0

with os.scandir(chirps) as data_files:
    for file in data_files:
        fh = Dataset(chirps + file.name, mode='r')
#         print(fh.variables)
        lons = fh.variables['longitude'][:]
        lats = fh.variables['latitude'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['precip'][:]
        
        ppt_units = fh.variables['precip'].units
        totalDaysInChirps += len(time)
        
        leftLon = np.where(lons == 71.875)[0][0]
        rightLon = np.where(lons == 100.125)[0][0]
        bottomLat = np.where(lats == 24.875)[0][0]
        topLat = np.where(lats == 38.125)[0][0]

        
        for matrix in ppt:
            matrix = matrix[bottomLat:topLat,leftLon:rightLon]
            calculateTotalPrcpt(matrix, 'chirps')
    

#         print(len(time))


calculateMeanPrcpt('chirps', totalDaysInChirps)
        
print(totalDaysInChirps) 





model = 'CMIP5/0Major 4/CanESM2/historical/'

with os.scandir(model) as data_files:
    for file in data_files:
        # count = count + 1
        fh = Dataset(model + file.name, mode='r')
        lons = np.add(fh.variables['lon'][:], -180)
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        ppt_units = fh.variables['pr'].units
        
#         print(fh.variables)
        print(len(time))

              
        leftLon = np.where(lons == 70.3125)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 23.72017643801291)[0][0]
        topLat = np.where(lats == 40.4636506825932)[0][0]
        startTime = 731
        endTime = 9855
        days = 9125
        
        for day in range(startTime, endTime):
            
            matrix = ppt[day][bottomLat:topLat,leftLon:rightLon]*24*60*60
            calculateTotalPrcpt(matrix, 'model')
            
calculateMeanPrcpt('model', days)



oldx = lons[leftLon:rightLon]
oldy = lats[bottomLat:topLat]


# newf = interp2d(oldx, oldy, mean_precipitation['model'], kind='linear')
# newf = interp2d(oldx, oldy, mean_precipitation['model'], kind='cubic')
newf = interp2d(oldx, oldy, mean_precipitation['model'], kind='quintic')

data_new = newf(newx, newy)
print(data_new)
print(data_new.shape)


difference = np.subtract(mean_precipitation['chirps'], data_new)
print(difference)





map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)


# Plot Data
# cs = map.pcolor(oldx, oldy, difference, cmap='seismic', shading='auto')
cs = map.pcolor(newx, newy, difference, cmap='seismic', shading='auto', vmin= -10, vmax=10)


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

plt.title('Model Validation - Can ESM5')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.show()

