import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium import plugins
import numpy
import requests
import geopandas as gpd
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import descartes
from shapely.geometry import Point, Polygon


b19 = pd.read_csv(r'/home/mateus/Documentos/reportagens/acidentes/datatran2019.csv', sep = ';' , encoding = 'latin-1')
b20 = pd.read_csv(r'/home/mateus/Documentos/reportagens/acidentes/datatran2020.csv', sep = ';' , encoding = 'latin-1')
malharn = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/rn_municipios/rn_municipios_2019.geojson')
rodovias = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/rn_municipios/export.geojson')

mbr101 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br101.geojson')
mbr304 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br304.geojson')
mbr406 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br406.geojson')
mbr226 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br226.geojson')
mbr405 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br405.geojson')
mbr427 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br427.geojson')
mbr110 = gpd.read_file(r'/home/mateus/Documentos/reportagens/acidentes/layers/br110.geojson')

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
malharn.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='grey', color='white')

mbr101.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='blue')
mbr304.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='green')
mbr406.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='black')
mbr226.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='orange')
mbr405.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='yellow')
mbr427.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='pink')
mbr110.plot(legend=True, ax=ax,
            legend_kwds=leg, edgecolor='purple')

blue = mpatches.Patch(color='blue',label = "BR-101")
green = mpatches.Patch(color='green',label = "BR-304")
black = mpatches.Patch(color='black',label = "BR-406")
orange = mpatches.Patch(color='orange',label = "BR-226")
yellow = mpatches.Patch(color='yellow',label = "BR-405")
pink = mpatches.Patch(color='pink',label = "BR-427")
purple = mpatches.Patch(color='purple',label = "BR-110")
red = mpatches.Patch(color='red',label = "Acidentes")
plt.title("Acidentes de trânsito em Rodovias Federais do Rio Grande do Norte")

#plt.scatter(f.longitude,f.latitude, s=60, c = "red",marker= 'p', edgecolor='grey')

plt.scatter(f.longitude,f.latitude, s=200, c = "red",marker= '.', edgecolor='grey')
#x1,y1 = m(-6.176900, -35.217270)

#plt.ylabel('Latitude', fontsize=13)
#plt.plot(-35.217270,-6.176900,'ok')
#plt.text(-35.217270,-6.176900,' BR 101', fontsize=12)
#plt.grid()
#ax.set_yticklabels([])
ax.set_xticklabels([])
plt.legend(handles=[blue,green,black,orange,yellow,pink,purple,red])
plt.gca().axes.get_yaxis().set_visible(False)
#plt.gca().axes.get_xaxis().set_visible(False)
plt.xlabel('Fonte: Polícia Rodoviária Federal - 2020', fontsize=13)
plt.show()
