from dash import Dash
from src.pages.home import layout

app = Dash(__name__)

# Note : Si layout est une fonction (comme ci-dessus), on l'appelle avec ()
# Si c'est une variable, on met juste layout
app.layout = layout() 

if __name__ == '__main__':
    app.run(debug=True)