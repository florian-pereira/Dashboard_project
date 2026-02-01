
import folium, branca 
import pandas as pd
import os
import sys
import math
from dash import html

# Ajout du dossier racine au chemin système pour pouvoir importer les modules du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import de la fonction personnalisée pour charger les données nettoyées
from src.utils.clean_data import load_data

def render():
    """
    Génère la carte et la retourne sous forme de composant Dash.
    """

    #Lecture du fichier csv dans une dataframe
    df_airports = load_data("airports")

    # Extraction des colonnes nécessaires pour la boucle
    LATS_PORTS = df_airports["Latitude"]
    LONGS_PORTS = df_airports["Longitude"]
    ROUTES = df_airports["Route_Count"]
    NAME_PORTS = df_airports["Name"]

    # --- CREATION DE LA CARTE ---
    # Initialisation des coordonnées, centrées sur la France
    coords = (46.539758, 2.430331)

    # Création de la carte avec un fond sombre (Dark Matter)
    map = folium.Map(location=coords, 
                    tiles='Cartodb dark_matter', 
                    zoom_start=6, 
                    min_zoom=2, 
                    max_bounds=True)

    df_pollution = pd.read_csv("data/cleaned/annual-co-emissions-from-aviation.csv")
    df_pollution_2024 = df_pollution.query("Year == 2024")

    folium.Choropleth(
        geo_data = "data/geo/continents.json",
        name = "Polution Atmosphérique",
        data = df_pollution_2024,
        columns = ["Entity","Total annual CO₂ emissions from aviation"],
        key_on = "feature.properties.CONTINENT",
        fill_color="YlOrRd",              # Yellow -> Orange -> Red (Plus c'est haut, plus c'est rouge)
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Pollution (tonnes CO2)",
        highlight=True,
    ).add_to(map)

    # --- AJOUT DE LA COUCHE AEROPORTS ---
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

    # Ajout du groupe d'aéroports à la carte principale
    fg_airports.add_to(map)

    # --- PREPARATION ET CHARGEMENT DES DONNEES DES AVIONS ---
    # Lecture du fichier csv des avions dans une dataframe
    df_plane = load_data("traffic")
    df_plane_france = df_plane.query("origin_country == 'France'")

    # Extraction des colonnes nécessaires pour la boucle
    LATS_PLANE = df_plane_france["latitude"]
    LONGS_PLANE = df_plane_france["longitude"]
    ANGLE_AVION = df_plane_france["true_track"]    # Cap de l'avion (0-360°)
    CALLSIGNS = df_plane_france["callsign"]
    VITESSE = df_plane_france["velocity_kmh"]
    PAYS = df_plane_france["origin_country"]
    ALTITUDE = df_plane_france["baro_altitude"]

    # --- AJOUT DE LA COUCHE AVIONS ---  
    fg_planes = folium.FeatureGroup(name="Avions en vol")

    for lat,lng,angle,callsign,vit,pays,alt in zip(LATS_PLANE,LONGS_PLANE,ANGLE_AVION,CALLSIGNS, VITESSE, PAYS, ALTITUDE):

        # Création du HTML pour l'icône : on utilise CSS pour la rotation
        content_html = f"""
        <div style="
            font-family: 'Helvetica Neue', Arial, Helvetica, sans-serif;
            width: 200px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            ">
            
            <div style="
                background-color: #2c3e50; 
                color: white; 
                padding: 10px; 
                text-align: center;
                font-weight: bold;
                border-bottom: 3px solid #e74c3c;">
                ✈️ VOL {callsign}
            </div>
            
            <div style="padding: 15px; color: #333; font-size: 13px;">
                <p style="margin: 5px 0;"><b>🌍 Pays :</b> {pays}</p>
                <p style="margin: 5px 0;"><b>💨 Vitesse :</b> {int(vit)} km/h</p>
                <p style="margin: 5px 0;"><b>🏔️ Altitude :</b> {int(alt)} m</p>
                <p style="margin: 5px 0;"><b>🧭 Cap :</b> {int(angle)}°</p>
            </div>
        </div>
        """

        # On crée l'objet Popup (iframe=False est important pour que le style passe bien)
        popup_objet = folium.Popup(content_html, max_width=250)


        # On indique au html la rotation de l'image de l'avion en fonction de la direction réelle de l'avion
        content_icone = f"""
            <div style="transform: rotate({angle}deg);">
                <img src="/assets/avion_icone.png" style="width:30px; height:30px;">
            </div>
        """

        # Utilisation de DivIcon pour insérer notre HTML personnalisé
        icone_avion = folium.DivIcon(
            icon_size = (35,35),
            icon_anchor = (15,15), # Point de pivot au centre de l'image pour une rotation correcte
            html = content_icone,
        )

        # Création du marqueur avion
        folium.Marker(
            location = [lat,lng],
            icon = icone_avion,
            popup=popup_objet,
            tooltip=f"Vol {callsign}"
        ).add_to(fg_planes)

    # Ajout du groupe d'avions à la carte principale
    fg_planes.add_to(map)

    # --- FINALISATION ET SAUVEGARDE ---
    # Ajout du panneau de contrôle pour activer/désactiver les couches
    folium.LayerControl().add_to(map)

    map_html = map.get_root().render()

    # On retourne une Iframe qui contient le HTML de la map
    return html.Div([
    html.Iframe(
        srcDoc=map_html,
        style={
            'width': '100%', 
            'height': '600px', 
            'border': 'none',
            'borderRadius': '15px'  # <--- ARRONDIS SUR L'IFRAME
        }
    )
], style={
    'width': '100%', 
    'borderRadius': '15px',     # <--- ARRONDIS SUR LE CADRE
    'overflow': 'hidden',       # <--- INDISPENSABLE pour couper les coins
    'boxShadow': '0 4px 20px rgba(0,0,0,0.5)'
})

