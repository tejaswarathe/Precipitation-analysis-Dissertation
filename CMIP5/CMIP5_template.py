from netCDF4 import Dataset
import numpy as np
import matplotlib as plt
import os
from mpl_toolkits.basemap import Basemap

count = 0
total_prcpt_in_the_year = np.zeros([400,450])
mean_prcpt_in_the_year = np.zeros([400,450])

numOfdays = {'preMonsoon': 92,
'monsoon':122,
'postMonsoon': 61,
'winter': 91}

def calculateTotalPrcpt(matrix):
    global total_prcpt_in_the_year
    total_prcpt_in_the_year = np.add(matrix, total_prcpt_in_the_year)

def calculateMeanPrecipitation():
    global mean_prcpt_in_the_year, total_prcpt_in_the_year, numOfdays
    mean_prcpt_in_the_year = np.true_divide(total_prcpt_in_the_year, 365)
    print(mean_prcpt_in_the_year)

with os.scandir('CMIP5/CanESM2/') as data_files:
    for file in data_files:
        count = count + 1
        fh = Dataset('CMIP5/CanESM2/' + file.name, mode='r')
        lons = fh.variables['lon'][:]
        lats = fh.variables['lat'][:]
        time = fh.variables['time'][:]
        ppt = fh.variables['pr'][0,:]
        ppt_units = fh.variables['pr'].units
        # print(lats)
        # print(lons)
        # print(time)
        # print(fh.variables)
        # print(ppt)
        # print(total_prcpt_in_the_year)
        # calculateTotalPrcpt(ppt) # total precipitation in a day
        # if(count ==2):
        #     break
        
        


# calculateMeanPrecipitation()

# # print(total_prcpt_in_the_year)
# map = Basemap(resolution='l', llcrnrlon=65, llcrnrlat=0, urcrnrlon=105, urcrnrlat=45, lat_0=22.5, lon_0= 85)

# x, y = np.meshgrid(lats, lons)

# # Plot Data
# cs = map.pcolor(y, x, mean_prcpt_in_the_year, cmap='gist_rainbow', shading='auto')

# map.drawcoastlines()
# map.drawcountries()

# # Add Colorbar
# cbar = map.colorbar(cs, location='bottom', pad="10%")
# cbar.set_label(ppt_units)

# plt.pyplot.title('Mean precipitation in the year 2019')
# plt.pyplot.savefig('mean_ppt_in_winter(2019-2020)')
# plt.pyplot.show()
