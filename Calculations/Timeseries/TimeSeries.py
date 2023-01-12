import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

cities = {
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

lons = np.arange(71.875,100.125,.25)
lats = np.arange(24.875,38.125,.25)

years = np.linspace(1981, 2101, 120)

indices = ['PRCPTOT', 'R10mm', 'R20mm', 'R95PTOT', 'R99PTOT']
indices2 = ['Rx1day', 'Rx5day']

for index in indices:
    for k in cities:
        data1 = np.load(r'Calculated Data\historical\\' + index + '_historical.npy')
        data2 = np.load(r'Calculated Data\period1\\' + index + '_period1.npy')
        data3 = np.load(r'Calculated Data\period2\\' + index + '_period2.npy')


        # print(data3.shape)

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




        timeSeries = flatten(data1, data2, data3, find_closest(lats, cities[k][0]), find_closest(lons, cities[k][1]))

        mymodel = np.poly1d(np.polyfit(years, timeSeries, 3))

        # print(timeSeries)
        # print(timeSeries.shape)

        fig, axes = plt.subplots(figsize=(12, 4))

        axes.plot(years, timeSeries, color='tab:blue', label=index)
        axes.plot(years, mymodel(years), color='tab:orange', label='polynomial')


        axes.set(xlabel='Years', ylabel=index,
            title='Change in ' + index + ' in ' + k)
        axes.grid()

        print(k)
        plt.savefig('Plots\Time Series\\' + k + '\\' + index + '_' + k + '.png')
        # plt.show()
    