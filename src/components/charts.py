import pandas as pd
import plotly.express as px
import os 
import sys
#charts.py va srvoir à créer des graphiques pour l'exploration des données

# Permet de trouver le fichier config.py à la racine du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from config import TRAFFIC_CLEANED_FILE

def create_altitude_histogram(): 
    """
    Crée un histogramme de la distribution des altitudes des aéroports
    à l'aide de Plotly pour une exploration interactive.
    """
    print("Création de l'histogramme des altitudes des aéroports...")
# Chargement des données nettoyées des avions
    df = pd.read_csv(TRAFFIC_CLEANED_FILE)

    fig = px.histogram(df, 
                   x='baro_altitude', 
                   nbins=50, 
                   title='Distribution de l\'Altitude des Aéroports (Exploration Plotly)')

    fig.show() 

if __name__ == "__main__":
    create_altitude_histogram()

