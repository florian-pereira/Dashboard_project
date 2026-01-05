import time
import sys
import os

# Ajout du dossier src au chemin pour les imports
sys.path.append(os.path.abspath("src"))

# 1. Import de la récupération (get_data.py)
from src.utils.get_data import get_live_traffic_data

# 2. Import du nettoyage (clean_data.py)
from src.utils.clean_data import process_live_traffic

# 3. Import de la carte (map.py)
from src.components.map import create_map_airports_plane

def start_dashboard_loop():
    print("🚀 Démarrage du Dashboard Live...")
    print("ℹ️  Appuyez sur Ctrl+C pour arrêter le programme.\n")
    
    while True:
        try:
            # --- ÉTAPE 1 : RÉCUPÉRATION ---
            print("📡 1. Téléchargement des données OpenSky...")
            get_live_traffic_data() 
            # Cela crée/écrase 'data/raw/traffic_raw.csv'
            
            # --- ÉTAPE 2 : TRAITEMENT ---
            print("🧹 2. Nettoyage des données...")
            process_live_traffic()
            # Cela lit 'traffic_raw.csv' et crée 'data/cleaned/traffic_processed.csv'
            
            # --- ÉTAPE 3 : VISUALISATION ---
            print("🗺️  3. Génération de la carte HTML...")
            create_map_airports_plane()
            # Cela lit 'traffic_processed.csv' et crée 'aeroports_plane.html' avec le refresh auto
            
            print("✅ Cycle terminé. Mise à jour dans 10 secondes.\n")
            
            # --- PAUSE ---
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n🛑 Arrêt du programme.")
            break
        except Exception as e:
            print(f"⚠️ Erreur inattendue : {e}")
            time.sleep(5) # On attend un peu avant de retenter en cas d'erreur

if __name__ == "__main__":
    start_dashboard_loop()