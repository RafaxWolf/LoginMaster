###ola
from flask import Flask,request,jsonify
import mysql.connector
from mysql.connector import IntegrityError,Error
import os
app = Flask(__name__)

db_config = {
    "user":"root",
    "password":"",
    "host":"localhost",
    "database":"loginmaster_db"
}

def conectar_base():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"no se pudo conectar {err}")
        return None

@app.route("/registrar",methods=["POST","GET"])

def registrar():
    if request.method == "POST":
        datos = request.get_json()
        user_nick = datos.get("user")
        user_mail = datos.get("mail")
        user_passwd = datos.get("password")
        ip_usereg = request.remote_addr
        print(f"usuario: {user_nick}\nmail:{user_mail}\npasswd:{user_passwd}")
        conexion = conectar_base()
        if conexion is None:
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


            return "Usuario registrado con exito",205
        
        except IntegrityError:
            return "El usuario ya esta registrado!",206
        
        except Error as e:
            return f"Error de mysql {e}",207
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    elif request.method == "GET":
        return "conexión exitosa!",200
    else:
        return "CONEXION ORRIBLE",400
    
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
        cursor.execute("SELECT passwd FROM users WHERE username = %s",(username,))
        resultado = cursor.fetchone()

        if resultado is None:
            return "El usuario no existe",404
        
        passwd_db = resultado[0]

        if passwd_db == password:
            print(f"Inicio de sesión exitoso {username} desde {ip}")
            return f"Inicio de sesión exitoso {username} desde {ip}",200
        else:
            print(f"el usuario {username} desde {ip} ingreso mal la contraseña")
            return f"Contraseña incorrecta",401
    except Error as r:
        return f"Error de sql {r}",500
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

app.run(debug=True)