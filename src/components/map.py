import folium, branca 
import pandas as pd
import os
import sys
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import (
    AIRPORTS_CLEANED_FILE,
    TRAFFIC_CLEANED_FILE
    )

#Lecture du fichier csv dans une dataframe
df_airports = pd.read_csv(AIRPORTS_CLEANED_FILE)

LATS_PORTS = df_airports["Latitude"]

LONGS_PORTS = df_airports["Longitude"]

ROUTES = df_airports["Route_Count"]

NAME_PORTS = df_airports["Name"]

coords = (46.539758, 2.430331)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

fg_airports = folium.FeatureGroup(name="Aéroports")

for lat,lng,size,name in zip(LATS_PORTS,LONGS_PORTS,ROUTES,NAME_PORTS):
    folium.CircleMarker(
        location = [lat,lng],
        radius = math.sqrt(size)*0.5,
        color = 'crimson',
        fill = True,
        fill_color = 'crimson',
        tooltip = name,
        popup = "{} routes".format(size)
    ).add_to(fg_airports)

fg_airports.add_to(map)

#Avions

df_plane = pd.read_csv(TRAFFIC_CLEANED_FILE)

LATS_PLANE = df_plane["latitude"]

LONGS_PLANE = df_plane["longitude"]

fg_planes = folium.FeatureGroup(name="Avions en vol")

for lat,lng in zip(LATS_PLANE,LONGS_PLANE):
    icone_avion = folium.Icon(color='red', icon_color='white', icon='plane', prefix='fa')
    folium.Marker(
        location = [lat,lng],
        icon = icone_avion,
    ).add_to(fg_planes)

fg_planes.add_to(map)

folium.LayerControl().add_to(map)

map.save(outfile='aeroports_plane.html')



