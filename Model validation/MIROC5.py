import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import interp2d

count = 0
total_precipitation = {
    'chirps' : np.zeros([53,113]),
    'model' : np.zeros([10,21])
                      }
mean_precipitation =  {
    'chirps' : np.zeros([53,113]),
    'model' : np.zeros([10,21])
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
    

        print(totalDaysInChirps)



calculateMeanPrcpt('chirps', totalDaysInChirps)
        
print(totalDaysInChirps) 




model = 'CMIP5/0Major 4/MIROC5/historical/'

with os.scandir(model) as data_files:
    for file in data_files:
        # count = count + 1
        fh = Dataset(model + file.name, mode='r')
        print(file.name)
        lons = np.add(fh.variables['lon'][:], -180)
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][:]
        ppt_units = fh.variables['pr'].units
        
#         print(fh.variables)
        print(len(time))

              
        leftLon = np.where(lons == 71.71875)[0][0]
        rightLon = np.where(lons == 101.25)[0][0]
        bottomLat = np.where(lats == 24.513420897062915)[0][0]
        topLat = np.where(lats == 38.52105552662436)[0][0]
   
        
        days = 9125
        
        print(ppt.shape)
        
        if(file.name == 'pr_day_MIROC5_historical_r1i1p1_19800101-19891231.nc'):
            ppt = ppt[365:]
            print(ppt.shape)
        
        if(file.name == 'pr_day_MIROC5_historical_r1i1p1_20000101-20091231.nc'):
            ppt = ppt[:2190]
            print(ppt.shape)
        
        for matrix in ppt:
            
            matrix = matrix[bottomLat:topLat,leftLon:rightLon]*24*60*60
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
cs = map.pcolor(newx, newy, difference, cmap='seismic', shading='auto', vmin= -20, vmax=20)


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

plt.title('Model Validation - MIROC5')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.show()

