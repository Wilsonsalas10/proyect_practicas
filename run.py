from main import app  # Importamos la aplicación desde 'main.py'

# Importando todos mis Routers (Rutas)
from routers.router_login import *
from routers.router_home import *
from routers.router_page_not_found import *

# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600)  # Inicia el servidor Flask en el puerto 5600

