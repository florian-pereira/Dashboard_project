import pandas as pd
import plotly.express as px
import os
import sys

# Configuration du chemin pour l'import de load_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.clean_data import load_data

def get_continent(lat, lon):
    """
    Détermine le continent en fonction des coordonnées GPS (Bounding Boxes).
    """
    if pd.isna(lat) or pd.isna(lon):
        return "Inconnu"

    # Définition des zones géographiques (Lat/Lon)
    if 35 <= lat <= 71 and -25 <= lon <= 45:
        return "Europe"
    elif 15 <= lat <= 72 and -170 <= lon <= -50:
        return "Amérique du Nord"
    elif -56 <= lat <= 15 and -95 <= lon <= -35:
        return "Amérique du Sud"
    elif -35 <= lat <= 37 and -20 <= lon <= 51:
        return "Afrique"
    elif 5 <= lat <= 77 and 45 <= lon <= 180:
        return "Asie"
    elif -47 <= lat <= 0 and 110 <= lon <= 180:
        return "Océanie"
    else:
        return "Inconnu" # Regroupe les océans et zones non définies

def cheeze_plot(df):
    if df is None or df.empty:
        print("Le DataFrame est vide.")
        return

    # 1. Création de la colonne continent via les coordonnées
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)

    # 2. Filtrage pour supprimer les "Inconnu"
    df_filtered = df[df['continent'] != "Inconnu"].copy()

    # 3. Dictionnaire de couleurs personnalisées
    couleurs_map = {
        "Europe": "#18669a",           # Bleu
        "Amérique du Nord": "#9c2417",  # Rouge
        "Amérique du Sud": "#118843",   # Vert
        "Asie": "#c9a209",             # Jaune
        "Afrique": "#a25613",          # Orange
        "Océanie": "#6b2088"           # Violet
    }

    # 4. Création du graphique "fromage"
    fig = px.pie(
        df_filtered, 
        names='continent', 
        color='continent',
        color_discrete_map=couleurs_map,
        title="<b>Répartition des Avions par Continent (Données GPS)</b>",
        hole=0.4, # Style donut
        template="plotly_dark"
    )

    # 5. Nettoyage de l'affichage
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Nombre d'avions : %{value}<extra></extra>"
    )

    fig.update_layout(
        title_x=0.5,
        margin=dict(t=80, b=20, l=20, r=20)
    )

    fig.show()

if __name__ == "__main__":
    # Chargement des données trafic
    df_avions = load_data(dataset="traffic")
    
    # Lancement du graphique
    cheeze_plot(df_avions)