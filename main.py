from dash import Dash
from src.pages.home import layout
from src.utils.get_data import get_live_traffic_data
from src.utils.clean_data import process_live_traffic, load_data

# ÉTAPE 1 : Récupération (Génère traffic_raw.csv)
get_live_traffic_data()
# ÉTAPE 2 : Nettoyage (Lit traffic_raw.csv et génère traffic_cleaned.csv)
process_live_traffic()
        
# ÉTAPE 3 : Chargement (Lit traffic_cleaned.csv pour Dash)
df = load_data(dataset="traffic")

app = Dash(__name__)

# Note : Si layout est une fonction (comme ci-dessus), on l'appelle avec ()
# Si c'est une variable, on met juste layout
app.layout = layout() 

if __name__ == '__main__':
    app.run(debug=True)