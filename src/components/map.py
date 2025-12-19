from dash import dcc, html
import plotly.express as px
import pandas as pd

def render(df):
    # Fausse map pour la démo
    fake_df = pd.DataFrame({'lat': [48.85], 'lon': [2.35], 'ville': ['Paris']})
    fig = px.scatter_mapbox(fake_df, lat="lat", lon="lon", zoom=3)
    fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})

    return html.Div([
        dcc.Graph(figure=fig, style={'height': '500px'})
    ], style={'width': '70%', 'paddingRight': '10px'}) # 70% de largeur