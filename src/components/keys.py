from dash import html

def render():
    # --- STYLE DU CONTENEUR ---
    container_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'height': '100%',        # <--- CRUCIAL : Prend toute la hauteur de la colonne parente
        'justifyContent': 'space-between', # Répartit les cartes du haut en bas
        'gap': '15px'            # Espace entre les cartes
    }

    # --- FONCTION DE GÉNÉRATION DE CARTE ---
    def create_kpi_card(title, value, gradient_colors):
        return html.Div([
            # Le Titre
            html.P(title, style={
                'color': 'rgba(255, 255, 255, 0.7)', 
                'fontSize': '12px', 
                'textTransform': 'uppercase', 
                'margin': '0',
                'letterSpacing': '1px',
                'fontWeight': '600'
            }),
            # La Valeur
            html.H2(value, style={
                'color': 'white', 
                'fontSize': '28px', 
                'fontWeight': 'bold', 
                'margin': '5px 0 0 0'
            })
        ], style={
            # L'astuce du dégradé
            'background': f'linear-gradient(135deg, {gradient_colors[0]}, {gradient_colors[1]})',
            'borderRadius': '12px',
            'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.4)',
            'textAlign': 'center',
            
            # --- CENTRAGE VERTICAL DU TEXTE ---
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center',
            
            # --- ELASTICITÉ ---
            'flex': '1',         # <--- MAGIQUE : La carte grandit pour remplir l'espace vide
            'minHeight': '0'     # Sécurité pour le flexbox
        })

    # --- RETOUR DU LAYOUT ---
    return html.Div([
        # Carte 1 : Bleu
        create_kpi_card("Vols Actifs", "125", ["#1d8cf8", "#33d9b2"]),
        
        # Carte 2 : Orange
        create_kpi_card("Altitude Moy.", "32k", ["#ff5252", "#ffb142"]),
        
        # Carte 3 : Violet
        create_kpi_card("Vitesse Max", "850", ["#706fd3", "#ff793f"]),
        
    ], style=container_style)