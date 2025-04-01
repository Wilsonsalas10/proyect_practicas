# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector

def connectionBD():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="app_empresa_bd",
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci",
            raise_on_warnings=True
        )
        if connection.is_connected():
            print("Conexión exitosa a la BD")  # Puedes comentar esto si no quieres que se muestre
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar a la base de datos: {error}") 

    return None  # Asegurar que siempre se devuelve algo

