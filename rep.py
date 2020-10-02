import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium import plugins
import numpy
import requests
import geopandas as gpd
import time
import matplotlib.pyplot as plt

import descartes
from shapely.geometry import Point, Polygon



b19 = pd.read_csv(r'/home/mateus/Documentos/reportagens/acidentes/datatran2019.csv', sep = ';' , encoding = 'latin-1')
b20 = pd.read_csv(r'/home/mateus/Documentos/reportagens/acidentes/datatran2020.csv', sep = ';' , encoding = 'latin-1')
malharn = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/rn_municipios/rn_municipios_2019.geojson')


b19.drop(b19[b19.uf != "RN"].index, inplace=True)
f = b19

f['data_inversa'] = pd.to_datetime(f['data_inversa'])
f['data_inversa'] = pd.DatetimeIndex(f['data_inversa']).month

f.drop(f[f.data_inversa >= 9].index, inplace=True)



locais = f[["latitude","longitude"]].values.tolist()
m = folium.Map(location=[-5.823167, -36.521897],
    zoom_start=8,
    tiles='Stamen Terrain',
    width='100%',
    height='100%')

MarkerCluster(locations = locais).add_to(m)
folium.GeoJson(malharn.to_json()).add_to(m)
m.save(r'/home/mateus/Documentos/reportagens/acidentes/mapa.html')




leg = {'title': '',
      'loc': 'upper left',
      'bbox_to_anchor':(1.0, 1.0),
      'ncol':1
}

f.drop(f[f.longitude <= -40].index, inplace=True)
f.drop(f[f.longitude >= -30].index, inplace=True)
f.drop(f[f.latitude <= -8].index, inplace=True)
f.drop(f[f.latitude >= -3].index, inplace=True)

fig,ax =plt.subplots(figsize =(10,10))
malharn.plot(legend=True, cmap='binary', ax=ax,
            legend_kwds=leg, edgecolor='grey')
#plt.scatter(f.longitude,f.latitude, s=60, c = "red",marker= 'p', edgecolor='grey')
plt.scatter(f.longitude,f.latitude, s=80, c = "red",marker= '.', edgecolor='grey')

plt.xlabel('Longitude', fontsize=13)
plt.ylabel('Latitude', fontsize=13)
plt.grid()
plt.show()
