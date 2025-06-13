### Libreriasss
from flask import Flask,request,jsonify
import mysql.connector
from mysql.connector import IntegrityError,Error
from datetime import datetime
import os
import bcrypt
import importlib
import threading
import time
import io
import contextlib

### Verifica si existe la carpeta logs, si no, la crea
if not os.path.exists("logs"):
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
        writelog.write(f"[{fechahoralog}]: {mensaje}\n")

app = Flask(__name__)

### Configuración de la base de datos
##!     Hay que ponerlo con dotenv para que no sea tan en plano xD
db_config = {
    "user":"simbio",
    "password":"simbionte123",
    "host":"0.0.0.0",
    "database":"login_db"
}

commands_dir = os.path.join(os.path.dirname(__file__), 'commands')

### Conexión a la base de datos
def conectar_base():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        crearlog(f"No se pudo conectar a la base de datos, error {err}")
        print(f"no se pudo conectar {err}")
        return None


###                      Cargador de comandos
def load_commands():
    time.sleep(1)  # Espera un segundo para asegurar que el servidor esté listo
    print("[+] Cargando comandos...")
    commands = {}
    if os.path.exists(commands_dir): # Verifica si el directorio 'commands' existe
        for file in os.listdir(commands_dir):
            if file.endswith(".py"):
                command_name = file[:-3] # Elimina la extensión .py
                command = importlib.import_module(f"commands.{command_name}")

                if hasattr(command, 'name') and hasattr(command, 'run'):
                    commands[command.name] = {
                        'description': getattr(command, 'description', 'No description provided'), # Obtiene la descripción del comando, si no existe, asigna un valor por defecto
                        'run': command.run # Asigna la función run del comando
                    }
        return commands
        
    
    else: # Si el directorio 'commands' no existe, lo crea
        print("[!] El directorio 'commands' no existe, creando el directorio...")
        os.mkdir(commands_dir)
        print("[+] Directorio 'commands' creado.")
        print("[+] Ahora puedes agregar comandos personalizados en el directorio 'commands'\n")

###                         Consola del servidor
def server_cli():
    time.sleep(1)  # Espera un segundo para asegurar que el servidor esté listo
    commands = load_commands() # Carga los comandos desde el directorio 'commands'
    print("[+] Console initialized, type '/help' for commands. [+]\n")
    while True:
        cmd = input(">> ").strip()
        if cmd.startswith("/"):
            parts = cmd[1:].split()
            if not parts:
                continue

            command = parts[0]
            args = parts[1:]

            ### Manejo de comandos
            if command == "help": # Comando para mostrar la ayuda
                print("[+] Comandos Disponibles:\n")
                print("/help - Show this help message")
                print("/clear - Clear the console")
                try:
                    for c, info in commands.items():
                        print(f"/{c} - {info['description']}")
                except Exception as e:
                    continue
                continue
            elif command == "clear": # Comando para limpiar la consola
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            elif command in commands: # Verifica si el comando ejecutado existe en el diccionario de comandos
                try:
                    buffer = io.StringIO() # Crea un buffer para capturar la salida del comando
                    with contextlib.redirect_stdout(buffer): # Redirige la salida estándar al buffer
                        commands[command]['run'](*args)
                    output = buffer.getvalue() # Obtiene el valor del buffer
                    print(output) # Imprime el valor del buffer en la consola

                    crearlog(f"Comando ejecutado: {command} con argumentos: {args}")
                    crearlog(output)
                except Exception as e: # Si ocurre un error al ejecutar el comando, muestra un mensaje de error
                    crearlog(f"[!] Error al ejecutar el comando {command}: {e}")
                    print(f"[!] Error al ejecutar el comando {command}: {e}")
            else: # Si el comando no existe, muestra un mensaje de error
                crearlog(f"[!] Comando desconocido: {command}")
                print(f"[!] Comando desconocido: {command} - Use '/help' para ver los comandos disponibles.")
        elif cmd == "clear" or cmd == "cls":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        elif cmd == "":
            continue
        else:
            print("[!] Error:\nEl prefix de los comandos es: '/'\nPor favor, usa el prefix para ejecutar los comandos.\n")
            continue

# -------------------------------------------------------------------------------------------------------
# |                                               ENDPONTS                                              |
# -------------------------------------------------------------------------------------------------------

### Registrar un usuario
@app.route("/registrar",methods=["POST","GET"])
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
            print("[!] El usuario ya existe!")
        else:
            os.makedirs("users/"+str(user_nick))

        try:
            query_sql = "INSERT INTO users (username,correo,passwd,ip_registro,user_type) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(query_sql,(user_nick,user_mail,user_passwd,ip_usereg,"normal"))

            conexion.commit()

            crearlog(f"[+] El usuario: {user_nick} se registró con exito en la base de datos desde: {ip_usereg}.")
            return "Usuario registrado con exito",205
        
        except IntegrityError:
            crearlog(f"[+] Una persona desde: {ip_usereg} intento registrarse con un usuario ya creado ({user_nick})")
            return "El usuario ya esta registrado!",206
        
        except Error as e:
            crearlog(f"[!] La dirección: {ip_usereg} tuvo un fallo al intentar registrarse!\nProblema del server con mysql")
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

### Verificar si un usuario ya existe
@app.route("/verificar_user",methods=["GET"])
def verificar_user():
    user = request.args.get("user")
    if not user:
        crearlog("[!] Usuario no proporcionado para verificar")
        return "Usuario no proporcionado",400
    
    conexion = conectar_base()
    if conexion is None:
        crearlog("[!] Error al conectar a la base de datos para verificar usuario")
        return "Error al conectar con la base de datos",500
    
    cursor = conexion.cursor()
    try:
        query_sql = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query_sql, (user,))
        resultado = cursor.fetchone()

        if resultado:
            crearlog(f"[!] Verificacion: El usuario {user} ya existe en la base de datos")
            return jsonify({"existe": True}), 200
        else:
            crearlog(f"[+] Verificacion: El usuario {user} no existe en la base de datos")
            return jsonify({"existe": False}), 200

    except Error as e:
        crearlog(f"[!] Error al verificar el usuario: {e}")
        return f"Error al verificar el usuario: {e}",500
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route("/verificar_mail",methods=["GET"])
def verificar_mail():
    mail = request.args.get("mail")
    if not mail:
        crearlog("[!] Correo no proporcionado para verificar")
        return "Correo no proporcionado",400
    
    conexion = conectar_base()
    if conexion is None:
        crearlog("[!] Error al conectar a la base de datos para verificar usuario")
        return "Error al conectar con la base de datos",500
    
    cursor = conexion.cursor()
    try:
        query_sql = "SELECT correo FROM users WHERE correo = %s"
        cursor.execute(query_sql, (mail,))
        resultado = cursor.fetchone()

        if resultado:
            crearlog(f"[!] Verificacion: El correo {mail} ya existe en la base de datos")
            return jsonify({"existe": True}), 200
        else:
            crearlog(f"[+] Verificacion: El correo {mail} no existe en la base de datos")
            return jsonify({"existe": False}), 200

    except Error as e:
        crearlog(f"[!] Error al verificar el correo: {e}")
        return f"Error al verificar el correo: {e}",500
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

### Iniciar sesion de un usuario
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

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        #crearlog("[+] Iniciando el servidor Flask...")
        console = threading.Thread(target=server_cli,daemon=True,args=())
        console.start()

app.run(debug=True)