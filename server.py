### Librerias
from flask import Flask,request,jsonify
import mysql.connector
from mysql.connector import IntegrityError,Error
import os
from datetime import datetime
import bcrypt
import threading

def consola_input():

    while True:
        fechahoralog = datetime.now()
        fechalog = fechahoralog.strftime("%d_%m_%y")
        comando = input("")
        if comando == "/help":
            print("Ayuda:\n" \
            "/show logs >> Para mostrar los logs del dia actual.")
        elif comando == "/show log" or comando == "/show logs":
            if os.path.exists(f"logs/log-{fechalog}.log"):
                with open(f"logs/log-{fechalog}.log","r") as leerlog:
                    print(leerlog.read())    
            else:
                print("No existen logs en el dia de hoy.")
        elif comando == "/now":
            print(f"la hora actual del servidor es {fechahoralog.strftime("%d:%m:%y")}")
        else:
            print("Comando Desconocido. La lista de los comandos se desplega con /help")

consola = threading.Thread(target=consola_input,daemon=True,args=())
consola.start()

### Verifica si existe la carpeta logs, si no, la crea
if os.path.exists("logs"):
    print("existe")
else:
    os.mkdir("logs")


### Crea un log de eventos
def crearlog(mensaje):

    fechahoralog = datetime.now()

    # Deprecated:
    #fechahoralogformat = fechahoralog.strftime("%H:%M:%S_%d/%m/%y")

    # New format:
    fechalog = fechahoralog.strftime("%d_%m_%y")

    ### Crea/Edita el archivo de log actual del dia
    with open(f"logs/log-{fechalog}.log", "a") as writelog: ### a == append
        writelog.write(f"[{fechahoralog}]:{mensaje}\n")

app = Flask(__name__)

### Configuración de la base de datos
##!     Hay que ponerlo con dotenv para que no sea tan en plano xD
db_config = {
    "user":"simbio",
    "password":"simbionte123",
    "host":"0.0.0.0",
    "database":"login_db"
}


### Conexión a la base de datos
def conectar_base():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        crearlog(f"No se pudo conectar a la base de datos, error {err}")
        print(f"no se pudo conectar {err}")
        return None

@app.route("/registrar",methods=["POST","GET"])


### Registrar un usuario
def registrar():
    if request.method == "POST":
        datos = request.get_json()
        user_nick = datos.get("user")
        user_mail = datos.get("mail")
        user_passwd = datos.get("password")
        ip_usereg = request.remote_addr
        conexion = conectar_base()
        if conexion is None:
            crearlog(f"Ocurrió un error en la base de datos")
            return f"Error en la base de datos",500
        
        cursor = conexion.cursor()

        if os.path.exists("users/"+str(user_nick)):
            print("ya existe")
        else:
            os.makedirs("users/"+str(user_nick))

        try:
            query_sql = "INSERT INTO users (username,correo,passwd,ip_registro,user_type) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(query_sql,(user_nick,user_mail,user_passwd,ip_usereg,"normal"))

            conexion.commit()

            crearlog(f"El usuario: {user_nick} se registró con exito en la base de datos desde: {ip_usereg}.")
            return "Usuario registrado con exito",205
        
        except IntegrityError:
            crearlog(f"Una persona desde: {ip_usereg} intento registrarse con un usuario ya creado ({user_nick})")
            return "El usuario ya esta registrado!",206
        
        except Error as e:
            crearlog(f"La dirección: {ip_usereg} tuvo un fallo al intentar registrarse!\nProblema del server con mysql")
            return f"Error de mysql {e}",207
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    elif request.method == "GET":
        crearlog(f"La dirección: {request.remote_addr} se conectó con exito (METODO GET)")
        return "conexión exitosa!",200
    else:
        crearlog(f"La dirección: {request.remote_addr} no pudo conectarse (METODO GET)")
        return "CONEXION HORRIBLE",400


@app.route("/auth",methods=["POST"])
def auth():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    ip = request.remote_addr

    conexion = conectar_base()
    if conexion is None:
        return "Error al conectar con la base de datitos",500
    
    cursor = conexion.cursor()
    try:
        query_sql = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query_sql,(username,))
        resultado = cursor.fetchone()

        if resultado is None:
            return "El usuario no existe",404
        
        passwd_db = resultado[0].encode()

        if bcrypt.checkpw(password.encode(), passwd_db):
            crearlog(f"Inicio de sesión exitoso: {username} desde: {ip}")
            print(f"Inicio de sesión exitoso: {username} desde: {ip}")
            return f"Inicio de sesión exitoso: {username} desde: {ip}",200
        else:
            crearlog(f"El usuario: {username} desde: {ip} ingreso mal la contraseña")
            print(f"El usuario: {username} desde: {ip} ingreso mal la contraseña")
            return f"Contraseña incorrecta",401
    except Error as r:
        crearlog(f"La dirección: {ip} tuvo un problema de MySQL para iniciar sesión como {username} error:{r}")
        return f"Error de SQL {r}",500
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

app.run(debug=True)


