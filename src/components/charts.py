from dash import dcc, html
import plotly.express as px
import pandas as pd
import os 
import sys

# Couleurs de ton thème (on les définit ici pour rester cohérent)
COLORS = {
    'card_bg': '#27293d',
    'electric_blue': '#1d8cf8',
    'text': '#ffffff',
    'text_dim': '#9a9a9a'
}

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

def render(df=None): # Ajout du paramètre df pour le temps réel
    # Si aucun df n'est passé (premier chargement), on charge le CSV
    if df is None:
        from src.utils.clean_data import load_data 
        df = load_data('traffic')
        
    if df is None or df.empty:
        return html.Div("En attente de données...", style={'color': COLORS['text_dim']})
        
    # 1. Traitement des continents
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)
    df_plot = df[df['continent'] != "Inconnu"].copy()

    # 2. Couleurs des continents adaptées au mode sombre (plus vibrantes)
    couleurs_map = {
        "Europe": "#1d8cf8",         # Ton Electric Blue
        "Amérique du Nord": "#e14eca", # Rose/Violet vif
        "Amérique du Sud": "#00f2c3", # Turquoise
        "Asie": "#ff8d72",           # Orange corail
        "Afrique": "#fd5d93",        # Rouge/Rose
        "Océanie": "#344675"         # Bleu nuit
    }

    # 3. Création de l'histogramme (obligatoire pour ta consigne !)
    fig = px.histogram(
        df_plot, 
        x='baro_altitude', 
        nbins=40, 
        range_x=[0, 13000],
        title="<b>Distribution des altitudes par zone géographique</b>",
        color='continent',
        color_discrete_map=couleurs_map,
        template="plotly_dark"
    )
    
    # 4. Ajustement ultra-précis du design pour ton thème
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', # Fond transparent pour voir le fond de la carte
        plot_bgcolor='rgba(0,0,0,0)',  # Fond du graphique transparent
        font_color=COLORS['text'],
        title_font_size=18,
        title_x=0.05,
        margin=dict(l=20, r=20, t=60, b=20),
        bargap=0.2,
        xaxis=dict(gridcolor='#33334d', title="Altitude (mètres)"),
        yaxis=dict(gridcolor='#33334d', title="Nombre d'appareils"),
        legend=dict(bgcolor='rgba(0,0,0,0)')
    )

    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False} # On cache les outils Plotly pour un look plus clean
        )
    ], style={
        'backgroundColor': COLORS['card_bg'], 
        'borderRadius': '12px',
        'padding': '10px'
    })