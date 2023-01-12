import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import pymannkendall as mk
import pandas as pd


cities = [ 'Srinagar','Leh','Jammu','Shimla','Mandi','Dehradun','Rishikesh','Haridwar','Gangtok','Itanagar']

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

lons = np.arange(71.875,100.125,.25)
lats = np.arange(24.875,38.125,.25)

years = np.linspace(1981, 2101, 120)

indices = ['CDD', 'CWD', 'SDII','PRCPTOT', 'R10mm', 'R20mm', 'R95PTOT', 'R99PTOT', 'Rx1day', 'Rx5day']



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

dataTosave = []

for index in indices:

    for k in range(len(cities)):
        data1 = np.load(r'Calculated Data\historical\\' + index + '_historical.npy')
        data2 = np.load(r'Calculated Data\period1\\' + index + '_period1.npy')
        data3 = np.load(r'Calculated Data\period2\\' + index + '_period2.npy')

        cityName = cities[k]

        timeSeries = flatten(data1, data2, data3, find_closest(lats, cityLocation[cityName][0]), find_closest(lons, cityLocation[cityName][1]))

        test_result = mk.yue_wang_modification_test(timeSeries)

        # print('---------------')
        # print(cityName)
        # print(index)
        # print(test_result)
        # print('---------------')

        d = [index, cityName, test_result.trend, test_result.z, test_result.s, test_result.slope, test_result.intercept]
        dataTosave.append(d)
        

df = pd.DataFrame(dataTosave)
df.to_csv('Calculated Data/mannKendallData.csv')

print(dataTosave)
