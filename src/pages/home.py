from dash import html
from src.components import keys, map_view, charts, cheeze

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
        
        # --- 1. INTRODUCTION (En-tête) ---
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
            ], style={**CARD_STYLE, 'borderLeft': f'5px solid {COLORS["electric_blue"]}', 'paddingLeft': '30px', 'minHeight': '100px'})
        ], style={'width': '100%', 'marginBottom': '20px'}),

        # --- 2. ZONE PRINCIPALE (CHIFFRES + MAP MÊME HAUTEUR) ---
        html.Div([
            
            # COL 1 : KPIs (10%)
            html.Div([
                keys.render()
            ], style={
                'width': '10%',           # Largeur cible
                'minWidth': '10%',        # Sécurité : ne peut pas être écrasé par la map
                'marginRight': '20px',    # Espace entre les chiffres et la map
                
                # --- ÉTIREMENT VERTICAL ---
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'space-between' # Répartit les chiffres (Haut, Milieu, Bas)
            }),

            # COL 2 : MAP (60%)
            html.Div([
                map_view.render()
            ], style={
                'width': '60%',           # Largeur cible
                'minWidth': '0',          # Autorise le contenu (Iframe) à s'adapter
                'overflow': 'hidden',     # COUPE les bords si la map essaie de dépasser (Anti-Chevauchement)
                'borderRadius': '12px'    # Esthétique
            }),
            # COL 3 : CHEEZE / CAMEMBERT (Le reste ~30%)
            
            html.Div([
                cheeze.render()
            ], style={
                'height': '100%',
                'display': 'flex',
                'alignItems': 'center',
                'flex': '1',
                'backgroundColor': COLORS['card_bg'],
                'borderRadius': '12px',
                'padding': '10px',
                'overflow': 'hidden'
            })

        ], style={
            'display': 'flex',        # Active Flexbox
            'flexDirection': 'row',   # Met côte à côte
            'alignItems': 'stretch',  # FORCE les deux colonnes à avoir la MÊME HAUTEUR
            'width': '100%',
            'marginBottom': '20px'
        }),

        # --- 3. ZONE BASSE (CHARTS) - 50% ---
        html.Div([
            charts.render()
        ], style={
            **CARD_STYLE, 
            'width': '50%',          # Prend la moitié de l'écran
            'boxSizing': 'border-box'
        })

    ], style={
        'padding': '30px', 
        'backgroundColor': COLORS['background'], 
        'minHeight': '100vh',
        'fontFamily': 'Segoe UI, sans-serif'
    })