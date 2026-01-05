import pandas as pd
import os
import sys

# Permet de trouver le fichier config.py à la racine du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import (
    TRAFFIC_RAW_FILE, AIRPORTS_RAW_FILE, ROUTES_RAW_FILE,
    TRAFFIC_CLEANED_FILE, AIRPORTS_CLEANED_FILE
)

def process_live_traffic():
    """
    Nettoie les données de trafic  (Avions).
    """
    print("Nettoyage du Trafic Aérien...")
    
    if not os.path.exists(TRAFFIC_RAW_FILE):
        print(" Fichier introuvable. Lancer d'abord get_data.py.")
        return

    try:
        df = pd.read_csv(TRAFFIC_RAW_FILE)

        # On ne garde que les avions EN L'AIR
        df = df[ (df['on_ground'] == False) & (df['baro_altitude'].notna()) ].copy()

        df = df.dropna(subset=['latitude', 'longitude'])
        #  Vitesse m/s en km/h
        if 'velocity' in df.columns:
            df['velocity_kmh'] = df['velocity'] * 3.6
        else:
            df['velocity_kmh'] = 0
        """
        # Création de la colonne 'origin_category' 
        # qui nous servira pour donner la couleur entre les avions Francais et internationaux.    
        # fonction de tri des pays (France vs International)
        def trier_pays(x):
            if x == 'France':
                return 'France'     # On garde France
            else:
                return 'International' # Tout le reste devient International

        df['origin_category'] = df['origin_country'].apply(trier_pays)
        """        

        #  On ne garde que les colonnes utiles :
        
        cols_to_keep = [
            'icao24', 'callsign', 'origin_country', 'longitude', 'latitude', 
            'baro_altitude', 'true_track', 'velocity_kmh', 'origin_country'
        ]
        cols_final = [c for c in cols_to_keep if c in df.columns]
        df = df[cols_final]

        df.to_csv(TRAFFIC_CLEANED_FILE, index=False)
        print(f" Il y a {len(df)} avions en vol.")

    except Exception as e:
        print(f"  Erreur nettoyage trafic : {e}")

def process_static_data():
    """
    Fusionne Aéroports et Routes pour calculer la taille des hubs.
    """
    print(" Fusion Aéroports & Routes...")
    
    if not os.path.exists(AIRPORTS_RAW_FILE) or not os.path.exists(ROUTES_RAW_FILE):
        print(" Fichiers RAW introuvables (Airports ou Routes manquants).")
        return

    try:
        
        df_air = pd.read_csv(AIRPORTS_RAW_FILE)
        df_routes = pd.read_csv(ROUTES_RAW_FILE)

        # Nettoyage de base avec dropna() on ne garde que les aéroports avec Latitude, Longitude et IATA valides
        df_air = df_air.dropna(subset=['Latitude', 'Longitude', 'IATA'])
        
        # Compté le nombre de routes par aéroport
        route_counts = df_routes['Source Airport'].value_counts().reset_index() #reset_index pour transformer en une nouvelle DataFrame
        route_counts.columns = ['IATA', 'Route_Count']
        route_counts['Route_Count'] = route_counts['Route_Count']

        # fusion des données d'aéroports avec le nombre de routes dans une nouvelle dataframe
        df_merged = pd.merge(df_air, route_counts, on='IATA', how='left')
        df_merged['Route_Count'] = df_merged['Route_Count'].fillna(0)# Remplacer NaN par 0 

        # on garde les aéroports avec au moins 5 routes 
        df_final = df_merged.query("Route_Count >= 5 ").copy()

        # Sauvegarde
        df_final.to_csv(AIRPORTS_CLEANED_FILE, index=False)
        print(f" Aéroports traités : {len(df_final)} lignes.")

    except Exception as e:
        print(f" Erreur traitement aéroports : {e}")

def load_data(dataset="traffic"):
    """
    Charge les données PROPRES pour le dashboard
    et convertit les colonnes en Entiers de manière robuste.
    """
    if dataset == "traffic":
        path = TRAFFIC_CLEANED_FILE
        # Liste des colonnes qu'on veut ABSOLUMENT en int
        int_cols = ['baro_altitude', 'velocity_kmh']
    
    elif dataset == "airports":
        path = AIRPORTS_CLEANED_FILE
        int_cols = ['Route_Count']
    
    else:
        return None

    if os.path.exists(path):
        # 1. On lit SANS forcer les types (pour éviter le crash immédiat)
        df = pd.read_csv(path)

        # 2. On convertit proprement chaque colonne
        for col in int_cols:
            if col in df.columns:
                # 'coerce' transforme les erreurs (textes, bugs) en NaN
                # round() gère les cas où on aurait 850.9 pour en faire 851
                df[col] = pd.to_numeric(df[col], errors='coerce').round().astype('Int64')

        return df
    else:
        print(f" Fichier {path} introuvable. ")
        return pd.DataFrame()

