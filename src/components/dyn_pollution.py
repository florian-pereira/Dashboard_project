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
df = pd.read_csv(path_pollution)
path_airports = os.path.join(current_dir, '..', '..', 'data', 'cleaned', 'airports_cleaned.csv')
df_airports = pd.read_csv(path_airports)



df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df = df.dropna(subset=['Year'])
df['Year'] = df['Year'].astype(int)


#annee_max = df['Year'].max()
#print(f"INFO: L'année maximale détectée dans le fichier CSV est : {annee_max}")

# Calcul des routes 
df_routes = df_airports.groupby('Country')['Route_Count'].sum().reset_index()
df_routes.rename(columns={'Route_Count': 'Total_Routes'}, inplace=True)

# Mapping Continents
continent_map = get_continent_mapping()
df['continent'] = df['Entity'].map(continent_map)
blacklist = ['World', 'Africa', 'Asia', 'Europe', 'Oceania', 'South America', 'North America', 'European Union (28)']
df_clean = df[~df['Entity'].isin(blacklist)].copy()
df_clean = df_clean.dropna(subset=['continent'])

df_clean = pd.merge(df_clean, df_routes, left_on='Entity', right_on='Country', how='left')
df_clean = df_clean.dropna(subset=['Total_Routes'])
df_clean = df_clean[df_clean['Total_Routes'] > 0] # Sécurité supplémentaire

all_years = range(df_clean['Year'].min(), df_clean['Year'].max() + 1)
all_countries = df_clean['Entity'].unique()

full_index = pd.MultiIndex.from_product([all_countries, all_years], names=['Entity', 'Year'])

df_clean = df_clean.set_index(['Entity', 'Year']).reindex(full_index).reset_index()


cols_to_fill = ['continent', 'Total_Routes', "Total annual CO₂ emissions from aviation"]
df_clean[cols_to_fill] = df_clean.groupby('Entity')[cols_to_fill].ffill()
df_clean = df_clean.dropna(subset=["Total annual CO₂ emissions from aviation"])


col_pollution = "Total annual CO₂ emissions from aviation"
df_clean['Intensity_Per_Route'] = df_clean[col_pollution] / df_clean['Total_Routes']

# Traduction Française forcée
traduction_continents = {
    'Asia': 'Asie', 'Europe': 'Europe', 'Americas': 'Amériques',
    'Africa': 'Afrique', 'Oceania': 'Océanie'
}
df_clean['continent'] = df_clean['continent'].replace(traduction_continents)

df_clean['Taille_Ajustee'] = np.sqrt(df_clean['Total_Routes'])
#df_clean['Taille_Ajustee'] = df_clean['Total_Routes']

#GRAPHIQUE
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
                 size_max=45, 
                 hover_data={
                     "Taille_Ajustee": False, # On cache la valeur de calcul
                     "Total_Routes": True,    # On montre la vraie valeur
                     "Entity": False,
                     "continent": False,      
                 },

                 color="continent",
                 color_discrete_map=neon_colors,
                 hover_name="Entity",
                 labels=french_labels,
                 log_x=True, 
                 log_y=True,
                 #range_x=[1000, 50_000], 
                 #range_y=[20000, 300_000_000],
                 range_x=[500, 70_000], 
                 range_y=[5000, 500_000_000], 
                 title="<b>PROFIL DE L'AVIATION MONDIALE</b>"#<br><span style='font-size: 14px; color: #aaa;'>X = Intensité (émissions de CO₂ / route) | Y = Pollution Totale  | Taille = Nombre de routes par pays</span>"
                 )

# --- 8. STYLE ---
fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a2e',
    plot_bgcolor="#131322",
    margin=dict(t=80, b=20, l=20, r=20),
    legend=dict(orientation="h", y=1.1, title=None)
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_xaxes(showgrid=True, gridcolor='#333')
fig.update_yaxes(showgrid=True, gridcolor='#333')

fig.update_traces(marker=dict(sizemin=0.1, line=dict(width=0.5, color='white'), opacity=0.9))




#////////////

def get_aviation_chart_component():
    """
    Cette fonction sera appelée par ton Dashboard principal.
    Elle retourne le layout HTML/CSS prêt à l'emploi.
    """
    return html.Div([
        dcc.Graph(
            figure=fig, 
            config={'displayModeBar': False, 'staticPlot': False},
            style={'width': '100%', 'height': '100%'} # Remplit le conteneur parent
        )
    ], style={
        'height': '100%', 
        'width': '100%',
        'display': 'flex',
        'alignItems': 'center',     # Centrage Vertical
        'justifyContent': 'center', # Centrage Horizontal
        'padding': '0'
    })




fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='#1a1a2e',
    plot_bgcolor="#131322",
    margin=dict(t=80, b=20, l=20, r=20),
    legend=dict(orientation="h", y=1.1, title=None),
    showlegend=False
)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_xaxes(showgrid=True, gridcolor='#333')
fig.update_yaxes(showgrid=True, gridcolor='#333')

fig.update_traces(marker=dict(sizemin=4, line=dict(width=0.5, color='white'), opacity=0.7))

pio.write_html(fig, file='pollution_final_fixed_years.html', auto_open=True, include_plotlyjs='cdn')
