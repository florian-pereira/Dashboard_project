from dash import html
# On importe tous nos composants
from src.components import keys, map, info_panel, charts

def layout(): # On peut en faire une fonction si tu préfères
    # On simule un DF vide pour l'instant car nos composants utilisent des fausses données
    df = None 

    return html.Div([
        # 1. HEADER
        html.H1("✈️ Dashboard Trafic Aérien", 
                style={'textAlign': 'center', 'color': '#333', 'padding': '20px'}),
        
        # 2. KPIs
        keys.render(df),
        
        # 3. ZONE PRINCIPALE (Map + Panel)
        # C'est le conteneur FLEX qui met les éléments côte à côte
        html.Div([
            map.render(df),   # Prend 70%
            info_panel.render()    # Prend 30%
        ], style={'display': 'flex', 'flexDirection': 'row'}), # <--- LA MAGIE EST ICI
        
        # 4. GRAPHIQUES DU BAS
        charts.render(df)
        
    ], style={'padding': '20px', 'backgroundColor': '#f4f4f4'}) # Fond gris clair global