import pandas as pd
import os
import sys

# On permet à Python de trouver 'config.py' à la racine
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import TRAFFIC_CLEANED_FILE, AIRPORTS_CLEANED_FILE

def load_traffic_data():
    """
    Charge les données de trafic nettoyées.
    Renvoie un DataFrame vide si le fichier n'existe pas encore.
    """
    if os.path.exists(TRAFFIC_CLEANED_FILE):
        return pd.read_csv(TRAFFIC_CLEANED_FILE)
    else:
        # On renvoie un tableau vide avec les colonnes attendues pour éviter les bugs
        return pd.DataFrame(columns=['latitude', 'longitude', 'callsign', 'baro_altitude'])

def load_airports_data():
    """
    Charge les données d'aéroports nettoyées.
    """
    if os.path.exists(AIRPORTS_CLEANED_FILE):
        return pd.read_csv(AIRPORTS_CLEANED_FILE)
    else:
        return pd.DataFrame()