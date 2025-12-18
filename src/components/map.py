import folium, branca 
import pandas as pd
import os
import sys
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.clean_data import load_data

def create_map_airports_plane():

    #Lecture du fichier csv dans une dataframe
    df_airports = load_data("airports")

    LATS_PORTS = df_airports["Latitude"]

    LONGS_PORTS = df_airports["Longitude"]

    ROUTES = df_airports["Route_Count"]

    NAME_PORTS = df_airports["Name"]

    coords = (46.539758, 2.430331)
    map = folium.Map(location=coords, tiles='cartodb positron', zoom_start=6)

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

    df_plane = load_data("traffic")

    LATS_PLANE = df_plane["latitude"]

    LONGS_PLANE = df_plane["longitude"]

    ANGLE_AVION = df_plane["true_track"]

    fg_planes = folium.FeatureGroup(name="Avions en vol")

    for lat,lng,angle in zip(LATS_PLANE,LONGS_PLANE,ANGLE_AVION):
        content_html = f"""
            <div style="transform: rotate({angle}deg);">
                <img src="avion_icone.png" style="width:30px; height:30px;">
            </div>
        """
        icone_avion = folium.DivIcon(
            icon_size = (35,35),
            icon_anchor = (15,15),
            html = content_html,
        )
        folium.Marker(
            location = [lat,lng],
            icon = icone_avion,
        ).add_to(fg_planes)

    fg_planes.add_to(map)

    folium.LayerControl().add_to(map)

    map.save(outfile='aeroports_plane.html')