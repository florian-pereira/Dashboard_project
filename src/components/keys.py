from dash import html

def render():
    # Style du conteneur : vertical (column) avec de l'espace entre les cartes
    container_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '15px',          # Espace entre les blocs
        'padding': '5px 0'     # Petit padding haut/bas
    }

    # Fonction pour générer une carte KPI avec dégradé
    def create_kpi_card(title, value, gradient_colors):
        return html.Div([
            # Le Titre (en haut, petit, blanc transparent)
            html.P(title, style={
                'color': 'rgba(255, 255, 255, 0.7)', 
                'fontSize': '11px', 
                'textTransform': 'uppercase', 
                'margin': '0',
                'letterSpacing': '1px'
            }),
            # La Valeur (au centre, en gros)
            html.H2(value, style={
                'color': 'white', 
                'fontSize': '26px', 
                'fontWeight': '900', 
                'margin': '5px 0 0 0'
            })
        ], style={
            # L'astuce du dégradé est ici (angle de 135 degrés)
            'background': f'linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]})',
            'borderRadius': '12px',
            'padding': '50px',
            'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.4)', # Ombre portée pour le relief
            'textAlign': 'center',
            'minWidth': '120px',
            'minHeight': '100px'
        })

    # On retourne la colonne de cartes
    return html.Div([
        # Carte 1 : Bleu Électrique / Cyan
        create_kpi_card("Vols Actifs", "125", ["#1d8cf8", "#33d9b2"]),
        
        # Carte 2 : Orange / Jaune
        create_kpi_card("Altitude Moy.", "11 km", ["#ff5252", "#ffb142"]),
        
        # Carte 3 : Violet / Rose
        create_kpi_card("Vitesse Max", "850 km/h", ["#706fd3", "#ff793f"]),
        
        # Carte 4 : (Optionnelle) Turquoise
        create_kpi_card("Destinations", "42", ["#00d2d3", "#54a0ff"])
        
    ], style=container_style)