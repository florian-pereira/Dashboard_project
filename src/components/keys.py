from dash import html

def render(df):
    # Style des cartes (petits rectangles)
    card_style = {
        'background': 'white',
        'borderRadius': '5px',
        'padding': '15px',
        'margin': '10px',
        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
        'textAlign': 'center',
        'flex': '1' # Pour qu'ils prennent toute la largeur dispo
    }
    
    return html.Div([
        html.Div([html.H2("125"), html.P("Avions en vol")], style=card_style),
        html.Div([html.H2("11 km"), html.P("Altitude Moyenne")], style=card_style),
        html.Div([html.H2("850 km/h"), html.P("Vitesse Max")], style=card_style),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'})