from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory
import os
import hashlib
from admin import Administrador
from validaLoginAdmin import ValidationLoginAdmin
from categorias import Categorias
from operadores import Operadores


app = Flask(__name__)
app.secret_key = "digitalforge"
# AGREGAR UN CONTROL DE TIEMPO DE LA SESION, (SOLO SI ES REQUERIDO)

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='10.206.80.40'
app.config['MYSQL_DATABASE_USER']='backend_2'
app.config['MYSQL_DATABASE_PASSWORD']='@Andres4321'
app.config['MYSQL_DATABASE_DB']='visitabuga'


""" app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='vistabuga3.0' """

mysql.init_app(app)

conexion = mysql.connect()
cursor = conexion.cursor()

losOperadores = Administrador(mysql)
validaLoginAdmin = ValidationLoginAdmin(mysql)
lasCategorias = Categorias(mysql)
losTrabajadores = Operadores(mysql)


@app.route('/') # QUITAR EL CONTROL DE SESION CUANDO YA ESTE LISTA LA PARTE DE TURISTAS 
def admin_index():
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad' or session.get("rol") == 'op':
        return render_template('admin/index.html')
    else:
        return render_template("admin/login.html")
    
    #############################################

# ADMINISTRADORES

@app.route('/admin/login')
def adminLogin():
    return render_template('admin/login.html')

@app.route('/admin/verAdmin')
def verAdmin():
    if session.get("logueado") and session.get("rol") == 'su': 
        resultados = losOperadores.consultarAdmin()

        return render_template("admin/verAdmin.html", admins = resultados)
    else:
        return render_template("admin/login.html")

@app.route('/admin/agregar', methods = ['POST'])
def agregarAdmin():
    if session.get("logueado") and session.get("rol") == 'su':

        nombre = request.form['txtNombre']
        apellido = request.form['txtApellido']
        cedula = request.form['txtCedula']
        correo = request.form['txtCorreo']
        celular = request.form['txtCelular']
        contrasena = request.form['txtPassword']

        nom_sitio = request.form['nom_sitio']
        categoria_sitio = request.form['categoria_sitio']
        sector = request.form['sector']

        sentencia_contar = f"SELECT COUNT(id) AS total FROM sitios"
        cursor.execute(sentencia_contar)
        resultado = cursor.fetchall()
        conexion.commit()

        string = nom_sitio

        cod_p1 = string[0:2]

        string = categoria_sitio

        cod_p2 =  string[0:2]

        

        cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

        rol = 'ad'

        estado = 'activo'

        if not losOperadores.buscarAdmin(correo, cedula):

            losOperadores.agregarAdmin([nombre, apellido, cedula, correo, celular, rol, cifrada, estado], session['user_name'])

            return redirect('/admin/verAdmin')
        
        else: 

            return render_template('admin/verAdmin.html' , men = "Correo o cedula no disponible")

    else:
        return render_template("admin/login.html")

@app.route('/admin/desactivar/<id>')
def desactivarAdmin(id):
        if session.get("logueado") and session.get("rol") == 'su':

            losOperadores.desactivarAdmin(id)
            return redirect('/admin/verAdmin')
        
        else:
            return render_template("admin/login.html")
        
@app.route('/admin/eliminar/<id>')
def eliminarAdmin(id):
    if session.get("logueado") and session.get("rol") == 'su':
        losOperadores.eliminarAdmin(id)
        return redirect('/admin/verAdmin')
    else:
            return render_template("admin/login.html")
        
# Validacion de login de administradores, operadores

@app.route('/admin/validationLogin', methods = ['POST'])
def adminValidationLogin():
    if request.method == 'POST':
        correo = request.form['txtCorreo']
        contrasena = request.form['txtPassword']

        encriptada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

        resultados = validaLoginAdmin.validaLogin(correo, encriptada)

        print(resultados)

        if len(resultados) > 0:
            if encriptada == resultados[0][2]:
                session["logueado"] = True
                session["user_name"] = resultados[0][0]
                session["rol"] = resultados[0][3]

                if session["rol"] == 'ad':
                    return render_template("admin/index.html")
                elif session["rol"] == 'su':
                    return render_template("admin/index.html")
                elif session["rol"] == 'op':
                    return render_template("admin/index.html")
                else:
                    return render_template("admin/login.html", mensaje = "Acesso denegado")

        else:
            return render_template('admin/login.html', mensaje = "Acesso denegado")
        
@app.route('/admin/cerrar')
def adminLoginCerrar():
    session.clear()
    return redirect('/admin/login')


####################################################################

# CATEGORIAS
        
@app.route('/admin/categorias')
def admincateg():
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad' or session.get("rol") == 'op':

        resultado_categorias = lasCategorias.consulta_categorias()
        
        return render_template('admin/categorias.html', admin_cate = resultado_categorias)
    else:
        return render_template("admin/login.html")


@app.route('/admin/categorias/agregar', methods= ['POST'])
def agregarCategoria():
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad' or session.get("rol") == 'op':

        nombre_categorias = request.form['txtCategorias']

        lasCategorias.agregar_categorias([nombre_categorias], session['user_name'])

        return redirect('/admin/categorias')
    else:
        return render_template("admin/login.html")
    
@app.route('/admin/categorias_desactivar/<id>')
def desactivarCategoria(id):
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad' or session.get("rol") == 'op':
        

        lasCategorias.desactivar_categorias(id)

        return redirect('/admin/categorias')
    
    else:
        return render_template("admin/login.html")
    
@app.route('/admin/eliminarCategorias/<id>')
def eliminarCategoria(id):
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad':

        lasCategorias.eliminar_categorias(id)

        return redirect('/admin/categorias')
    else:
        return render_template("admin/login.html")
    
# Registro de operadores por parte de los administradores

@app.route('/admin/operadores')
def verOperador():
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad': 
        resultados = losTrabajadores.consultarOperador()

        return render_template("admin/operadores.html", operadores = resultados)
    else:
        return render_template("admin/login.html")

@app.route('/admin/agregar/operador', methods = ['POST'])
def agregarOperadores():
    if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad': 

        nombre = request.form['txtNombre']
        apellido = request.form['txtApellido']
        cedula = request.form['txtCedula']
        correo = request.form['txtCorreo']
        celular = request.form['txtCelular']
        contrasena = request.form['txtPassword']
            
        cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

        rol = 'op'

        estado = 'activo'

        if not losTrabajadores.buscarOperador(correo, cedula):

            losTrabajadores.agregarOperadores([nombre, apellido, cedula, correo, celular, rol, cifrada, estado], session['user_name'])

            return redirect('/admin/operadores')

        else:
            return render_template("admin/operadores.html", men = "Correo o cedula no disponible")
    
    else:
        return render_template("admin/login.html")
    

@app.route('/admin/desactivarOpe/<id>')
def desactivarOpe(id):
        if session.get("logueado") and session.get("rol") == 'su' or session.get("rol") == 'ad':

            losTrabajadores.desactivarOpe(id)
            return redirect('/admin/operadores')
        
        else:
            return render_template("admin/login.html")
        
@app.route('/admin/eliminar/operador/<id>')
def eliminarOperador(id):
    if session.get("logueado") and session.get("rol") == 'su' and session.get("rol") == 'ad':
        losTrabajadores.eliminarOpe(id)
        return redirect("/admin/operadores")
    else:
            return render_template("admin/login.html")
    
# TURISTAS

@app.route('/turistas/registro')
def turistasLogin():
    return render_template("sitio/registro.html")

@app.route('/turistas/agregar', methods = ['POST'])
def agregarTurista():
    nombre = request.form['txtNombre']
    apellido = request.form['txtApellido']
    cedula = request.form['txtCedula']
    correo = request.form['txtCorreo']
    celular = request.form['txtCelular']
    contrasena = request.form['txtPassword']

    cifrada = hashlib.sha512(contrasena.encode("utf-8")).hexdigest()

    rol = 'us'

    estado = 'activo'




        

# AGREGAR SITIOS TURISTICOS

""" @app.route('/admin/agregar/sitio', methods = ['POST'])
def agregarSitioTuristicos(): """





if __name__ == '__main__':
    app.run(debug=True)