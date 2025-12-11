import os

# --- 1. Chemins des Dossiers (Architecture) ---
# On récupère le dossier où se trouve ce fichier (la racine du projet)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# On définit les chemins vers les données
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
CLEANED_DIR = os.path.join(DATA_DIR, "cleaned")

# --- 2. URLs des APIs et Données ---
# API Dynamique (Avions)
OPENSKY_URL = "https://opensky-network.org/api/states/all"

# Fichier Statique (Aéroports du monde - Source: OurAirports)
AIRPORTS_URL = "https://davidmegginson.github.io/ourairports-data/airports.csv"

# --- 3. Noms des Fichiers (Stockage) ---
# Fichiers Bruts (Raw)
TRAFFIC_RAW_FILE = os.path.join(RAW_DIR, "traffic_raw.csv")
AIRPORTS_RAW_FILE = os.path.join(RAW_DIR, "airports_raw.csv")

# Fichiers Nettoyés (Cleaned) - Prêts pour le dashboard
AIRPORTS_CLEANED_FILE = os.path.join(CLEANED_DIR, "airports_cleaned.csv")