from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap

count = 0
total_prcpt_in_the_year = np.zeros([53,113])
mean_prcpt_in_the_year = np.zeros([53,113])

numOfdays = {'preMonsoon': 92,
'monsoon':122,
'postMonsoon': 61,
'winter': 91}

totalDays = 0

def calculateTotalPrcpt(precip):
    global total_prcpt_in_the_year
    for matrix in precip:
        total_prcpt_in_the_year = np.add(matrix, total_prcpt_in_the_year)

def calculateMeanPrecipitation():
    global mean_prcpt_in_the_year, total_prcpt_in_the_year, numOfdays, totalDays
    mean_prcpt_in_the_year = np.true_divide(total_prcpt_in_the_year, totalDays)
    print(mean_prcpt_in_the_year)

with os.scandir('chirps data/Monthly/') as data_files:
    for file in data_files:
        fh = Dataset('chirps data/Monthly/' + file.name, mode='r')
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

        ppt = ppt[:,bottomLat:topLat,leftLon:rightLon]
        totalDays += len(ppt)
        calculateTotalPrcpt(ppt) # total precipitation in a day
       

print(totalDays)

calculateMeanPrecipitation()



print(total_prcpt_in_the_year)
map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85)
# map = Basemap(resolution='l',  llcrnrlon=-180, llcrnrlat=-50, urcrnrlon=180, urcrnrlat=50, lat_0=22.5, lon_0= 85)

lons = lons[leftLon:rightLon]
lats = lats[bottomLat:topLat]
x, y = np.meshgrid(lons, lats)

# Plot Data
cs = map.pcolormesh(lons, lats, total_prcpt_in_the_year, cmap='Blues', shading='auto')

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

plt.pyplot.title('Total precipitation')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
plt.pyplot.show()


np.save('Calculated Data/Chirps_total_ppt_40years.npy', total_prcpt_in_the_year)
np.save('Calculated Data/Chirps_mean_ppt_40years.npy', mean_prcpt_in_the_year)
