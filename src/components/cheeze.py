"""
Génération d'un graphique en anneau (Donut) illustrant la répartition des vols par continent.

Ce module permet de :
- Segmenter le trafic aérien selon les coordonnées géographiques.
- Visualiser la part de chaque continent via un Pie Chart stylisé.
- S'intégrer dynamiquement dans un Dashboard Dash.
"""

from dash import dcc, html
import plotly.express as px
import pandas as pd
import os
import sys

COLORS = {
    'card_bg': '#27293d',
    'text': '#ffffff',
    'text_dim': '#9a9a9a'
}

CONTINENT_COLORS = {
    "Europe": "#1d8cf8",      
    "Amérique du Nord": "#fd5d93", 
    "Asie": "#00f2c3",          
    "Amérique du Sud": "#ff8d72",
    "Afrique": "#ffb142",    
  "Océanie": "#d63031"       
}

def get_continent(lat, lon):
    """
    Détermine le continent d'appartenance selon les coordonnées GPS.
    Retourne 'Inconnu' si les coordonnées sont hors bornes.
    """
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


def render(df=None):
    if df is None:
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            from src.utils.clean_data import load_data
            df = load_data('traffic')
        except Exception as e:
            return html.Div(f"Erreur chargement: {e}", style={'color': 'red'})

    if df is None or df.empty:
        return html.Div("Aucune donnée disponible", style={'color': COLORS['text'], 'textAlign': 'center'})

    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)
    df_filtered = df[df['continent'] != "Inconnu"].copy()

    fig = px.pie(
        df_filtered, 
        names='continent', 
        color='continent',
        color_discrete_map=CONTINENT_COLORS,
        title="<b>Répartition par Continent</b>",
        hole=0.55, 
        template="plotly_dark"
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent', 
        hovertemplate="<b>%{label}</b><br>Avions: %{value} (%{percent})<extra></extra>",
        marker=dict(line=dict(color=COLORS['card_bg'], width=2)) 
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        
        font=dict(family="Segoe UI, sans-serif", color=COLORS['text']),
        
        title=dict(
            font=dict(size=14, color=COLORS['text']),
            x=0.5,      
            y=0.95,     
            xanchor='center',
            yanchor='top'
        ),
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
        
        margin=dict(t=40, b=30, l=20, r=20)
    )

    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False, 'staticPlot': False},
            style={'width': '100%', 'height': '100%'}
        )
    ], style={
        'height': '100%', 
        'width': '100%',
        'display': 'flex',
        'alignItems': 'center',    
        'justifyContent': 'center',
        'padding': '0',
        'backgroundColor': COLORS['card_bg'], 
        'borderRadius': '12px'
    })