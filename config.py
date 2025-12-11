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

# B. Source Statique (Infrastructure Aérienne - OpenFlights)
# Documentation : https://openflights.org/data
# Note : On utilise les fichiers bruts (Raw) depuis GitHub
AIRPORTS_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
ROUTES_URL = "https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat"

# --- 3. Noms des Fichiers (Stockage) ---
# Fichiers Bruts (Raw)
TRAFFIC_RAW_FILE = os.path.join(RAW_DIR, "traffic_raw.csv")
AIRPORTS_RAW_FILE = os.path.join(RAW_DIR, "airports_raw.csv")
ROUTES_RAW_FILE = os.path.join(RAW_DIR, "routes_raw.csv")

# Fichiers Nettoyés (Cleaned) - Prêts pour le dashboard
AIRPORTS_CLEANED_FILE = os.path.join(CLEANED_DIR, "airports_cleaned.csv")
TRAFFIC_CLEANED_FILE = os.path.join(CLEANED_DIR, "traffic_processed.csv")