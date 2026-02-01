"""
Génération d'un histogramme interactif affichant la distribution des altitudes des avions.

Ce module permet de :
- Déterminer le continent approximatif d'un avion selon ses coordonnées (Lat/Lon).
- Segmenter les données de trafic aérien par zone géographique.
- Visualiser la répartition des altitudes via un histogramme empilé (Stacked Histogram).
- S'intégrer dynamiquement dans un Dashboard Dash (mise à jour temps réel supportée).
"""

from dash import dcc, html
import plotly.express as px
import pandas as pd
import os 
import sys

COLORS = {
    'card_bg': '#27293d',
    'electric_blue': '#1d8cf8',
    'text': '#ffffff',
    'text_dim': '#9a9a9a'
}

def get_continent(lat, lon):
    """
    Détermine le continent d'appartenance basé sur des boîtes englobantes (Bounding Boxes).
    Retourne 'Inconnu' si les coordonnées sont hors des zones définies ou manquantes.
    """
    if pd.isna(lat) or pd.isna(lon):
        return "Inconnu"
    
    # Même logique que dans cheeze.py, je réutilise les bornes GPS
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


def render(df=None):
    """
    Génère le layout HTML contenant le graphique Plotly.
    
    Args:
        df (pd.DataFrame, optional): DataFrame contenant les données 'latitude', 'longitude' 
                                     et 'baro_altitude'. Si None, tente de charger les données par défaut.
    """
    if df is None:
        try:
            from src.utils.clean_data import load_data 
            df = load_data('traffic')
        except ImportError:
            return html.Div("Erreur: Module de données introuvable.", style={'color': 'red'})
        
    if df is None or df.empty:
        return html.Div("En attente de données...", style={'color': COLORS['text_dim']})
        
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)
    # Hop, on ne garde que ce qu'on a réussi à identifier
    df_plot = df[df['continent'] != "Inconnu"].copy()

    couleurs_map = {
        "Europe": "#1d8cf8",
        "Amérique du Nord": "#e14eca",
        "Amérique du Sud": "#00f2c3",
        "Asie": "#ff8d72",
        "Afrique": "#fd5d93",
        "Océanie": "#344675"
    }

    fig = px.histogram(
        df_plot, 
        x='baro_altitude', 
        nbins=40, 
        range_x=[0, 13000], # Je coupe à 13km parce qu'au dessus y'a quasiment personne, ça sert à rien d'afficher du vide
        color='continent',
        color_discrete_map=couleurs_map,
        template="plotly_dark"
    )

    fig.update_traces(
        hovertemplate="<b>%{data.name}</b><br>" +
                      "Altitude: %{x} m<br>" +
                      "Appareils: %{y}<extra></extra>"
    )
    
    fig.update_layout(
        # Fond transparent pour l'intégration propre dans le dash
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        
        title={
            'text': "<b>Distribution des altitudes par zone géographique</b>",
            'y': 0.96,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top'
        },
        
        margin=dict(l=20, r=20, t=110, b=20),
        bargap=0.2,
        
        xaxis=dict(gridcolor='#33334d', title="Altitude (mètres)"),
        yaxis=dict(gridcolor="#33334d", title="Nombre d'appareils"),
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=-0.05,
            bgcolor='rgba(0,0,0,0)',
            title=None,
            font=dict(size=10)
        )
    )

    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False},
            style={'height': '100%', 'width': '100%'}
        )
    ], style={
        'backgroundColor': 'transparent', 
        'height': '100%',
        'width': '100%'
    })