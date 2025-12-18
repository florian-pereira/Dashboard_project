import folium, branca 
import pandas as pd
import os
import sys
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import AIRPORTS_CLEANED_FILE

#Lecture du fichier csv dans une dataframe
df = pd.read_csv(AIRPORTS_CLEANED_FILE)

LATS = df["Latitude"]

LONGS = df["Longitude"]

ROUTES = df["Route_Count"]

NAME_AIRPORTS = df["Name"]

coords = (46.539758, 2.430331)
map = map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=6)

for lat,lng,size,name in zip(LATS,LONGS,ROUTES,NAME_AIRPORTS):
    folium.CircleMarker(
        location = [lat,lng],
        radius = math.sqrt(size)*0.5,
        color = 'crimson',
        fill = True,
        fill_color = 'crimson',
        tooltip = name,
    ).add_to(map)

map.save(outfile='aeroports.html')



