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
        
    # 1. Traitement
    df['continent'] = df.apply(lambda row: get_continent(row['latitude'], row['longitude']), axis=1)
    df_plot = df[df['continent'] != "Inconnu"].copy()

    # 2. Couleurs
    couleurs_map = {
        "Europe": "#1d8cf8",
        "Amérique du Nord": "#e14eca",
        "Amérique du Sud": "#00f2c3",
        "Asie": "#ff8d72",
        "Afrique": "#fd5d93",
        "Océanie": "#344675"
    }

    # 3. Création Graphique
    fig = px.histogram(
        df_plot, 
        x='baro_altitude', 
        nbins=40, 
        range_x=[0, 13000],
        color='continent',
        color_discrete_map=couleurs_map,
        template="plotly_dark"
    )

    fig.update_traces(
        hovertemplate="<b>%{data.name}</b><br>" +
                      "Altitude: %{x} m<br>" +
                      "Appareils: %{y}<extra></extra>"
    )
    
    # 4. Design & Layout
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font_color=COLORS['text'],
        
        # Titre
        title={
            'text': "<b>Distribution des altitudes par zone géographique</b>",
            'y': 0.96,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top'
        },
        
        # Marges (t=110 pour laisser la place à la légende sous le titre)
        margin=dict(l=20, r=20, t=110, b=20),
        bargap=0.2,
        
        xaxis=dict(gridcolor='#33334d', title="Altitude (mètres)"),
        yaxis=dict(gridcolor="#33334d", title="Nombre d'appareils"),
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            bgcolor='rgba(0,0,0,0)',
            title=None 
        )
    )

    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False}
        )
    ], style={
        'backgroundColor': COLORS['card_bg'], 
        'borderRadius': '12px',
        'padding': '10px'
    })