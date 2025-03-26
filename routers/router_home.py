from main import app
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from mysql.connector.errors import Error

# Importando funciones para conductores
from controllers.funciones_home import *
from controllers.funciones_conductores.f_conductores import *

PATH_URL = "public/conductores"


@app.route('/registrar-conductor', methods=['GET'])
def viewFormconductor():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/form_conductor.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/form-registrar-conductor', methods=['POST'])
def formconductor():
    if 'conectado' in session:
        if 'foto_conductor' in request.files:
            foto_perfil = request.files['foto_conductor']
            resultado = procesar_form_conductor(request.form, foto_perfil)
            if resultado:
                flash('Conductor registrado exitosamente.', 'success')
                return redirect(url_for('lista_conductores'))
            else:
                flash('El conductor NO fue registrado.', 'error')
                return render_template(f'{PATH_URL}/form_conductor.html')
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))



@app.route('/lista-de-conductores', methods=['GET'])
def lista_conductores():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_conductores.html', conductores=sql_lista_conductoresBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-conductor/", methods=['GET'])
@app.route("/detalles-conductor/<int:idconductor>", methods=['GET'])
def detalleconductor(idconductor=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idconductor es None o no está presente en la URL
        if idconductor is None:
            return redirect(url_for('inicio'))
        else:
            detalle_conductor = sql_detalles_conductoresBD(idconductor) or []
            return render_template(f'{PATH_URL}/detalles_conductor.html', detalle_conductor=detalle_conductor)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscador de conductores
@app.route("/buscando-conductor", methods=['POST'])
def viewBuscarconductorBD():
    resultadoBusqueda = buscarconductorBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_conductor.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})


@app.route("/editar-conductor/<int:id>", methods=['GET'])
def viewEditarConductor(id):
    if 'conectado' in session:
        respuestaconductor = buscarconductorUnico(id)
        if respuestaconductor:
            return render_template(f'{PATH_URL}/form_conductor_update.html', respuestaconductor=respuestaconductor)
        else:
            flash('El conductor no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Recibir formulario para actualizar información de conductor
@app.route('/actualizar-conductor', methods=['POST'])
def actualizarconductor():
    resultData = procesar_actualizacion_form(request)
    if resultData:
        return redirect(url_for('lista_conductores'))


@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/borrar-conductor/<string:id_conductor>/<string:foto_conductor>', methods=['GET'])
def borrarconductor(id_conductor, foto_conductor):
    resp = eliminarconductor(id_conductor, foto_conductor)
    if resp:
        flash('El conductor fue eliminado correctamente', 'success')
        return redirect(url_for('lista_conductores'))


@app.route("/descargar-informe-conductores/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
