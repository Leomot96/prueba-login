from flask import Flask
from flask import render_template, redirect, request, Response, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='login'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL (app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ingreso')
def ingreso():
    return render_template('ingreso.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

#FUNCION DE INICIO DE SESION
@app.route('/acceso-login', methods = ["GET","POST"])
def login():

    if request.method == 'POST' and 'txtUsuario' in request.form and 'txtPassword':
        _usuario = request.form ['txtUsuario']
        _password = request.form ['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE user = %s AND password = %s', (_usuario,_password,))
        account = cur.fetchone()

        if account:
            session['logueado']=True
            session['id'] = account['id']

            return render_template("ingreso.html")
        else:


            return render_template('index.html', mensaje="Usuario o contraseña incorrecto")

#FUNCION REGISTRO
@app.route('/crear-registro', methods = ["GET","POST"])
def crear_registro():

    usuario = request.form ['txtUsuario']
    correo = request.form ['txtCorreo']
    password = request.form ['txtPassword']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO usuarios (user, correo, password) VALUES (%s, %s, %s)", (usuario,correo,password,))
    mysql.connection.commit()

    return render_template("index.html", mensaje2="Usuario registrado")

#CERRAR SESION
@app.route('/cerrar-sesion', methods = ["GET","POST"])
def cerrar_sesion():

    return render_template("index.html", mensaje3="La sesión ah finalizado")

if __name__ == '__main__':
    app.secret_key="leonardo_hds"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)