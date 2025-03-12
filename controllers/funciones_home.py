
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file


def procesar_form_conductor(dataForm, foto_perfil):
    # Formateando Salario
    salario_sin_puntos = re.sub('[^0-9]+', '', dataForm['salario_conductor'])
    # convertir salario a INT
    salario_entero = int(salario_sin_puntos)

    result_foto_perfil = procesar_imagen_perfil(foto_perfil)
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:

                sql = "INSERT INTO tbl_conductores (nombre_conductor, apellido_conductor, sexo_conductor, telefono_conductor, email_conductor, profesion_conductor, foto_conductor, salario_conductor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

                # Creando una tupla con los valores del INSERT
                valores = (dataForm['nombre_conductor'], dataForm['apellido_conductor'], dataForm['sexo_conductor'],
                           dataForm['telefono_conductor'], dataForm['email_conductor'], dataForm['profesion_conductor'], result_foto_perfil, salario_entero)
                cursor.execute(sql, valores)

                conexion_MySQLdb.commit()
                resultado_insert = cursor.rowcount
                return resultado_insert

    except Exception as e:
        return f'Se produjo un error en procesar_form_conductor: {str(e)}'


def procesar_imagen_perfil(foto):
    try:
        # Nombre original del archivo
        filename = secure_filename(foto.filename)
        extension = os.path.splitext(filename)[1]

        # Creando un string de 50 caracteres
        nuevoNameFile = (uuid.uuid4().hex + uuid.uuid4().hex)[:100]
        nombreFile = nuevoNameFile + extension

        # Construir la ruta completa de subida del archivo
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_dir = os.path.join(basepath, f'../static/fotos_conductores/')

        # Validar si existe la ruta y crearla si no existe
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            # Dando permiso a la carpeta
            os.chmod(upload_dir, 0o755)

        # Construir la ruta completa de subida del archivo
        upload_path = os.path.join(upload_dir, nombreFile)
        foto.save(upload_path)

        return nombreFile

    except Exception as e:
        print("Error al procesar archivo:", e)
        return []


# Lista de conductores
def sql_lista_conductoresBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = (f"""
                    SELECT 
                        e.id_conductor,
                        e.nombre_conductor, 
                        e.apellido_conductor,
                        e.salario_conductor,
                        e.foto_conductor,
                        CASE
                            WHEN e.sexo_conductor = 1 THEN 'Masculino'
                            ELSE 'Femenino'
                        END AS sexo_conductor
                    FROM tbl_conductores AS e
                    ORDER BY e.id_conductor DESC
                    """)
                cursor.execute(querySQL,)
                conductoresBD = cursor.fetchall()
        return conductoresBD
    except Exception as e:
        print(
            f"Errro en la función sql_lista_conductoresBD: {e}")
        return None


# Detalles del conductor
def sql_detalles_conductoresBD(idconductor):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        e.id_conductor,
                        e.nombre_conductor, 
                        e.apellido_conductor,
                        e.salario_conductor,
                        CASE
                            WHEN e.sexo_conductor = 1 THEN 'Masculino'
                            ELSE 'Femenino'
                        END AS sexo_conductor,
                        e.telefono_conductor, 
                        e.email_conductor,
                        e.profesion_conductor,
                        e.foto_conductor,
                        DATE_FORMAT(e.fecha_registro, '%Y-%m-%d %h:%i %p') AS fecha_registro
                    FROM tbl_conductores AS e
                    WHERE id_conductor =%s
                    ORDER BY e.id_conductor DESC
                    """)
                cursor.execute(querySQL, (idconductor,))
                conductoresBD = cursor.fetchone()
        return conductoresBD
    except Exception as e:
        print(
            f"Errro en la función sql_detalles_conductoresBD: {e}")
        return None


# Funcion conductores Informe (Reporte)
def conductoresReporte():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = ("""
                    SELECT 
                        e.id_conductor,
                        e.nombre_conductor, 
                        e.apellido_conductor,
                        e.salario_conductor,
                        e.email_conductor,
                        e.telefono_conductor,
                        e.profesion_conductor,
                        DATE_FORMAT(e.fecha_registro, '%d de %b %Y %h:%i %p') AS fecha_registro,
                        CASE
                            WHEN e.sexo_conductor = 1 THEN 'Masculino'
                            ELSE 'Femenino'
                        END AS sexo_conductor
                    FROM tbl_conductores AS e
                    ORDER BY e.id_conductor DESC
                    """)
                cursor.execute(querySQL,)
                conductoresBD = cursor.fetchall()
        return conductoresBD
    except Exception as e:
        print(
            f"Errro en la función conductoresReporte: {e}")
        return None


def generarReporteExcel():
    dataconductores = conductoresReporte()
    wb = openpyxl.Workbook()
    hoja = wb.active

    # Agregar la fila de encabezado con los títulos
    cabeceraExcel = ("Nombre", "Apellido", "Sexo",
                     "Telefono", "Email", "Profesión", "Salario", "Fecha de Ingreso")

    hoja.append(cabeceraExcel)

    # Formato para números en moneda colombiana y sin decimales
    formato_moneda_colombiana = '#,##0'

    # Agregar los registros a la hoja
    for registro in dataconductores:
        nombre_conductor = registro['nombre_conductor']
        apellido_conductor = registro['apellido_conductor']
        sexo_conductor = registro['sexo_conductor']
        telefono_conductor = registro['telefono_conductor']
        email_conductor = registro['email_conductor']
        profesion_conductor = registro['profesion_conductor']
        salario_conductor = registro['salario_conductor']
        fecha_registro = registro['fecha_registro']

        # Agregar los valores a la hoja
        hoja.append((nombre_conductor, apellido_conductor, sexo_conductor, telefono_conductor, email_conductor, profesion_conductor,
                     salario_conductor, fecha_registro))

        # Itera a través de las filas y aplica el formato a la columna G
        for fila_num in range(2, hoja.max_row + 1):
            columna = 7  # Columna G
            celda = hoja.cell(row=fila_num, column=columna)
            celda.number_format = formato_moneda_colombiana

    fecha_actual = datetime.datetime.now()
    archivoExcel = f"Reporte_conductores_{fecha_actual.strftime('%Y_%m_%d')}.xlsx"
    carpeta_descarga = "../static/downloads-excel"
    ruta_descarga = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), carpeta_descarga)

    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)
        # Dando permisos a la carpeta
        os.chmod(ruta_descarga, 0o755)

    ruta_archivo = os.path.join(ruta_descarga, archivoExcel)
    wb.save(ruta_archivo)

    # Enviar el archivo como respuesta HTTP
    return send_file(ruta_archivo, as_attachment=True)


def buscarconductorBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            e.id_conductor,
                            e.nombre_conductor, 
                            e.apellido_conductor,
                            e.salario_conductor,
                            CASE
                                WHEN e.sexo_conductor = 1 THEN 'Masculino'
                                ELSE 'Femenino'
                            END AS sexo_conductor
                        FROM tbl_conductores AS e
                        WHERE e.nombre_conductor LIKE %s 
                        ORDER BY e.id_conductor DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarconductorBD: {e}")
        return []


def buscarconductorUnico(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            e.id_conductor,
                            e.nombre_conductor, 
                            e.apellido_conductor,
                            e.sexo_conductor,
                            e.telefono_conductor,
                            e.email_conductor,
                            e.profesion_conductor,
                            e.salario_conductor,
                            e.foto_conductor
                        FROM tbl_conductores AS e
                        WHERE e.id_conductor =%s LIMIT 1
                    """)
                mycursor.execute(querySQL, (id,))
                conductor = mycursor.fetchone()
                return conductor

    except Exception as e:
        print(f"Ocurrió un error en def buscarconductorUnico: {e}")
        return []


def procesar_actualizacion_form(data):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                nombre_conductor = data.form['nombre_conductor']
                apellido_conductor = data.form['apellido_conductor']
                sexo_conductor = data.form['sexo_conductor']
                telefono_conductor = data.form['telefono_conductor']
                email_conductor = data.form['email_conductor']
                profesion_conductor = data.form['profesion_conductor']

                salario_sin_puntos = re.sub(
                    '[^0-9]+', '', data.form['salario_conductor'])
                salario_conductor = int(salario_sin_puntos)
                id_conductor = data.form['id_conductor']

                if data.files['foto_conductor']:
                    file = data.files['foto_conductor']
                    fotoForm = procesar_imagen_perfil(file)

                    querySQL = """
                        UPDATE tbl_conductores
                        SET 
                            nombre_conductor = %s,
                            apellido_conductor = %s,
                            sexo_conductor = %s,
                            telefono_conductor = %s,
                            email_conductor = %s,
                            profesion_conductor = %s,
                            salario_conductor = %s,
                            foto_conductor = %s
                        WHERE id_conductor = %s
                    """
                    values = (nombre_conductor, apellido_conductor, sexo_conductor,
                              telefono_conductor, email_conductor, profesion_conductor,
                              salario_conductor, fotoForm, id_conductor)
                else:
                    querySQL = """
                        UPDATE tbl_conductores
                        SET 
                            nombre_conductor = %s,
                            apellido_conductor = %s,
                            sexo_conductor = %s,
                            telefono_conductor = %s,
                            email_conductor = %s,
                            profesion_conductor = %s,
                            salario_conductor = %s
                        WHERE id_conductor = %s
                    """
                    values = (nombre_conductor, apellido_conductor, sexo_conductor,
                              telefono_conductor, email_conductor, profesion_conductor,
                              salario_conductor, id_conductor)

                cursor.execute(querySQL, values)
                conexion_MySQLdb.commit()

        return cursor.rowcount or []
    except Exception as e:
        print(f"Ocurrió un error en procesar_actualizacion_form: {e}")
        return None


# Lista de Usuarios creados
def lista_usuariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id, name_surname, email_user, created_user FROM users"
                cursor.execute(querySQL,)
                usuariosBD = cursor.fetchall()
        return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []


# Eliminar conductor
def eliminarconductor(id_conductor, foto_conductor):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM tbl_conductores WHERE id_conductor=%s"
                cursor.execute(querySQL, (id_conductor,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

                if resultado_eliminar:
                    # Eliminadon foto_conductor desde el directorio
                    basepath = path.dirname(__file__)
                    url_File = path.join(
                        basepath, '../static/fotos_conductores', foto_conductor)

                    if path.exists(url_File):
                        remove(url_File)  # Borrar foto desde la carpeta

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarconductor : {e}")
        return []


# Eliminar usuario
def eliminarUsuario(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM users WHERE id=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount

        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []
