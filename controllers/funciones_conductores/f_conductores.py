import datetime
import os
import re
import openpyxl
from flask import send_file
from conexion.conexionBD import connectionBD
from werkzeug.utils import secure_filename
import os
import uuid

# Carpeta donde se almacenarán las fotos de los conductores
UPLOAD_FOLDER = "../static/fotos_conductores/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función para procesar y guardar la imagen del conductor
def procesar_imagen(foto_conductor):
    if foto_conductor and allowed_file(foto_conductor.filename):
        # Generar un nombre único para la imagen
        filename = str(uuid.uuid4()) + '.' + foto_conductor.filename.rsplit('.', 1)[1].lower()
        
        # Verifica si la carpeta existe, si no, la crea
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        # Guardar la imagen en la carpeta especificada
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Usar secure_filename para asegurar que el nombre del archivo es seguro
        foto_conductor.save(filepath)
        
        # Retornar la ruta de la imagen guardada
        return filename
    else:
        # Si no se recibe una imagen válida, retornar None o algún valor por defecto
        return None


# Función para procesar el formulario de conductor y registrar en la base de datos
def procesar_form_conductor(dataForm, foto_conductor):
    try:
        # Validación y procesamiento del salario (limpiar caracteres no numéricos)
        salario_sin_puntos = re.sub('[^0-9]+', '', dataForm['salario_conductor'])
        salario_entero = int(salario_sin_puntos)
        
        # Procesar la imagen del conductor
        result_foto_conductor = procesar_imagen(foto_conductor)

        # Inserción de datos en la base de datos
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    INSERT INTO tbl_conductores 
                    (nombre_conductor, apellido_conductor, sexo_conductor, telefono_conductor, 
                    email_conductor, profesion_conductor, foto_conductor, salario_conductor) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                valores = (
                    dataForm['nombre_conductor'], dataForm['apellido_conductor'], int(dataForm['sexo_conductor']),
                    dataForm['telefono_conductor'], dataForm['email_conductor'], dataForm['profesion_conductor'], 
                    result_foto_conductor, salario_entero
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount  # Verifica si se insertó correctamente el registro
    except Exception as e:
        print(f"Error en procesar_form_conductor: {str(e)}")
        return None



# Función para obtener la lista de conductores de la base de datos
def sql_lista_conductoresBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id_conductor, nombre_conductor, apellido_conductor, salario_conductor, foto_conductor,
                    CASE WHEN sexo_conductor = 1 THEN 'Masculino' ELSE 'Femenino' END AS sexo_conductor
                    FROM tbl_conductores ORDER BY id_conductor DESC
                """
                cursor.execute(querySQL)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en sql_lista_conductoresBD: {e}")
        return None

# Función para obtener los detalles de un conductor específico
def sql_detalles_conductoresBD(idconductor):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id_conductor, nombre_conductor, apellido_conductor, salario_conductor,
                    CASE WHEN sexo_conductor = 1 THEN 'Masculino' ELSE 'Femenino' END AS sexo_conductor,
                    telefono_conductor, email_conductor, profesion_conductor, foto_conductor,
                    DATE_FORMAT(fecha_registro, '%Y-%m-%d %h:%i %p') AS fecha_registro
                    FROM tbl_conductores WHERE id_conductor = %s ORDER BY id_conductor DESC
                """
                cursor.execute(querySQL, (idconductor,))
                return cursor.fetchone()
    except Exception as e:
        print(f"Error en sql_detalles_conductoresBD: {e}")
        return None

# Función para generar el reporte de conductores en formato Excel
def generarReporteExcel():
    try:
        dataconductores = sql_lista_conductoresBD()
        wb = openpyxl.Workbook()
        hoja = wb.active
        hoja.append(["Nombre", "Apellido", "Sexo", "Telefono", "Email", "Profesión", "Salario", "Fecha de Ingreso"])
        
        for registro in dataconductores:
            hoja.append([
                registro['nombre_conductor'], registro['apellido_conductor'], registro['sexo_conductor'],
                registro['telefono_conductor'], registro['email_conductor'], registro['profesion_conductor'],
                registro['salario_conductor'], registro['fecha_registro']
            ])
        
        fecha_actual = datetime.datetime.now().strftime('%Y_%m_%d')
        archivoExcel = f"Reporte_conductores_{fecha_actual}.xlsx"
        ruta_archivo = os.path.join("../static/downloads-excel", archivoExcel)
        
        if not os.path.exists(os.path.dirname(ruta_archivo)):
            os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        
        wb.save(ruta_archivo)
        return send_file(ruta_archivo, as_attachment=True)
    except Exception as e:
        print(f"Error en generarReporteExcel: {e}")
        return None

# Función para buscar conductores por nombre
def buscarconductorBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id_conductor, nombre_conductor, apellido_conductor, salario_conductor,
                    CASE WHEN sexo_conductor = 1 THEN 'Masculino' ELSE 'Femenino' END AS sexo_conductor
                    FROM tbl_conductores WHERE nombre_conductor LIKE %s ORDER BY id_conductor DESC
                """
                cursor.execute(querySQL, (f"%{search}%",))
                return cursor.fetchall()
    except Exception as e:
        print(f"Error en buscarconductorBD: {e}")
        return []

# Función para eliminar un conductor de la base de datos
def eliminarconductor(id_conductor, foto_conductor):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM tbl_conductores WHERE id_conductor=%s"
                cursor.execute(querySQL, (id_conductor,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
                
                if resultado_eliminar:
                    url_File = os.path.join("../static/fotos_conductores", foto_conductor)
                    if os.path.exists(url_File):
                        os.remove(url_File)
                
        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarconductor: {e}")
        return None
    
# buscarconductorUnico

def buscarconductorUnico(id_conductor):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                    SELECT id_conductor, nombre_conductor, apellido_conductor, telefono_conductor, 
                           email_conductor, profesion_conductor, salario_conductor, foto_conductor
                    FROM tbl_conductores
                    WHERE id_conductor = %s
                """
                cursor.execute(querySQL, (id_conductor,))
                return cursor.fetchone()  # Retorna el primer resultado (único) encontrado
    except Exception as e:
        print(f"Error en buscarconductorUnico: {e}")
        return None

# f_conductores.py

def procesar_actualizacion_form(request):
    try:
        # Supongo que los datos vienen de un formulario que es un diccionario
        dataForm = request.form
        id_conductor = dataForm['id_conductor']
        salario_sin_puntos = re.sub('[^0-9]+', '', dataForm['salario_conductor'])
        salario_entero = int(salario_sin_puntos)
        
        # Aquí procesamos la imagen del conductor si es que se sube una nueva
        foto_conductor = request.files.get('foto_conductor')
        if foto_conductor:
            result_foto_conductor = procesar_imagen(foto_conductor)  # Esta es la función que ya tienes definida
        else:
            result_foto_conductor = dataForm['foto_conductor_anterior']  # Usamos la foto anterior si no hay nueva imagen
        
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                sql = """
                    UPDATE tbl_conductores
                    SET nombre_conductor = %s, apellido_conductor = %s, telefono_conductor = %s, 
                        email_conductor = %s, profesion_conductor = %s, salario_conductor = %s, 
                        foto_conductor = %s
                    WHERE id_conductor = %s
                """
                valores = (
                    dataForm['nombre_conductor'], dataForm['apellido_conductor'], dataForm['telefono_conductor'],
                    dataForm['email_conductor'], dataForm['profesion_conductor'], salario_entero,
                    result_foto_conductor, id_conductor
                )
                cursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                return cursor.rowcount  # Retorna el número de filas afectadas (si es > 0, la actualización fue exitosa)
    except Exception as e:
        print(f"Error en procesar_actualizacion_form: {e}")
        return None
