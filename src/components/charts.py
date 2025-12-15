import pandas as pd
import plotly.express as px

# 1. Chargement de votre base de données
df = pd.read_csv('airports_cleaned.csv')

# 2. Création de l'histogramme de l'altitude
fig = px.histogram(df, x='Altitude', title='Distribution de l\'Altitude des Aéroports')

# 3. Affichage
fig.show()
