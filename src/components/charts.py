from dash import dcc, html
import plotly.express as px
import pandas as pd

def render(df):
    # Faux graph pour la démo
    df_fake = pd.DataFrame({'x': [1, 2, 3], 'y': [10, 20, 15]})
    fig = px.bar(df_fake, x='x', y='y', title="Statistiques Globales")
    
    return html.Div([
        dcc.Graph(figure=fig)
    ], style={'marginTop': '20px', 'padding': '10px', 'background': 'white'})