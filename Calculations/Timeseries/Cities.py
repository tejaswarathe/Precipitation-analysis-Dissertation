import numpy as np
import matplotlib.pyplot as plt


lon = np.arange(71.875,100.125,.25)
lat = np.arange(24.875,38.125,.25)


def find_closest(array, value):
    mini = np.abs(array-value)
    index = mini.argmin()
    return index

Shrinagar = (34.097754, 74.814425)
Leh = (34.164203, 77.584813)
Jammu = (32.718561, 74.858092)

Shimla = (31.104153, 77.170973)
Mandi = (31.708595, 76.932037)

Dehradun = (30.316496, 78.032188)
Rishikesh = (30.086927, 78.267609)
Haridwar = (29.945690, 78.164246)

Gangtok = (27.338936, 88.606506)

Itanagar = (27.084368, 93.605316)


print(find_closest(lat, Shrinagar[0]))
print(find_closest(lon, Shrinagar[1]))
