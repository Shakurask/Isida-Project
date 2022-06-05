import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import geocoder
import csv
import geoplot
import geopandas
from transliterate import translit

import python_weather
import asyncio
import json
from datetime import date

df = pd.read_csv('C:\\Users\\Vovan\\Downloads\\csv.csv', sep=';', header=0)


def plot_geo_data():
    mp = pd.read_csv('foo.txt', sep=' ', header=0)
    mp = mp[mp['lat'] != "None"].astype(float)
    print(mp.values)

    for c in mp.values:
        print("[" + str(c[0]) + ", " + str(c[1]) + "],")
    print(mp.lon)

    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_cities')
    )

    gdf = geopandas.GeoDataFrame(
        mp, geometry=geopandas.points_from_xy(mp.lon, mp.lat))
    ax = world.plot()
    gdf.plot(ax=ax, color='red')


#plot_geo_data()

print(df.punkt.unique())



def  get_weather_data(d):
    with open('2020.json') as f:
        obj = json.load(f)

    dt = pd.to_datetime(d).date()
    d0 = date(2020, 1, 1)

    delta = dt-d0

    temp = obj["data"]['temperature'][delta.days*48+18]
    if temp == None:
        temp = obj["data"]['temperature'][delta.days*48+19]
    if temp == None:
        temp = obj["data"]['temperature'][delta.days * 48 + 20]
    print(temp)



#for i in range(0,df.values.shape[0]):
#    get_weather_data(df.Столбец1[i])


def write_geo_data():
    fp = open('foo.txt', 'w')

    progress = 16000
    c = 0
    for i in df[["who"]].values:
        c += 1
        query_text = translit(i[0], reversed=True)
        g = geocoder.arcgis(i[0])
        fp.write(str(g.lat) + ' ' + str(g.lng) + "\n")
        print(float(c) / progress)

    fp.close()

def cumvert(f):
    if f == None or f == 'None':
        return 10
    else:
        return float(f)
def calculate_matrix_for_svd():
    fp = open('svd.txt', 'w')
    sbs = df[["age", "temperature", "lat", "lon"]]
    last_day = sbs.values[0].astype(float)[0] * 100000
    count = 0
    result = np.zeros((4, 4))
    test0 = np.zeros((1))
    test1 = np.zeros((1))
    test2 = np.zeros((1))
    test3 = np.zeros((1))
    sbs['temperature'] = pd.to_numeric(df['temperature'],errors='coerce')
    sbs['age'] = pd.to_numeric(df['age'], errors='coerce')
    sbs['lat'] = pd.to_numeric(df['lat'], errors='coerce')
    sbs['lon'] = pd.to_numeric(df['lon'], errors='coerce')
    for i in range(1, sbs.values.shape[0]):

        n = sbs.astype(float).values[i].reshape((1, 4))
        res = np.multiply(n, n.T)
        np.fill_diagonal(res, 0)
        result += res
        count = count + 1;
        if n[0][0] * 100000 - last_day < 3:

            count = 0
            last_day = n[0][0] * 100000
        else:
            result = np.divide(result, count)

            test0 = np.append(test0, np.log10(result[0][0]))
            test1 = np.append(test1, np.log10(result[0][1]))
            test2 = np.append(test2, np.log10(result[0][2]))
            test3 = np.append(test3, np.log10(result[0][3]))

            fp.write(str(np.log10(result[0][1]))+',' + str(np.log10(result[0][2]))+',' + str(np.log10(result[0][3])) + '\n')
            # plt.matshow(result)
            # plt.colorbar()
            # plt.show()
            result = 0
    plt.plot(test0)
    plt.plot(test1)
    plt.plot(test2)
    plt.plot(test3)
    plt.show()
    fp.close()
calculate_matrix_for_svd()
