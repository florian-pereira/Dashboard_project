import urllib.request
import urllib.error
import json
import pandas as pd
import os
import sys

# Permet de remonter à la racine pour trouver 'config.py'

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import (
    OPENSKY_URL, TRAFFIC_RAW_FILE, 
    AIRPORTS_RAW_FILE,  AIRPORTS_URL,
    ROUTES_RAW_FILE, ROUTES_URL)


# FONCTIONS DE RÉCUPÉRATION DE DONNÉES

def get_live_traffic_data():
    """
    Récupère les avions en temps réel via l'API OpenSky.
    Sauvegarde les données brutes dans 'traffic_raw.csv'.
    """
    print("[Connexion à OpenSky pour récupérer les données de trafic aérien...")
    
    # Paramètres pour cibler la l'Europe
    # l'API OpenSky demande des paramètres dans l'URL
    params = "?lamin=35.00&lomin=-15.00&lamax=72.00&lomax=45.00"
    url = OPENSKY_URL 
    
    try:

        with urllib.request.urlopen(url) as response:
            
            data= response.read()
            data_str = data.decode('utf-8')
            json_data = json.loads(data_str)
            
            # Extraction de la liste des avions
            flights = json_data.get('states', [])
            
            if flights:
                # On définit les colonnes selon la doc OpenSky: https://openskynetwork.github.io/opensky-api/rest.html
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

    print(" Téléchargement OpenFlights...")
    try:
        #Documentation : https://openflights.org/data pour les noms des colonnes (aireports et routes)
        # ---  AÉROPORTS ---
        
        cols_airports = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", 
                         "Latitude", "Longitude", "Altitude", "Timezone", "DST", 
                         "Tz", "Type", "Source"]
        df_air = pd.read_csv(AIRPORTS_URL, names=cols_airports, header=None)
        df_air.to_csv(AIRPORTS_RAW_FILE, index=False)
        print(f" Aéroports : {len(df_air)} lignes.")

        # ---  ROUTES ---
        cols_routes = ["Airline", "Airline ID", "Source Airport", "Source Airport ID", 
                       "Dest Airport", "Dest Airport ID", "Codeshare", "Stops", "Equipment"]
        
        # On télécharge
        df_routes = pd.read_csv(ROUTES_URL, names=cols_routes, header=None)
        
        # On sauvegarde
        df_routes.to_csv(ROUTES_RAW_FILE, index=False)
        print(f" Routes : {len(df_routes)} lignes.")
        
    except Exception as e:
        print(f" Erreur statique : {e}")

#Test de la fonction
if __name__ == "__main__":
    get_live_traffic_data()
    get_static_AeroportsRoads_data()
