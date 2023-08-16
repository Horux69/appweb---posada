from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os
import hashlib
from admin import Administrador
from validaLoginAdmin import ValidationLoginAdmin


app = Flask(__name__)
app.secret_key = "digitalforge"

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='10.206.66.185'
app.config['MYSQL_DATABASE_USER']='backend_2'
app.config['MYSQL_DATABASE_PASSWORD']='@Andres4321'
app.config['MYSQL_DATABASE_DB']='visitabuga'
mysql.init_app(app)

conexion = mysql.connect()
cursor = conexion.cursor()

losOperadores = Administrador(mysql)
validaLoginAdmin = ValidationLoginAdmin(mysql)


@app.route('/')
def admin_index():
    return render_template('admin/login.html')

@app.route('/admin/login')
def adminLogin():
    return render_template('admin/login.html')

@app.route('/admin/verAdmin')
def verAdmin():

    resultados = losOperadores.consultarAdmin()

    return render_template("admin/verAdmin.html", admins = resultados)

@app.route('/admin/agregar', methods = ['POST'])
def agregarAdmin():
    nombre = request.form['txtNombre']
    apellido = request.form['txtApellido']
    cedula = request.form['txtCedula']
    correo = request.form['txtCorreo']
    celular = request.form['txtCelular']
    contrasena = request.form['txtPassword']

    cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

    rol = 'ad'

    estado = 'activo'

    if not losOperadores.buscarAdmin(correo, cedula):

        user_registro = "usuario_que_realiza_el_registro"

        losOperadores.agregarAdmin([nombre, apellido, cedula, correo, celular, rol, cifrada, estado], user_registro)
    
    else: 

        return render_template('admin/verAdmin.html' , men = "Correo o cedula no disponible")

    return redirect('/admin/verAdmin')

@app.route('/admin/validationLogin', methods = ['POST'])
def adminValidationLogin():
    if request.method == 'POST':
        correo = request.form['txtCorreo']
        contrasena = request.form['txtPassword']

        encriptada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

        resultados = validaLoginAdmin.validaLogin(correo, encriptada)

        print(resultados)

        if len(resultados) > 0:
            if resultados[0][1]:
                session["logueado"] = True
                session["user_name"] = resultados[0][1]

                return render_template("admin/index.html")

        else:
                return render_template('admin/login.html', mensaje = "Acesso denegado")
        




if __name__ == '__main__':
    app.run(debug=True)