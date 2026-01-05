from dash import html
from src.components import keys, map_view, info_panel, charts

COLORS = {
    'background': '#1e1e2f',
    'card_bg': '#27293d',
    'electric_blue': '#1d8cf8',
    'text': '#ffffff',
    'text_dim': '#9a9a9a'
}

CARD_STYLE = {
    'backgroundColor': COLORS['card_bg'],
    'borderRadius': '12px',
    'padding': '20px',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.5)',
    'marginBottom': '20px',
    'color': COLORS['text']
}

def layout():
    

    return html.Div([
        
        # --- 1. INTRODUCTION (Prend toute la largeur en haut) ---
        html.Div([
            html.H1("Trafic Aérien", 
                    style={'color': COLORS['text'], 'fontWeight': 'bold', 'marginBottom': '10px'}),
            
            html.Div([
                html.H4("Vue d'ensemble et Surveillance", style={'color': COLORS['electric_blue'], 'marginBottom': '10px'}),
                html.P(
                    "Interface de contrôle en temps réel. Suivez les trajectoires, analysez les données "
                    "aéroportuaires et consultez les indicateurs de performance clés.",
                    style={'color': COLORS['text_dim'], 'fontSize': '14px', 'margin': '0'}
                )
            ], style={**CARD_STYLE, 'borderLeft': f'5px solid {COLORS["electric_blue"]}', 'paddingLeft': '30px', 'minHeight': '150px'})
        ], style={'width': '100%',
                'marginBottom': '20px'}),

        # --- 2. ZONE PRINCIPALE (Division en colonnes sous l'intro) ---
        html.Div([
            
            # COLONNE GAUCHE (KPIs) : 15%
            html.Div([
                keys.render()
            ], style={'width': '15%', 'marginRight': '20px'}),

            # COLONNE DROITE (Dashboard Interactif) : 85%
            html.Div([
                
                # Zone Map + Info Panel
                html.Div([
                    # Carte (70% de la colonne de droite)
                    html.Div([
                        map_view.render()
                    ], style={'width': '69%', 'marginRight': '1%'}),
                    
                    # Panneau d'info (30% de la colonne de droite)
                    html.Div([
                        info_panel.render()
                    ], style={'width': '30%'})
                ], style={'display': 'flex', 'flexDirection': 'row', 'marginBottom': '20px'}),

                # Graphiques du bas
                html.Div([
                    charts.render()
                ], style=CARD_STYLE)

            ], style={'width': '85%'})

        ], style={'display': 'flex', 'flexDirection': 'row'}) # Aligne les colonnes horizontalement

    ], style={
        'padding': '30px', 
        'backgroundColor': COLORS['background'], 
        'minHeight': '100vh',
        'fontFamily': 'Segoe UI, sans-serif'
    })