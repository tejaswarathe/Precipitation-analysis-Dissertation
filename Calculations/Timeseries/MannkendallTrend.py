import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import pymannkendall as mk

cities = [ 'Srinagar','Leh','Jammu','Shimla','Mandi']
cities2 = ['Dehradun','Rishikesh','Haridwar','Gangtok','Itanagar']

cityLocation = {
'Srinagar' : (34.097754, 74.814425),
'Leh' : (34.164203, 77.584813),
'Jammu' : (32.718561, 74.858092),
'Shimla' : (31.104153, 77.170973),
'Mandi' : (31.708595, 76.932037),
'Dehradun' : (30.316496, 78.032188),
'Rishikesh' : (30.086927, 78.267609),
'Haridwar' : (29.945690, 78.164246),
'Gangtok' : (27.338936, 88.606506),
'Itanagar' : (27.084368, 93.605316)
}
lats = [34.097754, 34.164203, 32.718561, 31.104153, 31.708595, 30.316496, 30.086927, 29.945690, 27.338936, 27.084368]
lons = [74.814425, 77.584813, 74.858092, 77.170973, 76.932037, 78.032188, 78.267609, 78.164246, 88.606506, 93.605316]



lons = np.arange(71.875,100.125,.25)
lats = np.arange(24.875,38.125,.25)

years = np.linspace(1981, 2101, 1440)

indices = ['CDD', 'CWD', 'SDII','PRCPTOT', 'R10mm', 'R20mm', 'R95PTOT', 'R99PTOT']
indices2 = ['Rx1day', 'Rx5day']

fig, axes = plt.subplots(5, 2, figsize=(12, 9))

fig.tight_layout(pad=4.0)

def find_closest(array, value):
    mini = np.abs(array-value)
    index = mini.argmin()
    return index

def flatten(data1, data2, data3, lat, lon):
    arr = []
    for i in range(len(data1)):
        arr.append(data1[i][lat][lon])
    for i in range(len(data2)):
        arr.append(data2[i][lat][lon])
    for i in range(len(data3)):
        arr.append(data3[i][lat][lon])
    return np.asarray(arr)


for index in indices2:
    fig, axes = plt.subplots(5, 2, figsize=(12, 9))
    fig.tight_layout(pad=4.0)

    for k in range(len(cities)):
        data1 = np.load(r'Calculated Data\historical\\' + index + '_historical.npy')
        data2 = np.load(r'Calculated Data\period1\\' + index + '_period1.npy')
        data3 = np.load(r'Calculated Data\period2\\' + index + '_period2.npy')

        cityName = cities[k]

        timeSeries = flatten(data1, data2, data3, find_closest(lats, cityLocation[cityName][0]), find_closest(lons, cityLocation[cityName][1]))

        yue_wang_modification_test = mk.yue_wang_modification_test(timeSeries)
        Sens_slope = mk.sens_slope(timeSeries)
        
        mymodel = np.arange(len(timeSeries)) * yue_wang_modification_test.slope + yue_wang_modification_test.intercept
        # print(mymodel.shape)

        # print(timeSeries)
        # print(timeSeries.shape)

        axes[k][0].set_title('Change in ' + index + ' in ' + cityName)
        axes[k][0].plot(years, timeSeries, color='tab:blue', label=index)
        axes[k][0].plot(years, mymodel, color='tab:orange', label='polynomial')
        # axes[k][0].legend([index, 'Mann Kendall trend'])


        axes[k][0].set(xlabel='Years', ylabel=index)
        axes[k][0].grid()

        # print(k)
        
        # plt.show()
    

    for k in range(len(cities2)):
        data1 = np.load(r'Calculated Data\historical\\' + index + '_historical.npy')
        data2 = np.load(r'Calculated Data\period1\\' + index + '_period1.npy')
        data3 = np.load(r'Calculated Data\period2\\' + index + '_period2.npy')

        cityName = cities2[k]

        timeSeries = flatten(data1, data2, data3, find_closest(lats, cityLocation[cityName][0]), find_closest(lons, cityLocation[cityName][1]))

        yue_wang_modification_test = mk.yue_wang_modification_test(timeSeries)
        Sens_slope = mk.sens_slope(timeSeries)
        
        mymodel = np.arange(len(timeSeries)) * yue_wang_modification_test.slope + yue_wang_modification_test.intercept
        # print(mymodel.shape)

        # print(timeSeries)
        # print(timeSeries.shape)

        axes[k][1].set_title('Change in ' + index + ' in ' + cityName)
        axes[k][1].plot(years, timeSeries, color='tab:blue', label=index)
        axes[k][1].plot(years, mymodel, color='tab:orange', label='polynomial')
        # axes[k][1].legend([index, 'Mann Kendall trend'])


        axes[k][1].set(xlabel='Years', ylabel=index)
        axes[k][1].grid()

        # print(k)
    
        # plt.show()
    # plt.savefig('Plots\Time Series\MannKendall\\' + index + '_total.png')    
     # + '(2)' 