from dash import html, dcc
# J'ai ajouté 'aviation_chart' à la liste des imports
from src.components import keys, map_view, charts, cheeze, dyn_pollution

COLORS = {
    'background': '#1e1e2f',
    'card_bg': '#27293d',
    'electric_blue': '#1d8cf8',
    'text': '#ffffff',
    'text_dim': '#9a9a9a'
}

CARD_STYLE = {
    'backgroundColor': COLORS['card_bg'],
    'borderRadius': '12px',
    'padding': '20px',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.5)',
    'marginBottom': '20px',
    'color': COLORS['text']
}

def layout():
    return html.Div([
        
        # --- 0. TIMERS (Pour le temps réel) ---
        dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0),

        # --- 1. INTRODUCTION (En-tête) ---
        html.Div([
            html.H1("Trafic Aérien", 
                    style={'color': COLORS['text'], 'fontWeight': 'bold', 'marginBottom': '10px'}),
            
            html.Div([
                html.H4("Visualisation des flux et enjeux écologiques", style={'color': COLORS['electric_blue'], 'marginBottom': '10px'}),
                html.P(
                    "Ce tableau de bord offre une vision en temps réel de l'activité aéronautique mondiale. "
                    "Conçu dans un cadre académique, il dépasse la simple surveillance : il vise à illustrer "
                    "la saturation du ciel et la pollution atmosphérique qui en découle. En croisant la densité "
                    "du trafic avec sa répartition géographique, cet outil permet de mieux saisir l'ampleur "
                    "de l'empreinte écologique laissée par le transport aérien.",
                    style={'color': COLORS['text_dim'], 'fontSize': '14px', 'margin': '0'}
                )
            ], style={**CARD_STYLE, 'borderLeft': f'5px solid {COLORS["electric_blue"]}', 'paddingLeft': '30px', 'minHeight': '100px'})
        ], style={'width': '100%', 'marginBottom': '20px'}),

        # --- 2. ZONE PRINCIPALE (LIGNE DU MILIEU) ---
        html.Div([
            
            # COL 1 : KPIs (10%)
            html.Div([
                keys.render()
            ], style={
                'width': '10%',           
                'minWidth': '10%',        
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'space-between' 
            }),

            # COL 2 : MAP (60%)
            html.Div([
                map_view.render() # Si render() renvoie un Graph direct, c'est bon. Sinon attention aux IDs.
            ], style={
                'width': '60%',           
                'minWidth': '0',          
                'overflow': 'hidden',     
                'borderRadius': '12px'    
            }),

            # COL 3 : CAMEMBERT + TEXTE (28%)
            html.Div([
                
                # BLOC HAUT : Le graphique Camembert
                html.Div([
                    cheeze.render()
                ], style={
                    'flex': '3', 
                    'backgroundColor': COLORS['card_bg'],
                    'borderRadius': '12px',
                    'padding': '10px',
                    'overflow': 'hidden',
                    'position': 'relative'
                }),

                # BLOC BAS : Le Texte Explicatif
                html.Div([
                    html.H5("Note Méthodologique", 
                            style={
                                'color': COLORS['electric_blue'], 
                                'fontWeight': 'bold', 
                                'marginBottom': '5px', 
                                'marginTop': '0', 
                                'fontSize': '12px'
                            }),
                    
                    html.P(
                        "La prédominance apparente de l'Europe reflète une densité optimale de capteurs." \
                        " À l'inverse, les zones blanches ont des causes distinctes : un déficit d'infrastructures en Afrique," \
                        " opposé à des restrictions gouvernementales et militaires en Asie. L'analyse doit également tenir compte du décalage horaire.",
                        style={
                            'color': COLORS['text_dim'], 
                            'fontSize': '10px', 
                            'marginBottom': '6px', 
                            'lineHeight': '1.3',
                            'textAlign': 'justify'
                        }
                    ),
                    
                    html.P(
                        "Performance : Pour garantir la fluidité temps-réel, les données visualisées sont ici restreintes aux avions français.",
                        style={
                            'color': COLORS['text_dim'],
                            'fontSize': '9px', 
                            'margin': '0', 
                            'fontStyle': 'italic',
                            'opacity': '0.8'
                        }
                    )

                ], style={
                    'flex': '1', 
                    'backgroundColor': COLORS['card_bg'],
                    'borderRadius': '12px',
                    'padding': '12px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                })

            ], style={
                'display': 'flex',
                'flexDirection': 'column', 
                'gap': '20px',             
                'width': '28%', 
                'height': '100%'           
            })

        ], style={
            'display': 'flex',        
            'flexDirection': 'row',   
            'gap': '20px',            
            'height': '550px',        
            'marginBottom': '20px',
            'width': '100%'
        }),

        # --- 3. ZONE BASSE (CHARTS CÔTE À CÔTE) ---
        html.Div([
            
            # Bloc Gauche (Graphique + Texte explicatif) - 40%
            html.Div([
                
                # BLOC HAUT : Le graphique histogramme
                html.Div([
                    charts.render()
                ], style={
                    'height': '350px',
                    'backgroundColor': COLORS['card_bg'],
                    'borderRadius': '12px',
                    'padding': '10px',
                    'overflow': 'hidden'
                }),
                
                # BLOC BAS : Texte explicatif
                html.Div([
                    html.H5("Lecture des Graphiques", 
                            style={
                                'color': COLORS['electric_blue'], 
                                'fontWeight': 'bold', 
                                'marginBottom': '5px', 
                                'marginTop': '0', 
                                'fontSize': '12px'
                            }),
                    
                    html.P(
                        "Altitudes : La distribution des altitudes révèle deux pics. Le premier correspond à la phase de montée et descente, "
                        "le second à l'altitude de croisière (9-12km). Les long-courriers privilégient les hautes altitudes pour réduire la consommation.",
                        style={
                            'color': COLORS['text_dim'], 
                            'fontSize': '10px', 
                            'marginBottom': '6px', 
                            'lineHeight': '1.3',
                            'textAlign': 'justify'
                        }
                    ),
                    
                    html.P(
                        "Empreinte Carbone : Chaque bulle représente un pays positionné selon deux critères. "
                        "L'axe horizontal indique l'intensité polluante, c'est-à-dire la quantité de CO₂ émise par route aérienne. "
                        "L'axe vertical montre les émissions totales du pays. La taille des bulles reflète le nombre de routes aériennes. "
                        "Ainsi, un pays situé en bas à gauche possède peu de liaisons et génère peu de pollution, comme les petites nations insulaires. "
                        "À l'inverse, un pays en haut à droite cumule un réseau aérien dense et des émissions massives, à l'image des États-Unis ou de la Chine.",
                        style={
                            'color': COLORS['text_dim'], 
                            'fontSize': '10px', 
                            'marginBottom': '6px', 
                            'lineHeight': '1.3',
                            'textAlign': 'justify'
                        }
                    ),
                    
                    html.P(
                        "Entre 1990 et 2019, on observe une progression constante des émissions portée par la mondialisation, "
                        "l'essor du tourisme de masse et la multiplication des compagnies low-cost. Cette croissance s'interrompt brutalement "
                        "en 2020-2021 avec la pandémie de COVID-19 : les fermetures de frontières et l'immobilisation des flottes provoquent "
                        "une chute historique. Dès 2022, la reprise du trafic confirme la dépendance mondiale au transport aérien.",
                        style={
                            'color': COLORS['text_dim'],
                            'fontSize': '10px', 
                            'margin': '0', 
                            'lineHeight': '1.3',
                            'textAlign': 'justify'
                        }
                    )

                ], style={
                    'flex': '1',
                    'backgroundColor': COLORS['card_bg'],
                    'borderRadius': '12px',
                    'padding': '12px',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center'
                })
                
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'gap': '15px',
                'width': '40%',
                'height': '100%',
                'boxSizing': 'border-box'
            }),

            # Bloc Droite (NOUVEAU : Profil Aviation Mondiale) - 60%
            html.Div([
                dyn_pollution.get_aviation_chart_component()
            ], style={
                **CARD_STYLE,
                'width': '60%',
                'marginBottom': '0',
                'boxSizing': 'border-box',
                'overflow': 'hidden' # Pour éviter que le graph ne dépasse
            })

        ], style={
            'display': 'flex',      # Active l'alignement horizontal
            'flexDirection': 'row', 
            'gap': '20px',          # Espace entre les deux graphiques
            'width': '100%',
            'height': '520px'       # Hauteur fixe pour la zone basse
        })

    ], style={
        'padding': '30px', 
        'backgroundColor': COLORS['background'], 
        'minHeight': '100vh',
        'fontFamily': 'Segoe UI, sans-serif'
    })