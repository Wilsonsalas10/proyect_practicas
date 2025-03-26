import datetime
import os
import re
import uuid  # Asegúrate de importar uuid
import openpyxl
from flask import send_file
from conexion.conexionBD import connectionBD

# Registrar vehículo
def procesar_form_vehiculo(dataForm, imagen_vehiculo):
    try:
        # Procesar la imagen del vehículo
        result_imagen = procesar_imagen(imagen_vehiculo)  # Función para procesar la imagen
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO tbl_vehiculos (cd_vehiculo, placa_vehiculo, soat_vencimiento, rtm_vencimiento, 
                    permiso_vencimiento, imagen_vehiculo) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                valores = (
                    dataForm['cd_vehiculo'], dataForm['placa_vehiculo'], dataForm['soat_vencimiento'],
                    dataForm['rtm_vencimiento'], dataForm['permiso_vencimiento'], result_imagen
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount
    except Exception as e:
        print(f"Error en procesar_form_vehiculo: {str(e)}")
        return None

# Obtener lista de vehículos
def sql_lista_vehiculosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id_vehiculo, cd_vehiculo, placa_vehiculo, soat_vencimiento, rtm_vencimiento, 
                    permiso_vencimiento, imagen_vehiculo 
                    FROM tbl_vehiculos ORDER BY id_vehiculo DESC
                """
                cursor.execute(querySQL)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en sql_lista_vehiculosBD: {e}")
        return None

# Obtener detalles de un vehículo
def sql_detalles_vehiculoBD(id_vehiculo):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT * FROM tbl_vehiculos WHERE id_vehiculo = %s
                """
                cursor.execute(querySQL, (id_vehiculo,))
                return cursor.fetchone()
    except Exception as e:
        print(f"Error en sql_detalles_vehiculoBD: {e}")
        return None

# Eliminar vehículo
def eliminar_vehiculo(id_vehiculo, imagen_vehiculo):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM tbl_vehiculos WHERE id_vehiculo=%s"
                cursor.execute(querySQL, (id_vehiculo,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
                
                if resultado_eliminar:
                    url_File = os.path.join("../static/fotos_vehiculos", imagen_vehiculo)
                    if os.path.exists(url_File):
                        os.remove(url_File)
                
        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminar_vehiculo: {e}")
        return None

# Generar reporte de vehículos en Excel
def generarReporteExcelVehiculos():
    try:
        dataVehiculos = sql_lista_vehiculosBD()
        wb = openpyxl.Workbook()
        hoja = wb.active
        hoja.append(["CD", "Placa", "SOAT Vencimiento", "RTM Vencimiento", "Permiso Vencimiento"])
        
        for registro in dataVehiculos:
            hoja.append([
                registro['cd_vehiculo'], registro['placa_vehiculo'], registro['soat_vencimiento'],
                registro['rtm_vencimiento'], registro['permiso_vencimiento']
            ])
        
        fecha_actual = datetime.datetime.now().strftime('%Y_%m_%d')
        archivoExcel = f"Reporte_vehiculos_{fecha_actual}.xlsx"
        ruta_archivo = os.path.join("../static/downloads-excel", archivoExcel)
        
        if not os.path.exists(os.path.dirname(ruta_archivo)):
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        
        wb.save(ruta_archivo)
        return send_file(ruta_archivo, as_attachment=True)
    except Exception as e:
        print(f"Error en generarReporteExcelVehiculos: {e}")
        return None

# Función para procesar la imagen del vehículo
def procesar_imagen(imagen_vehiculo):
    if imagen_vehiculo and allowed_file(imagen_vehiculo.filename):
        filename = str(uuid.uuid4()) + '.' + imagen_vehiculo.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join("../static/fotos_vehiculos", filename)
        imagen_vehiculo.save(filepath)
        return filename
    return None

# Verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
