from flask import Flask
from routers.rutas_vehiculos.router_vehiculos import vehiculos_bp  # Importa el Blueprint

# Crear la aplicación Flask
app = Flask(__name__)

# Registrar el Blueprint de vehículos
app.register_blueprint(vehiculos_bp, url_prefix='/vehiculos')

# Configurando la clave secreta para sesiones y otras configuraciones
app.secret_key = '97110c78ae51a45af397b6534caef90ebb9b1dcb3380f008f90b23a5d1616bf1bc29098105da20fe'

if __name__ == '__main__':
    app.run(debug=True, port=5600)
