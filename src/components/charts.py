import pandas as pd
import plotly.express as px
import os 
import sys

# Gestion du chemin pour config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import TRAFFIC_CLEANED_FILE

# Chargement des données d'avions
df = pd.read_csv(TRAFFIC_CLEANED_FILE)

def histo1(df):
    # On adapte x et color aux colonnes réelles : baro_altitude et origin_country
    fig = px.histogram(df, 
                    x='baro_altitude', 
                    nbins=50, 
                    range_x=[0, 15000],
                    title="<b>Répartition de l'Altitude des Avions Français en Vol</b>",
                    color_discrete_sequence=["#CC0000"],
                    color='origin_country', # Utilise le pays d'origine
                    hover_data=['callsign', 'velocity_kmh', 'longitude', 'latitude'],
                    hover_name='callsign', # Affiche l'identifiant de l'avion en gras
                    opacity=0.75,
                    template="plotly_dark"
    )
    
    fig.update_layout(
        bargap=0.25,
        font_family="Arial",
        title_x=0.5, 
        xaxis=dict(gridcolor='grey'), 
        yaxis=dict(gridcolor='grey'),
        xaxis_title="Altitude (Barométrique)",
        yaxis_title="Nombre d'Avions",
    )

    fig.show()
    return fig

histo1(df)

