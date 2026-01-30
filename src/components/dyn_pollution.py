import plotly.express as px
import os
import pandas as pd
import numpy as np
from dash import dcc, html

# --- 1. LES FONCTIONS UTILITAIRES (Restent en dehors) ---
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

# --- 2. FONCTION DE CRÉATION DE LA FIGURE (Tout est encapsulé ici) ---
def create_figure():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_pollution = os.path.join(current_dir, '..', '..', 'data', 'cleaned', 'annual-co-emissions-from-aviation.csv')
    path_airports = os.path.join(current_dir, '..', '..', 'data', 'cleaned', 'airports_cleaned.csv')
    
    # Lecture
    df = pd.read_csv(path_pollution)
    df_airports = pd.read_csv(path_airports)

    # Nettoyage
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df = df.dropna(subset=['Year'])
    df['Year'] = df['Year'].astype(int)

    # Calcul des routes 
    df_routes = df_airports.groupby('Country')['Route_Count'].sum().reset_index()
    df_routes.rename(columns={'Route_Count': 'Total_Routes'}, inplace=True)

    # Mapping Continents
    continent_map = get_continent_mapping()
    df['continent'] = df['Entity'].map(continent_map)
    blacklist = ['World', 'Africa', 'Asia', 'Europe', 'Oceania', 'South America', 'North America', 'European Union (28)']
    df_clean = df[~df['Entity'].isin(blacklist)].copy()
    df_clean = df_clean.dropna(subset=['continent'])

    # Fusion
    df_clean = pd.merge(df_clean, df_routes, left_on='Entity', right_on='Country', how='left')
    df_clean = df_clean.dropna(subset=['Total_Routes'])

    all_years = range(df_clean['Year'].min(), df_clean['Year'].max() + 1)
    all_countries = df_clean['Entity'].unique()

    full_index = pd.MultiIndex.from_product([all_countries, all_years], names=['Entity', 'Year'])

    df_clean = df_clean.set_index(['Entity', 'Year']).reindex(full_index).reset_index()

    cols_to_fill = ['continent', 'Total_Routes', "Total annual CO₂ emissions from aviation"]
    df_clean[cols_to_fill] = df_clean.groupby('Entity')[cols_to_fill].ffill()
    df_clean = df_clean.dropna(subset=["Total annual CO₂ emissions from aviation"])

    col_pollution = "Total annual CO₂ emissions from aviation"
    df_clean['Intensity_Per_Route'] = df_clean[col_pollution] / df_clean['Total_Routes']

    # Traduction
    traduction_continents = {
        'Asia': 'Asie', 'Europe': 'Europe', 'Americas': 'Amériques',
        'Africa': 'Afrique', 'Oceania': 'Océanie'
    }
    df_clean['continent'] = df_clean['continent'].replace(traduction_continents)
    df_clean['Taille_Ajustee'] = np.sqrt(df_clean['Total_Routes'])

    # GRAPHIQUE
    neon_colors = {'Asie': '#bd93f9', 'Europe': '#ffb86c', 'Amériques': '#50fa7b', 'Afrique': '#ff79c6', 'Océanie': '#8be9fd'}
    french_labels = {
        "Intensity_Per_Route": "Intensité (CO₂ / Route)",
        col_pollution: "Émissions Totales (Tonnes CO₂)",
        "Total_Routes": "Nombre de Routes Aériennes",
        "continent": "Continent", "Entity": "Pays", "Year": "Année"
    }

    # --- DÉBUT MODIFICATION ---
    
    # On raccourcit le titre et on réduit la taille du sous-titre HTML (font-size: 10px)
    titre_graphe = "<b>PROFIL AVIATION</b><br><span style='font-size: 10px; color: #aaa;'>Intensité vs Pollution vs Trafic</span>"

    fig = px.scatter(df_clean, 
                     x="Intensity_Per_Route", 
                     y=col_pollution, 
                     animation_frame="Year", 
                     animation_group="Entity",
                     facet_col="continent", 
                     size="Taille_Ajustee", 
                     size_max=40, # J'ai réduit un peu la taille max des bulles aussi (50 -> 40)
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
                     range_x=[100, 500_000], 
                     range_y=[5000, 1000_000_000], 
                     title=titre_graphe
                     )

    # --- STYLE MINIMALISTE & PETIT ---
    # --- STYLE MINIMALISTE & SANS LÉGENDE ---
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='#1a1a2e',
        plot_bgcolor="#131322",
        
        # On supprime totalement la légende (les ronds de couleur à droite)
        showlegend=False,  # <--- C'EST ICI QUE ÇA SE PASSE

        # Réduction des marges
        margin=dict(t=60, b=10, l=10, r=10),
        
        # Police Globale par défaut (petite)
        font=dict(family="Segoe UI, sans-serif", size=10, color="#ffffff"),
        
        # Titre principal
        title=dict(font=dict(size=14), x=0.05, y=0.95),
    )

    # Réduction de la taille des noms des continents (Annotations)
    fig.for_each_annotation(lambda a: a.update(
        text=a.text.split("=")[-1],
        font=dict(size=11, color="white") # Taille des titres "Europe", "Asie"...
    ))

    # Configuration des Axes (Titres et Chiffres plus petits)
    axis_style = dict(
        showgrid=True, 
        gridcolor='#333',
        title_font=dict(size=10), # Taille "Intensité..."
        tickfont=dict(size=8)     # Taille des chiffres "100", "1k"...
    )
    
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)

    fig.update_traces(marker=dict(sizemin=1, line=dict(width=0.5, color='white'), opacity=0.8))
    
    return fig
    

# --- 3. EXPORT POUR DASH ---
def get_aviation_chart_component():
    
    # On génère la figure uniquement à la demande
    fig = create_figure()
    
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