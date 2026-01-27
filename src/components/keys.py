from dash import html
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.clean_data import load_data

def get_kpi_value():
    """
    Lit les CSV et calcule :
    1. Nombre d'avions (Trafic)
    2. Estimation CO2 (Trafic * facteur)
    3. Top Aéroport 
    """
    #Nombre d'avions actuellement en vol
    df_traffic = load_data("traffic")
    count = len(df_traffic)
    nb_plane = f"{count:,}".replace(",", " ")

    #Pollution
    df_pollution = pd.read_csv("data/cleaned/annual-co-emissions-from-aviation.csv")
    df_world_pollution = df_pollution.query("Entity == 'World' and Year == 2024")
    world_pollution = df_world_pollution["Total annual CO₂ emissions from aviation"].iloc[0]
    total_pollution = f"{world_pollution:,} t".replace(","," ")

    # Aéoroport qui possède le plus de routes (le plus "grand")
    max_altitude = df_traffic["baro_altitude"].max()
    max = f"{max_altitude:,} m".replace(","," ")


    return nb_plane, total_pollution, max


def render():

    nb_plane, total_co2, max_alt= get_kpi_value()
    # --- STYLE DU CONTENEUR ---
    container_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',        # <--- CRUCIAL : Prend toute la hauteur de la colonne parente
        'justifyContent': 'space-between', # Répartit les cartes du haut en bas
        'gap': '15px'            # Espace entre les cartes
    }

    # --- FONCTION DE GÉNÉRATION DE CARTE ---
    def create_kpi_card(title, value, gradient_colors):
        return html.Div([
            # Le Titre
            html.P(title, style={
                'color': 'rgba(255, 255, 255, 0.7)', 
                'fontSize': '12px', 
                'textTransform': 'uppercase', 
                'margin': '0',
                'letterSpacing': '1px',
                'fontWeight': '600'
            }),
            # La Valeur
            html.H2(value, style={
                'color': 'white', 
                'fontSize': '28px', 
                'fontWeight': 'bold', 
                'margin': '5px 0 0 0'
            })
        ], style={
            # L'astuce du dégradé
            'background': f'linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]})',
            'borderRadius': '12px',
            'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.4)',
            'textAlign': 'center',
            
            # --- CENTRAGE VERTICAL DU TEXTE ---
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center',
            
            # --- ELASTICITÉ ---
            'flex': '1',         # <--- MAGIQUE : La carte grandit pour remplir l'espace vide
            'minHeight': '0'     # Sécurité pour le flexbox
        })

    # --- RETOUR DU LAYOUT ---
    return html.Div([
        # Carte 1 : Bleu
        create_kpi_card("Vols Actifs", nb_plane , ["#1d8cf8", "#33d9b2"]),
        
        # Carte 2 : Orange
        create_kpi_card("Emission Co2", total_co2 , ["#ff5252", "#ffb142"]),
        
        # Carte 3 : Violet
        create_kpi_card("Altitude max.", max_alt , ["#706fd3", "#ff793f"]),
        
    ], style=container_style)