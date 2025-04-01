from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'tu_secreto'  # Necesario para flash messages

# Crear la carpeta de uploads si no existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_db_connection():
    try:
        return pymysql.connect(
            host='localhost',
            user='root',  # Ajusta tu usuario
            password='1234',  # Ajusta tu contraseña
            database='app_empresa_bd',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        flash(f'Error de conexión a la base de datos: {str(e)}', 'danger')
        return None

@app.route('/form-registrar-conductor', methods=['POST'])
def registrar_conductor():
    connection = None  # Inicializar la conexión

    try:
        nombre_conductor = request.form.get('nombres', '').strip()
        apellido_conductor = request.form.get('apellidos', '').strip()
        numero_identificacion = request.form.get('numero_identificacion', '').strip()
        
        if not numero_identificacion.isdigit():
            flash('El número de identificación debe ser un número válido.', 'danger')
            return redirect(url_for('mostrar_lista_conductores'))
        
        numero_identificacion = int(numero_identificacion)
        cargo = request.form.get('cargo', '').strip()
        fecha_vencimiento_licencia = request.form.get('fecha_vencimiento_licencia', '')
        comparendos = request.form.get('comparendos', 'No')  # Si no está marcado, será 'No'
        acuerdo_pago = request.form.get('acuerdo_pago', 'No')
        fecha_vencimiento_curso = request.form.get('fecha_vencimiento_curso', '')

        # Calcular los días restantes
        fecha_actual = datetime.now().date()
        dias_restantes_licencia = (datetime.strptime(fecha_vencimiento_licencia, '%Y-%m-%d').date() - fecha_actual).days if fecha_vencimiento_licencia else None
        dias_restantes_curso = (datetime.strptime(fecha_vencimiento_curso, '%Y-%m-%d').date() - fecha_actual).days if fecha_vencimiento_curso else None

        # Manejar la subida de la imagen
        foto_conductor = request.files.get('foto_conductor')
        filename = 'default.png'  # Imagen por defecto

        if foto_conductor and foto_conductor.filename != '':
            filename = f"{numero_identificacion}_{foto_conductor.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            foto_conductor.save(filepath)

        connection = get_db_connection()
        if connection is None:
            return redirect(url_for('mostrar_lista_conductores'))

        with connection.cursor() as cursor:
            sql = """
            INSERT INTO tbl_conductores (
                nombre_conductor, apellido_conductor, numero_identificacion,
                cargo, fecha_vencimiento_licencia, dias_restantes_licencia,
                comparendos, acuerdo_pago, fecha_vencimiento_curso, dias_restantes_curso, foto_conductor
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                nombre_conductor, apellido_conductor, numero_identificacion,
                cargo, fecha_vencimiento_licencia, dias_restantes_licencia,
                comparendos, acuerdo_pago, fecha_vencimiento_curso, dias_restantes_curso, filename
            ))
            connection.commit()
        flash('Conductor registrado con éxito', 'success')

    except Exception as e:
        flash(f'Error al registrar conductor: {str(e)}', 'danger')
    
    finally:
        if connection:
            connection.close()
    
    return redirect(url_for('mostrar_lista_conductores'))

@app.route('/lista-conductores')
def mostrar_lista_conductores():
    connection = None  # Inicializar la conexión
    conductores = []

    try:
        connection = get_db_connection()
        if connection is None:
            return render_template('lista_conductores.html', conductores=conductores)

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tbl_conductores")
            conductores = cursor.fetchall()

    except Exception as e:
        flash(f'Error al obtener la lista de conductores: {str(e)}', 'danger')
    
    finally:
        if connection:
            connection.close()
    
    return render_template('lista_conductores.html', conductores=conductores)

if __name__ == '__main__':
    app.run(debug=True)
