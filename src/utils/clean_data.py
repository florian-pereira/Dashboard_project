"""
Module de nettoyage et transformation des données.

Traite les données brutes pour les rendre exploitables par le dashboard :
- Filtrage des valeurs manquantes ou incohérentes
- Conversion des unités (vitesse m/s vers km/h)
- Fusion des tables aéroports et routes
- Calcul des métriques dérivées (nombre de routes par aéroport)

Les données nettoyées sont exportées dans data/cleaned/
"""

import pandas as pd
import os
import sys

# Petit hack pour importer config.py qui est dans le dossier parent
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from config import (
    TRAFFIC_RAW_FILE,
    AIRPORTS_RAW_FILE,
    ROUTES_RAW_FILE,
    TRAFFIC_CLEANED_FILE,
    AIRPORTS_CLEANED_FILE,
)


def process_live_traffic():
    """
    Nettoie les données de trafic  (Avions)
    """

    if not os.path.exists(TRAFFIC_RAW_FILE):
        print(" Fichier introuvable. Lancer d'abord get_data.py.")
        return

    try:
        df = pd.read_csv(TRAFFIC_RAW_FILE)

        # On filtre pour garder seulement les avions qui volent

        df = df[(df["on_ground"] == False) & (df["baro_altitude"].notna())].copy()

        df = df.dropna(subset=["latitude", "longitude"])
        # Conversion vitesse m/s -> km/h
        if "velocity" in df.columns:
            df["velocity_kmh"] = df["velocity"] * 3.6
        else:
            df["velocity_kmh"] = 0

        # On garde juste les colonnes qui nous intéressent :

        cols_to_keep = [
            "icao24",
            "callsign",
            "origin_country",
            "longitude",
            "latitude",
            "baro_altitude",
            "true_track",
            "velocity_kmh",
            "origin_country",
        ]
        cols_final = [c for c in cols_to_keep if c in df.columns]
        df = df[cols_final]

        df.to_csv(TRAFFIC_CLEANED_FILE, index=False)
        print(f" Il y a {len(df)} avions en vol, après nettoyage.")

    except Exception as e:
        print(f"  Erreur nettoyage trafic : {e}")


def process_static_data():
    """
    Fusionne Aéroports et Routes pour calculer la taille des hubs.
    """

    if not os.path.exists(AIRPORTS_RAW_FILE) or not os.path.exists(ROUTES_RAW_FILE):
        print(" Fichiers RAW introuvables (Airports ou Routes manquants).")
        return

    try:
        df_air = pd.read_csv(AIRPORTS_RAW_FILE)
        df_routes = pd.read_csv(ROUTES_RAW_FILE)

        # on supprime les lignes où il manque des infos importantes (Lat/Lon/IATA)
        df_air = df_air.dropna(subset=["Latitude", "Longitude", "IATA"])

        # On compte combien de routes partent de chaque aéroport
        route_counts = (
            df_routes["Source Airport"].value_counts().reset_index()
        )  # reset_index pour un dataframe propre
        route_counts.columns = ["IATA", "Route_Count"]
        route_counts["Route_Count"] = route_counts["Route_Count"]

        # On fusionne les aéroports avec le nombre de routes
        df_merged = pd.merge(df_air, route_counts, on="IATA", how="left")
        df_merged["Route_Count"] = df_merged["Route_Count"].fillna(
            0
        )  # Si pas de route, je mets 0

        # On filtre les petits aéroports (au moins 5 routes)
        df_final = df_merged.query("Route_Count >= 5 ").copy()

        # Sauvegarde
        df_final.to_csv(AIRPORTS_CLEANED_FILE, index=False)
        print(f" Aéroports après nettoyage : {len(df_final)} lignes.")

    except Exception as e:
        print(f" Erreur traitement aéroports : {e}")


def load_data(dataset="traffic"):
    """
    Charge les données PROPRES pour le dashboard
    et convertit les colonnes en Entiers de manière robuste.
    """
    if dataset == "traffic":
        path = TRAFFIC_CLEANED_FILE
        # Liste des colonnes qu'on veut convertir en entier
        int_cols = ["baro_altitude", "velocity_kmh"]

    elif dataset == "airports":
        path = AIRPORTS_CLEANED_FILE
        int_cols = ["Route_Count"]

    else:
        return None

    if os.path.exists(path):
        # 1. Lecture simple du CSV
        df = pd.read_csv(path)

        # 2. Conversion en nombres entiers
        for col in int_cols:
            if col in df.columns:
                # Si bug dans la conversion, ça met NaN
                # round() gère les cas où on aurait 850.9 pour en faire 851
                df[col] = (
                    pd.to_numeric(df[col], errors="coerce").round().astype("Int64")
                )

        return df
    else:
        print(f" Fichier {path} introuvable. ")
        return pd.DataFrame()
