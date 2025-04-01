# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Para crear identificadores únicos
import datetime
import re
import os

from os import remove, path  # Para manejar archivos
import openpyxl  # Para generar archivos Excel
from flask import send_file  # Para forzar descargas

# Conexión a BD
from conexion.conexionBD import connectionBD


# Obtener lista de usuarios desde la base de datos
def lista_usuariosBD():
    try:
        conexion_MySQLdb = connectionBD()
        if conexion_MySQLdb is None:
            return []  # Si la conexión falla, retornar lista vacía

        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = "SELECT id, name_surname, email_user, created_user FROM users"
            cursor.execute(querySQL)
            usuariosBD = cursor.fetchall() or []  # Evitar None si no hay resultados

        conexion_MySQLdb.close()  # Cerrar conexión después de uso
        return usuariosBD

    except Exception as e:
        print(f"Error en lista_usuariosBD: {e}")
        return []


# Eliminar usuario de la base de datos
def eliminarUsuario(id):
    try:
        conexion_MySQLdb = connectionBD()
        if conexion_MySQLdb is None:
            return 0  # Retorna 0 si no hay conexión

        with conexion_MySQLdb.cursor(dictionary=True) as cursor:
            querySQL = "DELETE FROM users WHERE id=%s"
            cursor.execute(querySQL, (id,))
            conexion_MySQLdb.commit()
            resultado_eliminar = cursor.rowcount  # Número de filas afectadas

        conexion_MySQLdb.close()
        return resultado_eliminar  # Retorna 1 si se eliminó correctamente, 0 si no

    except Exception as e:
        print(f"Error en eliminarUsuario: {e}")
        return 0  # Retorna 0 en caso de error
