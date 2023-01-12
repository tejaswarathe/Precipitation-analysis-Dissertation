import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


###### lat longs to plot #############
lats = [34.097754, 34.164203, 32.718561, 31.104153, 31.708595, 30.316496, 30.086927, 29.945690, 27.338936, 27.084368]
lons = [74.814425, 77.584813, 74.858092, 77.170973, 76.932037, 78.032188, 78.267609, 78.164246, 88.606506, 93.605316]


newx = np.arange(71.875,100.125,.25)
newy = np.arange(24.875,38.125,.25)

cM = plt.cm.get_cmap('seismic')
reversedCM = cM.reversed()

colorM = reversedCM

indices3 = ['CDD']
indices2 = ['SDII']
indices = ['CWD','PRCPTOT', 'R10mm', 'R20mm', 'R95PTOT', 'R99PTOT', 'Rx1day', 'Rx5day']

units = { 'CDD' : 'days',
'CWD': 'days',
'PRCPTOT' : 'mm',
'R10mm' : 'days',
'R20mm' : 'days',
'R95PTOT' : 'mm',
'R99PTOT' : 'mm',
'Rx1day' : 'mm',
'Rx5day' : 'mm',
'SDII' : 'mm'
}

for index in indices2:
    historical = np.load('Calculated Data\historical\\'+ index +'_historical_40years.npy')
    period1 = np.load('Calculated Data\period1\\'+ index +'_period1_40years.npy')
    period2 = np.load('Calculated Data\period2\\'+ index +'_period2_40years.npy')

    print(historical.shape)
    print(period1.shape)
    print(period2.shape)

    fig, axes = plt.subplots(1,2, figsize=(10, 4))
    fig.tight_layout(pad=2.0)



    difference1 = period1-historical

    difference2 = period2-historical

################### Find maximum and minimum values and corresponding latitude and longitude ########################

    print(np.max(difference1))
    print(np.min(difference1))

    print('-------------')

    print(np.max(difference2))
    print(np.min(difference2))
    
    
    max1 = max(abs(np.max(difference1)), abs(np.min(difference1)))
    
    max2 = max(abs(np.max(difference2)), abs(np.min(difference2)))

    minmin = -(max(max1,max2))
    maxmax = max(max1,max2)

    print(minmin)
    print(maxmax)

    ################################
    



    axes[0].set_title('(a) Change in '+ index +' in Period 1 (2021-2060)')
    map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[0])

    # Plot Data
    cs = map.pcolor(newx, newy, difference1, cmap=colorM, shading='auto', vmin=minmin, vmax=maxmax)
    map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
    map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
    map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
    map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
    map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')
    # map.readshapefile('ShapeFiles\Cities\cities2', 'Cities')

    # North Arrow
    x, y = map(97, 37)
    x2, y2 = (97, 34)

    axes[0].annotate('N', xy=(x, y),  xycoords='data',
                    xytext=(x2, y2), textcoords='data',
                    arrowprops=dict(arrowstyle="->")
                    )
    
    
    a, b = map(lons, lats)

    map.scatter(a, b, marker='^',color='g')



    map.drawcountries()

    # Add Colorbar
    cbar = map.colorbar(cs, location='bottom', pad="5%")
    cbar.set_label(units[index])

    ################################



    axes[1].set_title('(b) Change in '+ index +' in Period 2 (2061-2100)')
    map = Basemap(resolution='l', llcrnrlon=72, llcrnrlat=25, urcrnrlon=100, urcrnrlat=38, lat_0=22.5, lon_0= 85, ax=axes[1])

    # Plot Data
    cs = map.pcolor(newx, newy, difference2, cmap=colorM, shading='auto', vmin=minmin, vmax=maxmax)
    map.readshapefile(r'ShapeFiles\Uttarakhand' , 'Uttarakhand')
    map.readshapefile('ShapeFiles\ArunachalPradesh' , 'ArunachalPradesh', default_encoding='ISO-8859-1')
    map.readshapefile('ShapeFiles\HimachalPradesh', 'Himachal_Pradesh')
    map.readshapefile('ShapeFiles\Jammu_state', 'Jammu_state')
    map.readshapefile('ShapeFiles\Sikkim', 'Sikkim')
    # map.readshapefile('ShapeFiles\Cities\cities2', 'Cities')

    # North Arrow
    x, y = map(97, 37)
    x2, y2 = (97, 34)

    axes[1].annotate('N', xy=(x, y),  xycoords='data',
                    xytext=(x2, y2), textcoords='data',
                    arrowprops=dict(arrowstyle="->")
                    )

    
    map.drawcountries()

    a, b = map(lons, lats)

    map.scatter(a, b, marker='^',color='g')

    # Add Colorbar
    cbar = map.colorbar(cs, location='bottom', pad="5%")
    cbar.set_label(units[index])


    # plotting
    # plt.suptitle('Difference in Consecutive Dry Days')
    plt.savefig('Plots\Difference\PPT\\'+ index + '.png')
    
    # plt.show()


