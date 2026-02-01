from dash import html
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.clean_data import load_data

def get_kpi_value():
    """
    Lit les CSV et calcule :
    1. Nombre d'avions
    2. Nombre d'avions qui proviennent de France
    3. Estimation CO2
    """
    #Nombre d'avions actuellement en vol
    df_traffic = load_data("traffic")
    count = len(df_traffic)
    nb_plane = f"{count:,}".replace(",", " ")

    # Aéoroport qui possède le plus de routes (le plus "grand")
    df_nb_plane_france = df_traffic.query("origin_country == 'France'")
    count_plane_france = len(df_nb_plane_france)
    nb_plane_f = f"{count_plane_france:,}".replace(","," ")

    #Pollution
    df_pollution = pd.read_csv("data/cleaned/annual-co-emissions-from-aviation.csv")
    df_world_pollution = df_pollution.query("Entity == 'World' and Year == 2024")
    world_pollution = df_world_pollution["Total annual CO₂ emissions from aviation"].iloc[0]
    total_pollution = convert_co(world_pollution)

    return nb_plane, nb_plane_f , total_pollution

def convert_co(total_pollution):
    """
    Convertit un nombre (tonnes) en format lisible (kt, Mt, Gt).
    """
    if total_pollution >= 1_000_000_000:
        return f"{total_pollution/1_000_000_000:0.1f} Gt"
    elif total_pollution >= 1_000_000 :
        return f"{total_pollution/1_000_000:0.1f} Mt"
    elif total_pollution >= 1_000:
        return f"{total_pollution/1_000:0.1f} kt"
    else:
        return f"{total_pollution:0.1f} t"

def render():
    """
    Génère le conteneur vertical affichant les 3 cartes KPIs (Vols, France, CO2).
    Utilise un layout Flexbox pour répartir les cartes sur toute la hauteur disponible.
    """
    nb_plane, nb_plane_france , total_co2= get_kpi_value()
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

        # Carte 2 : Violet
        create_kpi_card("Vols Actifs (France)", nb_plane_france , ["#706fd3", "#ff793f"]),

        # Carte 3 : Orange
        create_kpi_card("Emission Co2", total_co2 , ["#ff5252", "#ffb142"]),
        
    ], style=container_style)