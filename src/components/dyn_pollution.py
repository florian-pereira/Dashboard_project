"""
Génération d'un graphique animé (Scatter Plot) analysant l'empreinte carbone de l'aviation mondiale.

Ce script croise les données d'émissions de CO₂ (Time Series) avec le volume de routes 
aériennes par pays pour visualiser l'intensité polluante.

Fonctionnalités :
- Nettoyage et fusion des datasets (Pollution & Aéroports).
- Calcul de l'intensité (CO₂ / Route) et mapping des continents.
- Configuration avancée de Plotly (Animation, Faceting, Style Dark).
- Correction des infobulles (Hovertemplate) pour supporter l'animation.
- Export sous forme de composant Dash.
"""

import plotly.express as px
import plotly.io as pio
import os
import pandas as pd
import numpy as np
from dash import dcc, html

def get_continent_mapping():
    mapping = {
        'Asia': [
            'Hong Kong', 'EEast Timor', 'Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 
            'Cambodia', 'China', 'Cyprus', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iran, Islamic Rep.',
            'Iraq', 'Israel', 'Japan', 'Jordan', 'Kazakhstan', 'Kuwait', 'Kyrgyzstan', 'Laos', 
            'Lao People\'s Democratic Republic', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 
            'Myanmar', 'Nepal', 'North Korea', 'Oman', 'Pakistan', 'Palestine', 'Philippines', 
            'Qatar', 'Saudi Arabia', 'Singapore', 'South Korea', 'Korea, Rep.', 'Korea, Dem. People\'s Rep.',
            'Sri Lanka', 'Syria', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey', 
            'Turkmenistan', 'United Arab Emirates', 'Uzbekistan', 'Vietnam', 'Viet Nam', 'Yemen'
        ],
        'Oceania': [
            'Cook Islands', 'Micronesia (country)', 'Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 
            'New Zealand', 'Palau', 'Papua New Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 
            'Tuvalu', 'Vanuatu', 'New Caledonia', 'French Polynesia'
        ],
        'Europe': [
            'Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium', 'Bosnia and Herzegovina', 
            'Bulgaria', 'Croatia', 'Czechia', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 
            'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Kosovo', 
            'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 'Monaco', 
            'Montenegro', 'Netherlands', 'North Macedonia', 'Macedonia', 'Norway', 'Poland', 
            'Portugal', 'Romania', 'Russia', 'Russian Federation', 'San Marino', 'Serbia', 
            'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 
            'Vatican'
        ],
        'Africa': [
            'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 
            'Cape Verde', 'Cameroon', 'Central African Republic', 'Chad', 'Comoros', 'Congo', 
            'Democratic Republic of Congo', 'Congo, Dem. Rep.', 'Djibouti', 'Egypt', 
            'Equatorial Guinea', 'Eritrea', 'Eswatini', 'Swaziland', 'Ethiopia', 'Gabon', 
            'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Cote d\'Ivoire', 
            'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 
            'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 
            'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 
            'South Africa', 'South Sudan', 'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 
            'Zambia', 'Zimbabwe'
        ],
        'Americas': [
            'Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia', 
            'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 
            'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 
            'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 
            'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 
            'Suriname', 'Trinidad and Tobago', 'United States', 'United States of America', 'USA', 
            'Uruguay', 'Venezuela'
        ]
    }
    
    country_to_continent = {}
    for continent, countries in mapping.items():
        for country in countries:
            country_to_continent[country] = continent
    return country_to_continent

current_dir = os.path.dirname(os.path.abspath(__file__))
path_pollution = os.path.join(current_dir, '..', '..', 'data', 'cleaned', 'annual-co-emissions-from-aviation.csv')
path_airports = os.path.join(current_dir, '..', '..', 'data', 'cleaned', 'airports_cleaned.csv')

# Chargement des fichiers
df = pd.read_csv(path_pollution)
df_airports = pd.read_csv(path_airports)

# Je m'assure que l'année est bien un chiffre
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)

# Je compte le nombre total de routes par pays
df_routes = df_airports.groupby('Country')['Route_Count'].sum().reset_index()
df_routes.rename(columns={'Route_Count': 'Total_Routes'}, inplace=True)

# J'ajoute la colonne Continent pour chaque pays
continent_map = get_continent_mapping()
df['continent'] = df['Entity'].map(continent_map)

# Je retire les regroupements bizarres (Monde, EU...) pour garder que les VRAIS pays
blacklist = ['World', 'Africa', 'Asia', 'Europe', 'Oceania', 'South America', 'North America', 'European Union (28)']
df_clean = df[~df['Entity'].isin(blacklist)].copy()
df_clean = df_clean.dropna(subset=['continent'])

# Fusion des données pollution + routes
df_clean = pd.merge(df_clean, df_routes, left_on='Entity', right_on='Country', how='left')
# Je vire ceux où il manque des infos
df_clean = df_clean.dropna(subset=['Total_Routes'])
df_clean = df_clean[df_clean['Total_Routes'] > 0] 

all_years = range(df_clean['Year'].min(), df_clean['Year'].max() + 1)
all_countries = df_clean['Entity'].unique()
full_index = pd.MultiIndex.from_product([all_countries, all_years], names=['Entity', 'Year'])

df_clean = df_clean.set_index(['Entity', 'Year']).reindex(full_index).reset_index()

cols_to_fill = ['continent', 'Total_Routes', "Total annual CO₂ emissions from aviation"]
df_clean[cols_to_fill] = df_clean.groupby('Entity')[cols_to_fill].ffill()
df_clean = df_clean.dropna(subset=["Total annual CO₂ emissions from aviation"])

df_clean['Total_Routes'] = df_clean['Total_Routes'].astype(int)


col_pollution = "Total annual CO₂ emissions from aviation"
df_clean['Intensity_Per_Route'] = df_clean[col_pollution] / df_clean['Total_Routes']

traduction_continents = {
    'Asia': 'Asie', 'Europe': 'Europe', 'Americas': 'Amériques',
    'Africa': 'Afrique', 'Oceania': 'Océanie'
}
df_clean['continent'] = df_clean['continent'].replace(traduction_continents)

df_clean['Taille_Ajustee'] = np.power(df_clean['Total_Routes'], 0.6)

neon_colors = {'Asie': '#bd93f9', 'Europe': '#ffb86c', 'Amériques': '#50fa7b', 'Afrique': '#ff79c6', 'Océanie': '#8be9fd'}
french_labels = {
    "Intensity_Per_Route": "Intensité (CO₂ / Route)",
    col_pollution: "Émissions Totales (Tonnes CO₂)",
    "Total_Routes": "Nombre de Routes Aériennes",
    "continent": "Continent", "Entity": "Pays", "Year": "Année"
}

fig = px.scatter(df_clean, 
                 x="Intensity_Per_Route", 
                 y=col_pollution, 
                 animation_frame="Year", 
                 animation_group="Entity",
                 facet_col="continent", 
                 size="Taille_Ajustee", 
                 size_max=40, 
                 hover_data={
                     "Taille_Ajustee": False, 
                     "Total_Routes": True,  
                     "Entity": True,
                     "continent": False,      
                 },
                 color="continent",
                 color_discrete_map=neon_colors,
                 hover_name="Entity",
                 labels=french_labels,
                 log_x=True, 
                 log_y=True,
                 range_x=[1000, 50_000], 
                 range_y=[20000, 300_000_000],
                 title="<b>EMPREINTE CARBONE DE L'AVIATION MONDIALE</b>"
                 )

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a2e',
    plot_bgcolor="#131322",
    margin=dict(t=80, b=60, l=20, r=20),  # b=60 pour laisser place au titre X global
    legend=dict(orientation="h", y=1.1, title=None),
    showlegend=False
)

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_xaxes(showgrid=True, gridcolor='#333', title=None)  # Supprime les titres X individuels
fig.update_yaxes(showgrid=True, gridcolor='#333')

# Ajoute un titre X unique et centré en bas
fig.add_annotation(
    text="Intensité (CO₂ / Route)",
    xref="paper", yref="paper",
    x=0.5, y=-0.15,
    showarrow=False,
    font=dict(size=12, color='white')
)



mon_hovertemplate = (
    "<b>%{hovertext}</b><br>" +
    "<br>" +
    "Intensité: %{x:,.0f} (CO₂/Route)<br>" +
    "Émissions: %{y:.3s} Tonnes<br>" +
    "Routes: %{customdata[1]:,.0f}<br>" +  
    "<extra></extra>"
)

fig.update_traces(
    hovertemplate=mon_hovertemplate,
    marker=dict(sizemin=0.1, line=dict(width=0.5, color='white'), opacity=0.9)
)

for frame in fig.frames:
    for data in frame.data:
        data.hovertemplate = mon_hovertemplate
        data.marker.line.width = 0.5
        data.marker.line.color = 'white'
        data.marker.opacity = 0.9


def get_aviation_chart_component():
    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False, 'staticPlot': False},
            style={'width': '100%', 'height': '100%'}
        )
    ], style={
        'height': '100%', 
        'width': '100%',
        'display': 'flex',
        'alignItems': 'center',    
        'justifyContent': 'center',
        'padding': '0'
    })

# Génération HTML pour vérification
#pio.write_html(fig, file='pollution_final_fixed_years.html', auto_open=True, include_plotlyjs='cdn')