from flask import Blueprint, request, jsonify, send_file
from controllers.funciones_vehiculos.funciones_vehiculos import (
    procesar_form_vehiculo, sql_lista_vehiculosBD, sql_detalles_vehiculoBD, 
    eliminar_vehiculo, generarReporteExcelVehiculos
)

vehiculos_bp = Blueprint('vehiculos', __name__)

# Dentro de router_vehiculos.py
from flask import Blueprint, render_template

vehiculos_bp = Blueprint('vehiculos', __name__)

# En router_vehiculos.py
@vehiculos_bp.route('/registrar-vehiculo', methods=['GET'])
def viewFormconductor():
    return render_template('public/conductores/form_conductor.html')

# Ruta para registrar un nuevo vehículo
@vehiculos_bp.route('/registrar-vehiculo', methods=['POST'])
def registrar_vehiculo():
    try:
        data = request.form
        imagen_vehiculo = request.files.get('imagen_vehiculo')
        
        # Procesamos el formulario del vehículo
        resultado = procesar_form_vehiculo(data, imagen_vehiculo)
        
        if resultado:
            return jsonify({'message': 'Vehículo registrado correctamente'}), 201
        else:
            return jsonify({'error': 'No se pudo registrar el vehículo'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener lista de vehículos
@vehiculos_bp.route('/lista-vehiculos', methods=['GET'])
def lista_vehiculos():
    try:
        data = sql_lista_vehiculosBD()
        if data:
            return jsonify(data), 200
        else:
            return jsonify({'message': 'No hay vehículos registrados'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener detalles de un vehículo específico
@vehiculos_bp.route('/detalles-vehiculo/<int:id_vehiculo>', methods=['GET'])
def detalles_vehiculo(id_vehiculo):
    try:
        data = sql_detalles_vehiculoBD(id_vehiculo)
        if data:
            return jsonify(data), 200
        else:
            return jsonify({'message': 'Vehículo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un vehículo
@vehiculos_bp.route('/eliminar-vehiculo/<int:id_vehiculo>', methods=['DELETE'])
def eliminar_vehiculo_route(id_vehiculo):
    try:
        # Obtener imagen de vehículo si es necesario
        data = request.json
        imagen_vehiculo = data.get('imagen_vehiculo')
        
        resultado = eliminar_vehiculo(id_vehiculo, imagen_vehiculo)
        
        if resultado:
            return jsonify({'message': 'Vehículo eliminado correctamente'}), 200
        else:
            return jsonify({'error': 'No se pudo eliminar el vehículo'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para generar un reporte en Excel de los vehículos
@vehiculos_bp.route('/reporte-vehiculos', methods=['GET'])
def reporte_vehiculos():
    try:
        return generarReporteExcelVehiculos()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
