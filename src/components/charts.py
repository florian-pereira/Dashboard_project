import pandas as pd
import plotly.express as px
import os 

# Assurez-vous que le chemin vers le fichier est correct
file_path = 'airports_cleaned.csv' 
df = pd.read_csv(file_path)

# Création de l'histogramme de l'altitude
# J'ajoute nbins pour avoir un peu plus de détail dans la distribution
fig = px.histogram(df, 
                   x='Altitude', 
                   nbins=50, 
                   title='Distribution de l\'Altitude des Aéroports (Exploration Plotly)')

fig.show()
