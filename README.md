# ✈️ SkyDash : Visualisation du Trafic Aérien & Infrastructures

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Dash](https://img.shields.io/badge/Dash-2.0%2B-orange)
![OpenData](https://img.shields.io/badge/Data-OpenSky-green)

## 📋 Description du Projet

Ce projet a été réalisé dans le cadre de l'unité **"Le projet Data"** à l'ESIEE Paris. L'objectif est de développer un dashboard interactif permettant d'analyser le transport aérien sous deux angles :

1.  **Vision Dynamique (Temps Réel) :** Visualisation des avions en vol au-dessus de la France à l'instant T.
2.  **Vision Structurelle (Statique) :** Analyse de la répartition et de l'importance des aéroports internationaux à travers le monde.

L'application est construite en **Python** et utilise la librairie **Dash** (Plotly) pour les visualisations graphiques.

## 🎯 Fonctionnalités Clés

* **Carte Live (France) :** Localisation précise des avions, affichage du cap, de l'altitude et de la vitesse (Données API OpenSky).
* **Carte Mondiale des Aéroports :** Visualisation des grands hubs internationaux filtrables par trafic.
* **Statistiques :** Histogrammes dynamiques sur la répartition des altitudes et des types d'avions.
* **Mise à jour automatique :** Le module de récupération de données permet de rafraîchir les positions sans redémarrer le serveur.

## 💾 Données Utilisées

Le projet s'appuie sur des données **Open Data** accessibles publiquement :

### 1. Données Dynamiques (Live)
* **Source :** [OpenSky Network API](https://opensky-network.org)
* **Utilisation :** Récupération des vecteurs d'état (Position, Vitesse, Altitude) pour les vols au-dessus de la France.
* **Script :** `src/utils/get_data.py`

### 2. Données Statiques (Infrastructure)
* **Source :** [OurAirports / OpenFlights](https://davidmegginson.github.io/ourairports-data/)
* **Utilisation :** Base de données des aéroports (Localisation, Code IATA, Type) pour l'analyse structurelle.
* **Script :** Stocké dans `data/raw/` et nettoyé via `src/utils/clean_data.py`.

## 🛠️ Architecture Technique

Le code respecte une architecture modulaire MVC (Modèle-Vue-Contrôleur) pour faciliter la maintenance et le travail collaboratif :

```text
data_project/
├── main.py                  # Point d'entrée de l'application
├── config.py                # Configuration globale (URLs, Chemins)
├── data/                    # Stockage des données (Raw vs Cleaned)
└── src/
    ├── utils/               # Scripts backend (API, Nettoyage)
    ├── components/          # Composants graphiques réutilisables
    └── pages/               # Mises en page des différentes vues

1. La Racine (L'Administration du Projet)
C'est le "quartier général". On y trouve les fichiers de configuration et le point de lancement.

main.py (Le Chef d'Orchestre)

Contenu : Il initialise l'application Dash, charge le style CSS (Bootstrap) et définit la structure globale (Barre de navigation + Contenu de la page).

Pourquoi ? Le prof a demandé de lancer le projet via python main.py. Ce fichier doit être court et propre. Il ne contient pas de calculs complexes, il se contente d'appeler les autres fichiers.

config.py (Le Tableau de Bord)

Contenu : Les variables globales : chemins des dossiers (DATA_DIR), URLs des API, clés secrètes si besoin.

Pourquoi ? Si demain l'URL de l'API change ou si tu changes d'ordinateur (Mac vs Windows), tu modifies juste une ligne ici au lieu de chercher dans 50 fichiers.

requirements.txt (La Liste de Courses)

Contenu : La liste des librairies (pandas, dash, etc.).

Pourquoi ? Indispensable pour que le prof puisse installer ton projet sur sa machine.

.gitignore (Le Videur)

Contenu : Liste des fichiers à ne pas envoyer sur GitHub (comme .venv).

Pourquoi ? Garder le dépôt propre et léger.

2. Le Dossier data/ (Le Carburant)
C'est ici que sont stockées les informations. Il est divisé en deux états.

data/raw/ (Le Brut)

Contenu : Les fichiers CSV/JSON tels qu'ils sortent exactement de l'API ou du téléchargement.

Pourquoi ? Si tu fais une erreur dans ton nettoyage, tu peux toujours revenir à la source originale sans avoir à re-télécharger. C'est ta sauvegarde de sécurité.

data/cleaned/ (Le Propre)

Contenu : Les fichiers CSV prêts à l'emploi (colonnes renommées, dates formatées, valeurs nulles supprimées).

Pourquoi ? Le Dashboard doit être rapide. Il ne doit pas recalculer le nettoyage à chaque fois qu'un utilisateur clique. Il lit directement le fichier propre.

3. Le Dossier src/utils/ (La Mécanique / Le Backend)
C'est le moteur caché sous le capot. Ici, pas de graphiques, juste du code Python pur.

get_data.py (Le Chasseur)

Contenu : Le code qui se connecte à l'API OpenSky, télécharge les données et les écrit dans data/raw.

Pourquoi ? C'est une exigence explicite du sujet. Il gère les problèmes de connexion Internet.

clean_data.py (Le Nettoyeur)

Contenu : Le code qui lit data/raw, fusionne les avions avec les aéroports, corrige les erreurs et sauvegarde dans data/cleaned.

Pourquoi ? Pour séparer la récupération (Internet) du traitement (CPU).

4. Le Dossier src/components/ (Les Briques LEGO)
Ce sont des morceaux d'interface réutilisables.

header.py / navbar.py

Contenu : Le code de la barre de menu en haut.

Pourquoi ? Si tu veux changer le titre du site, tu le fais ici une seule fois, et ça se met à jour sur toutes les pages.

map_view.py (Exemple de composant)

Contenu : La fonction qui génère la carte Plotly.

Pourquoi ? Le code d'une carte est souvent long (50-100 lignes). Si tu le mets directement dans la page, le code devient illisible. On l'isole ici.

5. Le Dossier src/pages/ (Les Écrans)
C'est l'assemblage final que voit l'utilisateur.

home.py

Contenu : Importe la navbar, importe la carte mondiale depuis components, et les dispose à l'écran (html.Div, dbc.Row).

france_live.py

Contenu : La page spécifique pour la France.

Pourquoi ? Dash permet de créer des applications "Multi-pages". Chaque fichier ici correspond à une URL différente (/home, /france).
