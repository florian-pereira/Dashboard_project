import pandas as pd
import plotly.express as px
import os 
import sys
import plotly.io as pio

# Force l'affichage dans le navigateur
pio.renderers.default = "browser"

# Gestion du chemin pour config 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils.clean_data import load_data 

def get_continent(lat, lon):
    """Détermine le continent en fonction des coordonnées GPS"""
    if pd.isna(lat) or pd.isna(lon):
        return "Inconnu"
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
        return "Inconnu"

def histo1(df):
    if df is None or df.empty:
        print("Le DataFrame est vide ou non chargé.")
        return
        
    # 1. Traitement : On calcule les continents
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)
    
    # 2. On filtre pour enlever les "Inconnu" (océans/erreurs) comme dans le fromage
    df_plot = df[df['continent'] != "Inconnu"].copy()

    # 3. Couleurs personnalisées (les mêmes que ton fromage pour être cohérent)
    couleurs_map = {
        "Europe": "#3498db", "Amérique du Nord": "#e74c3c", 
        "Amérique du Sud": "#2ecc71", "Asie": "#f1c40f", 
        "Afrique": "#e67e22", "Océanie": "#9b59b6"
    }

    fig = px.histogram(df_plot, 
                x='baro_altitude', 
                nbins=50, 
                range_x=[0, 15000],
                title="<b>Répartition de l'Altitude des Avions par Continent</b>",
                color='continent', # Remplace origin_country
                color_discrete_map=couleurs_map,
                hover_data={
                    'baro_altitude': False,
                    'continent': True,
                    'origin_country': True, 
                    'callsign': True,
                    'velocity_kmh': True
                },
                template="plotly_dark"
    )
    
    fig.update_layout(
        bargap=0.1, # Réduit un peu l'espace pour un look plus dense
        title_x=0.5, 
        xaxis_title="Altitude (Barométrique)",
        yaxis_title="Nombre d'Avions",
        legend_title="Continents (GPS)"
    )

    fig.show()

if __name__ == "__main__":
    df_avions = load_data(dataset="traffic")
    histo1(df_avions)
    input("Graphique lancé. Appuyez sur Entrée pour fermer le script...")