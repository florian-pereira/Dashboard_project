"""
Point d'entrée principal de l'application Dashboard.

Ce fichier orchestre le lancement du tableau de bord en exécutant
successivement la récupération des données, leur nettoyage,
puis l'initialisation du serveur Dash.

Utilisation : python main.py
Accès : http://127.0.0.1:8050
"""

from dash import Dash
from src.pages.home import layout
from src.utils.get_data import get_live_traffic_data, get_static_AeroportsRoads_data
from src.utils.clean_data import process_live_traffic, load_data, process_static_data

# Récupération traffic
get_live_traffic_data()

# Nettoyage traffic
process_live_traffic()

# Récupération données aéroports
get_static_AeroportsRoads_data()

# Nettoyage données aéroports
process_static_data()


app = Dash(__name__)

# J'appelle la fonction layout
# Si c'était une variable, pas besoin de ()
app.layout = layout() 

if __name__ == '__main__':
    app.run(debug=True)