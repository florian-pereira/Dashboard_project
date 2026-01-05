import folium, branca 
import pandas as pd
import os
import sys
import math

# Ajout du dossier racine au chemin système pour pouvoir importer les modules du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import de la fonction personnalisée pour charger les données nettoyées
from src.utils.clean_data import load_data

def create_map_airports_plane():
    """
    Génère une carte HTML avec les aéroports (points fixes) 
    et les avions orientés selon leur cap.
    """
    # --- PREPARATION ET CHARGEMENT DES DONNEES AEROPORTS ---
    # Lecture du fichier csv des aéroports dans une dataframe
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
    map = folium.Map(location=coords, tiles='Cartodb dark_matter', zoom_start=6)

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

    # Extraction des colonnes nécessaires pour la boucle
    LATS_PLANE = df_plane["latitude"]
    LONGS_PLANE = df_plane["longitude"]
    ANGLE_AVION = df_plane["true_track"]    # Cap de l'avion (0-360°)


    CALLSIGNS = df_plane["callsign"]
    VITESSE = df_plane["velocity_kmh"]
    PAYS = df_plane["origin_country"]
    ALTITUDE = df_plane["baro_altitude"]

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



        content_icone = f"""
            <div style="transform: rotate({angle}deg);">
                <img src="avion_icone.png" style="width:30px; height:30px;">
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
            popup=content_html,
            tooltip=f"Vol {callsign}"
        ).add_to(fg_planes)

    # Ajout du groupe d'avions à la carte principale
    fg_planes.add_to(map)

    # --- FINALISATION ET SAUVEGARDE ---
    # Ajout du panneau de contrôle pour activer/désactiver les couches
    folium.LayerControl().add_to(map)

    # Sauvegarde du fichier HTML final
    map.save(outfile='aeroports_plane.html')

if __name__ == "__main__":
    # Exécution de la fonction si le script est lancé directement
    create_map_airports_plane()
