from dash import html
from src.components import keys, map_view, charts, cheeze

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
        # J'ai ajouté 'display': 'flex' ici pour que les 3 blocs soient côte à côte
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
                map_view.render()
            ], style={
                'width': '60%',           
                'minWidth': '0',          
                'overflow': 'hidden',     
                'borderRadius': '12px'    
            }),

            # COL 3 : CAMEMBERT + TEXTE (Reste de la place)
            html.Div([
                
                # BLOC HAUT : Le graphique Camembert (75%)
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

                # BLOC BAS : Le Texte Explicatif (25%)
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
                'width': '28%', # J'ai mis une largeur explicite pour équilibrer (10+60+28+gap = ~100)
                'height': '100%'           
            })

        ], style={
            'display': 'flex',        # <--- INDISPENSABLE pour l'alignement horizontal
            'flexDirection': 'row',   # <--- INDISPENSABLE
            'gap': '20px',            # Espace entre les colonnes
            'height': '550px',        # Hauteur fixe pour forcer la map et le camembert à avoir la même taille
            'marginBottom': '20px',
            'width': '100%'
        }),

        # --- 3. ZONE BASSE (CHARTS) ---
        html.Div([
            html.Div([
                charts.render()
            ], style={
                **CARD_STYLE, 
                'width': '50%', # J'ai remis 100% car 50% ferait bizarre tout seul à gauche
                'boxSizing': 'border-box'
            })
        ])

    ], style={
        'padding': '30px', 
        'backgroundColor': COLORS['background'], 
        'minHeight': '100vh',
        'fontFamily': 'Segoe UI, sans-serif'
    })