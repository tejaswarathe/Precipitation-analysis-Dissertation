import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)
spikesRemoved = np.zeros([53,113])

indices = ['PRCPTOT', 'R10mm', 'R20mm', 'R95PTOT', 'R99PTOT', 'Rx1day', 'Rx5day']
indices2 = ['CDD', 'CWD', 'SDII']


def removeSpikes(data, sd , mean, factor):
    global spikesRemoved
    for matrix in data:
        maximum = mean + factor*sd
        minimum = mean - factor*sd
        for i in range(53):
            for j in range(113):
                if(matrix[i][j] > maximum[i][j] or matrix[i][j] < minimum[i][j]):
                    spikesRemoved[i][j] += 1
                    matrix[i][j] = mean[i][j]
    return data

for indice in indices2:
    spikesRemoved = np.zeros([53,113])
    indexData = np.load('Calculated Data\period2\\' + indice + '_period2.npy')

    print(indexData.shape)

    mean = np.mean(indexData, axis=0)
    sd = np.std(indexData, axis=0)

    print(mean.shape)

    removedSpikesFac = removeSpikes(indexData, sd, mean, 3)

    meanAfterRemovingSpikes = np.mean(removedSpikesFac, axis=0)

    np.save('Calculated Data\period2\\' + indice + '_period2_noSpikesMean.npy', meanAfterRemovingSpikes)


    fig, axes = plt.subplots(1,3, figsize=(14, 6))


    ################################
    axes[0].set_title('mean')
    map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[0])

    # Plot Data
    cs = map.pcolor(newx, newy, mean, cmap='jet', shading='auto')
    map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
    map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
    map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
    map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
    map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')

    # Add Colorbar
    cbar = map.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label('number')

    ################################
    axes[1].set_title('mean After Removing Spikes')
    map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[1])

    # Plot Data
    cs = map.pcolor(newx, newy, meanAfterRemovingSpikes, cmap='jet', shading='auto')
    map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
    map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
    map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
    map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
    map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')

    # Add Colorbar
    cbar = map.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label('number')

    ################################
    axes[2].set_title('Spikes Removed')
    
    map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[2])

    # Plot Data
    cs = map.pcolor(newx, newy, spikesRemoved, cmap='jet', shading='auto')
    map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
    map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
    map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
    map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
    map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')

    # Add Colorbar
    cbar = map.colorbar(cs, location='bottom', pad="10%")
    cbar.set_label('number')


    # plotting
    plt.suptitle( indice + ' Removed Spikes')
    plt.show()