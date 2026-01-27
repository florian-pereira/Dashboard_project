import pandas as pd
import plotly.express as px
import os
import sys
import plotly.io as pio

# Configuration du rendu dans le navigateur
pio.renderers.default = "browser"

# Gestion du chemin pour importer load_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.clean_data import load_data

def get_continent(lat, lon):
    """Détermine le continent en fonction des coordonnées GPS"""
    if pd.isna(lat) or pd.isna(lon):
        return "Inconnu"
    if 35 <= lat <= 71 and -25 <= lon <= 45: return "Europe"
    elif 15 <= lat <= 72 and -170 <= lon <= -50: return "Amérique du Nord"
    elif -56 <= lat <= 15 and -95 <= lon <= -35: return "Amérique du Sud"
    elif -35 <= lat <= 37 and -20 <= lon <= 51: return "Afrique"
    elif 5 <= lat <= 77 and 45 <= lon <= 180: return "Asie"
    elif -47 <= lat <= 0 and 110 <= lon <= 180: return "Océanie"
    else: return "Inconnu"

def dynamic_bubble_chart(df):
    if df is None or df.empty:
        print("Données vides.")
        return

    # 1. Préparation des données (Continents)
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)
    
    # On retire les Inconnus pour garder un graphique propre
    df = df[df['continent'] != "Inconnu"].copy()

    # 2. Création du Bubble Chart (Style Gapminder)
    # x : Vitesse, y : Altitude, size : Vitesse (pour accentuer), color : Continent
    fig = px.scatter(
        df, 
        x="velocity_kmh", 
        y="baro_altitude",
        size="velocity_kmh", 
        color="continent",
        hover_name="callsign", 
        log_x=False, 
        size_max=15,
        title="<b>Analyse Dynamique : Vitesse vs Altitude par Continent</b>",
        labels={
            "velocity_kmh": "Vitesse (km/h)",
            "baro_altitude": "Altitude (m)",
            "continent": "Continent"
        },
        template="plotly_dark",
        # Mapping de couleurs cohérent avec tes autres graphiques
        color_discrete_map={
            "Europe": "#3498db", "Amérique du Nord": "#e74c3c", 
            "Amérique du Sud": "#2ecc71", "Asie": "#f1c40f", 
            "Afrique": "#e67e22", "Océanie": "#9b59b6"
        }
    )

    # 3. Optimisation du Layout (proche de l'exercice Gapminder)
    fig.update_layout(
        title_x=0.5,
        xaxis=dict(gridcolor='gray', showgrid=True),
        yaxis=dict(gridcolor='gray', showgrid=True),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # 4. Ajustement des traces (opacité pour gérer les chevauchements)
    fig.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='White')))

    fig.show()

if __name__ == "__main__":
    # Chargement des données via ton utilitaire
    df_avions = load_data(dataset="traffic")
    
    # Affichage
    dynamic_bubble_chart(df_avions)