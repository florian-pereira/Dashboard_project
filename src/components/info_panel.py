from dash import html

def render():
    return html.Div([
        html.H3("Détails du Vol", style={'borderBottom': '1px solid white', 'paddingBottom': '10px'}),
        html.P("Cliquez sur un avion pour voir les infos."),
        html.Div([
            html.P("Compagnie : --"),
            html.P("Altitude : --"),
            html.P("Vitesse : --"),
        ], style={'marginTop': '20px'})
    ], style={
        'width': '30%',             # 30% de largeur
        'backgroundColor': '#333',  # Fond gris foncé
        'color': 'white',           # Texte blanc
        'padding': '20px',
        'height': '500px',          # Même hauteur que la map
        'borderRadius': '5px'
    })