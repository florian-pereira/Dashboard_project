import pandas as pd
import plotly.express as px
import os
import sys
from dash import dcc, html

# Configuration du chemin pour l'import de load_data
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.clean_data import load_data

def get_continent(lat, lon):
    """
    Détermine le continent en fonction des coordonnées GPS.
    """
    if pd.isna(lat) or pd.isna(lon): return "Inconnu"

    # Définition sommaire des zones (Lat/Lon)
    if 35 <= lat <= 71 and -25 <= lon <= 45: return "Europe"
    elif 15 <= lat <= 72 and -170 <= lon <= -50: return "Amérique du Nord"
    elif -56 <= lat <= 15 and -95 <= lon <= -35: return "Amérique du Sud"
    elif -35 <= lat <= 37 and -20 <= lon <= 51: return "Afrique"
    elif 5 <= lat <= 77 and 45 <= lon <= 180: return "Asie"
    elif -47 <= lat <= 0 and 110 <= lon <= 180: return "Océanie"
    else: return "Inconnu"

def render():
    try:
        df = load_data('traffic')
    except Exception as e:
        return html.Div(f"Erreur chargement: {e}", style={'color': 'red'})

    if df is None or df.empty:
        return html.Div("Aucune donnée disponible", style={'color': 'white', 'textAlign': 'center'})

    # 1. Création de la colonne continent
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)

    # 2. Filtrage pour supprimer les "Inconnu"
    df_filtered = df[df['continent'] != "Inconnu"].copy()

    # 3. Palette de couleurs "Dashboard Theme" (Néon/Electrique)
    # Ces couleurs ressortent mieux sur le fond sombre #27293d
    couleurs_map = {
        "Europe": "#1d8cf8",           # Bleu Électrique (Couleur principale)
        "Amérique du Nord": "#fd5d93",  # Rose fluo
        "Asie": "#00f2c3",             # Cyan / Turquoise
        "Amérique du Sud": "#ff8d72",   # Orange Corail
        "Afrique": "#ffb142",          # Jaune Orange
        "Océanie": "#d63031"           # Rouge vif
    }

    # 4. Création du graphique "Donut"
    fig = px.pie(
        df_filtered, 
        names='continent', 
        color='continent',
        color_discrete_map=couleurs_map,
        title="<b>Répartition par Continent</b>",
        hole=0.55, # Donut un peu plus fin pour l'élégance
        template="plotly_dark"
    )

    # 5. Nettoyage et Centrage
    fig.update_traces(
        textposition='inside',
        textinfo='percent', # On affiche juste le % dedans pour ne pas surcharger
        hovertemplate="<b>%{label}</b><br>Avions: %{value} (%{percent})<extra></extra>",
        marker=dict(line=dict(color='#27293d', width=2)) # Petite bordure sombre pour séparer les parts
    )

    fig.update_layout(
        # Fond transparent pour s'intégrer au conteneur parent
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
        # Police et titre
        font=dict(family="Segoe UI, sans-serif", color="#ffffff"),
        title=dict(
            font=dict(size=14, color="#ffffff"),
            x=0.5,      # Centrage horizontal du titre
            y=0.95,     # Position haute
            xanchor='center',
            yanchor='top'
        ),
        
        # Légende en bas pour équilibrer
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        
        # Marges réduites pour maximiser la taille du graph
        margin=dict(t=40, b=30, l=20, r=20)
    )

    # Retourne le graph dans un conteneur Flex pour le centrage parfait
    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False, 'staticPlot': False},
            style={'width': '100%', 'height': '100%'} # Remplit le conteneur parent
        )
    ], style={
        'height': '100%', 
        'width': '100%',
        'display': 'flex',
        'alignItems': 'center',     # Centrage Vertical
        'justifyContent': 'center', # Centrage Horizontal
        'padding': '0'
    })