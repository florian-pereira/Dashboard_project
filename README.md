# ✈️ Dashboard Analyse Trafic Aérien & Impact Environnemental

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Dash](https://img.shields.io/badge/Dash-2.0%2B-orange)
![ESIEE](https://img.shields.io/badge/École-ESIEE%20Paris-red)

## 📋 Description du Projet

Ce projet a été réalisé dans le cadre de l'unité **"Projet Python"** à l'ESIEE Paris. L'objectif est de concevoir un tableau de bord analytique permettant de croiser les données de trafic aérien mondial avec leur impact écologique.

Le dashboard dépasse la simple visualisation de positions : il propose une réflexion sur la saturation de l'espace aérien, l'inégalité de la répartition des flux (Nord vs Sud) et la corrélation directe avec les émissions de CO₂.

---

## 🚀 User Guide (Guide Utilisateur)

### Prérequis
*   Python 3.8 ou supérieur.
*   Une connexion internet 

### Installation

1.  Clonez le dépôt :
    ```bash
    git clone https://github.com/votre-repo/dashboard-aviation.git
    ```

2.  Installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

### Lancement de l'Application

Exécutez la commande suivante à la racine du projet :
```bash
python main.py
```

Ouvrez ensuite votre navigateur à l'adresse indiquée 


## 💾 Données (Data Sources)

Le projet consolide plusieurs sources de données ouvertes pour garantir la précision des analyses :

1.  **OpenSky Network** :
    *   Données de trafic aérien en temps réel (ou snapshots récents).
    *   Utilisé pour la cartographie des positions et l'analyse des altitudes.
    *   *Script de récupération :* `src/utils/get_data.py`.

2.  **Our World in Data (OWID)** :
    *   Dataset : *Annual CO₂ emissions from aviation*.
    *   Utilisé pour l'axe historique et la comparaison des empreintes carbones par pays.

3.  **OpenFlights / OurAirports** :
    *   Base de données statique des aéroports et des routes aériennes.
    *   Permet le calcul de la densité des réseaux aériens (nombre de routes par pays).
    *   *Fichiers bruts :* `data/raw/airports_raw.csv`, `traffic_raw.csv`.

Les données brutes sont traitées et nettoyées via `src/utils/clean_data.py` pour être stockées dans `data/cleaned/`.

---

## 🛠️ Developer Guide

### Architecture du Projet

Le code respecte une structure modulaire pour séparer la logique de traitement de l'interface graphique.

```text
Dashboard_project/
├── main.py                  # Point d'entrée unique (Lance le serveur Dash)
├── config.py                # Variables globales (Chemins, Constantes)
├── requirements.txt         # Liste des librairies Python
├── data/                    # Stockage
│   ├── raw/                 # Données brutes (sourcées)
│   └── cleaned/             # Données nettoyées prêtes pour le Dash
├── src/
│   ├── components/          # Composents graphiques indépendants
│   │   ├── charts.py        # Histogrammes (Altitudes)
│   │   ├── cheeze.py        # Diagramme Camembert (Répartition Continents)
│   │   ├── dyn_pollution.py # Scatter Plot Animé (Pollution vs Routes)
│   │   ├── map_view.py      # Carte Folium/Plotly Mapbox
│   │   └── keys.py          # Indicateurs Clés (KPIs)
│   ├── pages/
│   │   └── home.py          # Assemblage de la page principale (Layout)
│   └── utils/               # Backend logique
│       ├── get_data.py      # Scripts de fetch API
│       └── clean_data.py    # Pipelines de nettoyage Pandas
```



## 📊 Rapport d'Analyse

À travers les différentes visualisations, ce dashboard met en lumière plusieurs tendances clés :

1.  **Inégalités Nord-Sud :**
    *   La carte de densité et le diagramme circulaire montrent une domination du trafic en Europe et Amérique du Nord. Pour  l'Asie c'est un peu différent on voit bien que c'est l'endroit le plus pollué mais les restrictions gouvernementales et militaires en termes d'acces au informations sur les vols faussent les résultats.
    *   L'Afrique et l'Amérique du Sud restent sous-représentées malgré leur superficie, soulignant une fracture infrastructurelle et économique.

2.  **Corrélation Activité/Pollution :**
    *   Le *Bubble Chart* animé (Pollution vs Routes) démontre que les pays ayant le plus de connexions aériennes (USA, Chine) sont logiquement les plus gros émetteurs.
    *   L'animation temporelle révèle l'impact drastique du COVID-19 (2oche 2020-2021) avec un recul des émissions à des niveaux historiques, avant une reprise rapide dès 2022.

3.  **Profils de Vol :**
    *   L'histogramme des altitudes confirme le modèle standard de vol commercial : une concentration massive entre 9km et 12km (altitude de croisière optimale pour la consommation de carburant), distincte des petits porteurs volant à basse altitude.

---

## 👥 Répartition des Tâches

Killian : map.py, keys.py
Theo : charts.py, cheeze.py, dyn_pollution.py
Florian : home.py, clean et get_data, main.py


---

## © Copyright & Licence

Ce projet a été développé à des fins pédagogiques à l'ESIEE Paris.
Usage libre pour consultation. Toute réutilisation commerciale du code source nécessite l'accord des auteurs.

**Auteurs :** [Florian Pereira], [Killian Mauge], [Théo Petreco].
*Année 2025-2026.*
