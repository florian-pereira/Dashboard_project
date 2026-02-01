"""
Page principale du dashboard.

Définit la structure et la mise en page de l'interface utilisateur
en assemblant les différents composants visuels (carte, graphiques, KPIs).
Le layout utilise une organisation en grille Flexbox pour une
disposition  des éléments.
"""

from dash import html, dcc
from src.components import keys, map_view, charts, cheeze, dyn_pollution

# Définition de la palette de couleurs centralisée.
# Cela permet de changer le thème de tout le dashboard en modifiant simplement ces valeurs ici,
# garantissant une cohérence visuelle sur toute la page.
COLORS = {
    "background": "#1e1e2f",
    "card_bg": "#27293d",
    "electric_blue": "#1d8cf8",
    "text": "#ffffff",
    "text_dim": "#9a9a9a",
}

# Définition d'un style de base réutilisable pour les "cartes" (conteneurs).
# Au lieu de répéter les mêmes propriétés CSS pour chaque div, on utilise ce dictionnaire.
CARD_STYLE = {
    "backgroundColor": COLORS["card_bg"],  # Couleur de fond des cartes
    "borderRadius": "12px",  # Arrondit les bords des cartes
    "padding": "20px",  # Ajoute de l'espace à l'intérieur de la carte
    "boxShadow": "0 4px 20px rgba(0,0,0,0.5)",  # Ajoute une ombre portée pour l'effet de profondeur
    "marginBottom": "20px",  # Ajoute une marge en bas pour séparer les éléments
    "color": COLORS["text"],  # Couleur du texte
}


def layout():
    """
    Définit la structure principale de la page d'accueil du Dashboard.

    Cette fonction assemble tous les composants visuels (Graphiques, Cartes, KPIs)
    dans une mise en page réactive basée sur Flexbox.

    Returns:
        html.Div: Le conteneur racine de la page.
    """
    return html.Div(
        [
            # LE TITRE ET INTRODUCTION
            html.Div(
                [
                    html.H1(
                        "Trafic Aérien",
                        style={
                            "color": COLORS["text"],
                            "fontWeight": "bold",
                            "marginBottom": "10px",
                        },
                    ),  # Titre en gras avec une marge en bas
                    html.Div(
                        [
                            html.H4(
                                "Visualisation des flux et enjeux écologiques",
                                style={
                                    "color": COLORS["electric_blue"],
                                    "marginBottom": "10px",
                                },
                            ),  # Sous-titre en bleu électrique
                            html.P(
                                "Ce tableau de bord offre une vision en temps réel de l'activité aéronautique mondiale. "
                                "Conçu dans un cadre académique, il dépasse la simple surveillance : il vise à illustrer "
                                "la saturation du ciel et la pollution atmosphérique qui en découle. En croisant la densité "
                                "du trafic avec sa répartition géographique, cet outil permet de mieux saisir l'ampleur "
                                "de l'empreinte écologique laissée par le transport aérien.",
                                style={
                                    "color": COLORS["text_dim"],
                                    "fontSize": "14px",
                                    "margin": "0",
                                },  # Texte gris clair, taille 14px, sans marge
                            ),
                        ],
                        style={
                            **CARD_STYLE,
                            "borderLeft": f"5px solid {COLORS['electric_blue']}",
                            "paddingLeft": "30px",
                            "minHeight": "100px",
                        },
                    ),  # Ajoute une bordure bleue à gauche du texte
                ],
                style={"width": "100%", "marginBottom": "20px"},
            ),  # Le conteneur prend toute la largeur
            # PARTIE CENTRALE
            html.Div(
                [
                    # COLONNE 1 : Les chiffres clés
                    html.Div(
                        [keys.render()],
                        style={
                            "width": "10%",  # Occupe 10% de la largeur
                            "minWidth": "10%",  # Largeur minimum de 10% pour ne pas être écrasé
                            "display": "flex",  # Utilise flexbox pour aligner le contenu
                            "flexDirection": "column",
                            "justifyContent": "space-between",  # Espacement égal entre les éléments
                        },
                    ),
                    # COLONNE 2 : La Carte
                    html.Div(
                        [map_view.render()],
                        style={
                            "width": "60%",  # La carte prend 60% de la largeur (élément principal)
                            "minWidth": "0",  # Permet au contenu de rétrécir si nécessaire
                            "overflow": "hidden",  # Cache ce qui dépasse du conteneur
                            "borderRadius": "12px",  # Arrondit les coins de la carte
                        },
                    ),
                    # COLONNE 3 : Droite
                    html.Div(
                        [
                            # Graphique Camembert (en haut)
                            html.Div(
                                [cheeze.render()],
                                style={
                                    "flex": "3",  # Prend 3 parts de l'espace vertical disponible
                                    "backgroundColor": COLORS["card_bg"],  # Fond sombre
                                    "borderRadius": "12px",  # Coins arrondis
                                    "padding": "10px",  # Marge interne
                                    "overflow": "hidden",  # Coupe ce qui dépasse
                                    "position": "relative",  # Nécessaire pour le positionnement absolu interne
                                },
                            ),
                            # Texte explicatif (en bas)
                            html.Div(
                                [
                                    html.H5(
                                        "Note Méthodologique",
                                        style={
                                            "color": COLORS["electric_blue"],
                                            "fontWeight": "bold",
                                            "marginBottom": "5px",
                                            "marginTop": "0",
                                            "fontSize": "12px",
                                        },
                                    ),
                                    html.P(
                                        "La prédominance apparente de l'Europe reflète une densité optimale de capteurs."
                                        " À l'inverse, les zones blanches ont des causes distinctes : un déficit d'infrastructures en Afrique,"
                                        " opposé à des restrictions gouvernementales et militaires en Asie. L'analyse doit également tenir compte du décalage horaire.",
                                        style={
                                            "color": COLORS["text_dim"],
                                            "fontSize": "10px",
                                            "marginBottom": "6px",
                                            "lineHeight": "1.3",  # Espacement entre les lignes pour la lisibilité
                                            "textAlign": "justify",  # Justifie le texte pour qu'il soit carré
                                        },
                                    ),
                                    html.P(
                                        "Performance : Pour garantir la fluidité temps-réel, les données visualisées sont ici restreintes aux avions français.",
                                        style={
                                            "color": COLORS["text_dim"],
                                            "fontSize": "9px",
                                            "margin": "0",
                                            "fontStyle": "italic",  # Texte en italique
                                            "opacity": "0.8",  # Légèrement transparent
                                        },
                                    ),
                                ],
                                style={
                                    "flex": "1",  # Prend 1 part de l'espace vertical (donc 1/4 du total car l'autre a 3)
                                    "backgroundColor": COLORS["card_bg"],
                                    "borderRadius": "12px",
                                    "padding": "12px",
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "center",  # Centre le contenu verticalement
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "20px",  # Espace de 20px entre le camembert et le texte
                            "width": "28%",  # Prend 28% de la largeur (total 10+60+28 env. 100%)
                            "height": "100%",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "row",  # Alignement horizontal des 3 colonnes principales
                    "gap": "20px",  # Espace entre les colonnes
                    "height": "550px",  # Hauteur fixe pour cette section
                    "marginBottom": "20px",
                    "width": "100%",
                },
            ),
            # ZONE BASSE
            html.Div(
                [
                    # Bloc Gauche (Graphique + Texte explicatif) - 40%
                    html.Div(
                        [
                            # BLOC HAUT : Le graphique histogramme
                            html.Div(
                                [charts.render()],
                                style={
                                    "height": "350px",  # Fixe la hauteur de l'histogramme
                                    "backgroundColor": COLORS["card_bg"],
                                    "borderRadius": "12px",
                                    "padding": "10px",
                                    "overflow": "hidden",
                                },
                            ),
                            # BLOC BAS : Texte explicatif
                            html.Div(
                                [
                                    html.H5(
                                        "Lecture des Graphiques",
                                        style={
                                            "color": COLORS["electric_blue"],
                                            "fontWeight": "bold",
                                            "marginBottom": "5px",
                                            "marginTop": "0",
                                            "fontSize": "12px",
                                        },
                                    ),
                                    html.P(
                                        "Altitudes : La distribution des altitudes révèle deux pics. Le premier correspond à la phase de montée et descente, "
                                        "le second à l'altitude de croisière (9-12km). Les long-courriers privilégient les hautes altitudes pour réduire la consommation.",
                                        style={
                                            "color": COLORS["text_dim"],
                                            "fontSize": "10px",
                                            "marginBottom": "6px",
                                            "lineHeight": "1.3",
                                            "textAlign": "justify",  # aligne le texte à la fois sur la marge de gauche et sur la marge de droite
                                        },
                                    ),
                                    html.P(
                                        "Empreinte Carbone : Chaque bulle représente un pays positionné selon deux critères. "
                                        "L'axe horizontal indique l'intensité polluante, c'est-à-dire la quantité de CO₂ émise par route aérienne. "
                                        "L'axe vertical montre les émissions totales du pays. La taille des bulles reflète le nombre de routes aériennes. "
                                        "Ainsi, un pays situé en bas à gauche possède peu de liaisons et génère peu de pollution, comme les petites nations insulaires. "
                                        "À l'inverse, un pays en haut à droite cumule un réseau aérien dense et des émissions massives, à l'image des États-Unis ou de la Chine.",
                                        style={
                                            "color": COLORS["text_dim"],
                                            "fontSize": "10px",
                                            "marginBottom": "6px",
                                            "lineHeight": "1.3",
                                            "textAlign": "justify",
                                        },
                                    ),
                                    html.P(
                                        "Entre 1990 et 2019, on observe une progression constante des émissions portée par la mondialisation, "
                                        "l'essor du tourisme de masse et la multiplication des compagnies low-cost. Cette croissance s'interrompt brutalement "
                                        "en 2020-2021 avec la pandémie de COVID-19 : les fermetures de frontières et l'immobilisation des flottes provoquent "
                                        "une chute historique. Dès 2022, la reprise du trafic confirme la dépendance mondiale au transport aérien.",
                                        style={
                                            "color": COLORS["text_dim"],
                                            "fontSize": "10px",
                                            "margin": "0",
                                            "lineHeight": "1.3",
                                            "textAlign": "justify",
                                        },
                                    ),
                                ],
                                style={
                                    "flex": "1",  # Prend l'espace restant en dessous de l'histogramme
                                    "backgroundColor": COLORS["card_bg"],
                                    "borderRadius": "12px",
                                    "padding": "12px",
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "center",  # Centre verticalement le texte
                                },
                            ),
                        ],
                        style={
                            "display": "flex",
                            "flexDirection": "column",
                            "gap": "15px",  # Espace entre l'histogramme et le texte explicatif
                            "width": "40%",  # Occupe 40% de la largeur totale
                            "height": "100%",
                            "boxSizing": "border-box",
                        },
                    ),
                    # Bloc Droite - 60%
                    html.Div(
                        [dyn_pollution.get_aviation_chart_component()],
                        style={
                            **CARD_STYLE,
                            "width": "60%",  # Occupe 60% de la largeur restante
                            "marginBottom": "0",  # Pas de marge extra en bas
                            "boxSizing": "border-box",
                            "overflow": "hidden",  # Pour éviter que le graph ne dépasse
                        },
                    ),
                ],
                style={
                    "display": "flex",  # Active l'alignement horizontal
                    "flexDirection": "row",
                    "gap": "20px",  # Espace entre les deux graphiques
                    "width": "100%",
                    "height": "520px",  # Hauteur fixe pour la zone basse
                },
            ),
        ],
        style={
            "padding": "30px",  # Ajoute de l'espace autour du contenu principal
            "backgroundColor": COLORS["background"],  # Couleur de fond de toute la page
            "minHeight": "100vh",  # La page prend au moins toute la hauteur de l'écran
            "fontFamily": "Segoe UI, sans-serif",  # Police d'écriture utilisée
        },
    )
