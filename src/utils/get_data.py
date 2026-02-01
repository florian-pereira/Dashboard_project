"""
Module de récupération des données externes.

Gère les appels aux APIs et le téléchargement des fichiers sources :
- OpenSky Network : positions des avions en temps réel
- OpenFlights : base de données des aéroports et routes aériennes

Les données brutes sont stockées dans le dossier data/raw/
"""

import urllib.request
import urllib.error
import json
import pandas as pd
import os
import sys

# Pour importer config depuis la racine
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import (
    OPENSKY_URL, TRAFFIC_RAW_FILE, 
    AIRPORTS_RAW_FILE,  AIRPORTS_URL,
    ROUTES_RAW_FILE, ROUTES_URL)

# Chemins des dossiers
raw_path = "data/raw"
cleaned_path = "data/cleaned"

# Je crée les dossiers si ils existent pas
os.makedirs(raw_path, exist_ok=True)
os.makedirs(cleaned_path, exist_ok=True)


# FONCTIONS DE RÉCUPÉRATION DE DONNÉES

def get_live_traffic_data():
    """
    Récupère les avions en temps réel via l'API OpenSky.
    Sauvegarde les données brutes dans 'traffic_raw.csv'.
    """
    
    # Zone géographique (Europe)
    # Ajout des parametres à l'URL
    params = "?lamin=35.00&lomin=-15.00&lamax=72.00&lomax=45.00"
    url = OPENSKY_URL 
    
    try:

        with urllib.request.urlopen(url) as response:
            
            data= response.read()
            data_str = data.decode('utf-8')
            json_data = json.loads(data_str)
            
            # On récupère la liste des avions du JSON
            flights = json_data.get('states', [])
            
            if flights:
                # Noms des colonnes (trouvé dans la doc OpenSky)
                cols = ["icao24", "callsign", "origin_country", "time_position", 
                        "last_contact", "longitude", "latitude", "baro_altitude", 
                        "on_ground", "velocity", "true_track", "vertical_rate", 
                        "sensors", "geo_altitude", "squawk", "spi", "position_source"]
                
  
                df = pd.DataFrame(flights, columns=cols)
                df.to_csv(TRAFFIC_RAW_FILE, index=False)
                print(f" {len(df)} avions récupérés .")
            else:
                print(" aucun avion trouvé.")

    except urllib.error.URLError as e:
        print(f"  Erreur de connexion Internet : {e}")
    except Exception as e:
        print(f"  Erreur inattendue : {e}")

def get_static_AeroportsRoads_data():

    try:
        # J'ai pris les noms de colonnes sur le site OpenFlights
        # AÉROPORTS
        
        cols_airports = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", 
                         "Latitude", "Longitude", "Altitude", "Timezone", "DST", 
                         "Tz", "Type", "Source"]
        df_air = pd.read_csv(AIRPORTS_URL, names=cols_airports, header=None)
        df_air.to_csv(AIRPORTS_RAW_FILE, index=False)
        print(f" Aéroports : {len(df_air)} lignes.")

        # ROUTES
        cols_routes = ["Airline", "Airline ID", "Source Airport", "Source Airport ID", 
                       "Dest Airport", "Dest Airport ID", "Codeshare", "Stops", "Equipment"]
        
        # On télécharge
        df_routes = pd.read_csv(ROUTES_URL, names=cols_routes, header=None)
        
        # On sauvegarde
        df_routes.to_csv(ROUTES_RAW_FILE, index=False)
        print(f" Routes : {len(df_routes)} lignes.")
        
    except Exception as e:
        print(f" Erreur  : {e}")

