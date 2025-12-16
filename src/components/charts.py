import pandas as pd
import plotly.express as px
import os 
from config import AIRPORTS_CLEANED_FILE

df = pd.read_csv(AIRPORTS_CLEANED_FILE)

fig = px.histogram(df, 
                   x='Altitude', 
                   nbins=50, 
                   title='Distribution de l\'Altitude des Aéroports (Exploration Plotly)')

fig.show()
