###                         ARCHIVO PRINCIPAL DEL SERVIDOR

#* Librerias
import os, signal, bcrypt, importlib, threading, time, io, contextlib

from flask import Flask,request,jsonify
import mysql.connector
from mysql.connector import IntegrityError,Error
from datetime import datetime

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

#* ╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗
#* ║                                             /  CONFIG /                                             ║
#* ╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝

###* Carpetas del servidor
commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
## Aqui se pueden agregar las carpetas para las distintas funciones del servidor
## TODO: Posiblemente meter el "Commands Handler" a una carpeta "Functions" en un futuro pero eso seria mucha pega
#! Verifica que el directorio de logs exista, si no, lo crea
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

###* Configuración del servidor
serverip = "0.0.0.0" # IP del servidor 
serverport = 5000 # Puerto del servidor

#* ╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗
#* ║                                             [ LOGS ]                                                ║
#* ╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝

###* Crea un .log de eventos que ocurran en el servidor
def crearlog(mensaje):

    # Fecha y hora del Log
    fechahoralog = datetime.now()
    fechalog = fechahoralog.strftime("%d_%m_%y")

    # Crea/Edita el archivo de log actual del dia
    with open(f"logs/log-{fechalog}.log", "a") as writelog: ### a == append
        writelog.write(f"[{fechahoralog}]: {mensaje}\n")


###* Commands Loader
def load_commands():
    print("[/] Loading: Cargando comandos...")
    commands = {}
    if os.path.exists(commands_dir): #! Verifica que el directorio '/commands/' exista
        for file in os.listdir(commands_dir):
            if file.endswith(".py"): # Detecta los archivos .py
                command_name = file[:-3] # Elimina la extensión .py para hacer la importacion
                command = importlib.import_module(f"commands.{command_name}")

                if hasattr(command, 'name') and hasattr(command, 'run'):
                    commands[command.name] = {
                        'description': getattr(command, 'description', 'No description provided'), # Obtiene la descripción del comando, si no existe, asigna un valor por defecto
                        'run': command.run # Asigna la función run del comando
                    }
                    print(f"[+] {command_name} - Cargado con exito")
                else:
                    print(f"[!] {command_name} - Error al cargar.")
        return commands
        
    else: #! Si el directorio '/commands/' no existe, lo crea
        print("[!] Warning: El directorio '/commands/' no existe, creando el directorio...")
        os.mkdir(commands_dir)

        print("[+] Info: Directorio '/commands/' creado.")
        print("[+] Tip: Ahora puedes agregar comandos personalizados en el directorio '/commands/'\n")


###* Server Console (CLI)
def server_cli():
    time.sleep(1)  # Tiempo de espera para que no hayan errores
    commands = load_commands() # Carga los comandos desde el directorio '/commands/'
    print("[+] Server Console Ready, type '/help' for commands.")
    session = PromptSession()  # Consola fixeada

    with patch_stdout(): # Parchea el STOUT para que no rompa la consola (No funciona con los registros de Flask.)
        while True:
            try:
                cmd = session.prompt(">> ") # Prompt
                # --------------------------------------------------------------------------- #
                #                              Comandos sin Prefix                            #
                # --------------------------------------------------------------------------- #

                # Si no se escribe nada y se pulsa Enter no hara nada
                if cmd == "":
                        continue
                
                # Si se escribe "clear" o "cls" sin el prefix igualmente limpia la consola
                elif cmd == "clear" or cmd == "cls":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue

                # --------------------------------------------------------------------------- #
                #                              Comandos con Prefix                            #
                # --------------------------------------------------------------------------- #

                ###* Commands Prefix
                elif cmd.startswith("/"):
                    parts = cmd[1:].split()
                    if not parts:
                        continue

                    command = parts[0] ## Comando
                    args = parts[1:]   ## Argumentos

                    ###* Commands Handler
                    # Comando /Help
                    if command == "help":
                        print("\n[+] Comandos Disponibles:")
                        # Comandos Por defecto (incluidos en el Handler)
                        print("\t/help - Show this help message")
                        print("\t/clear - Clear the console")
                        print("\t/logs list - Show the logs | /logs <log_name> - Show a specific log")
                        # Comandos Customs (Carpeta "/commands/")
                        try:
                            # Obtiene el noombre del comando y su Descripcion para el Help
                            for c, info in commands.items():
                                print(f"\t/{c} - {info['description']}")
                            print() # Espacio vacio al final
                        except Exception as e: ## Si no hay comandos custom
                            print() # Espacio vacio al final
                            continue
                        continue
                    # Comando /clear | /cls
                    elif command == "clear" or command == "cls":
                        os.system('cls' if os.name == 'nt' else 'clear')
                        continue
                    # Comando /logs
                    elif command == "logs":
                        if not args:
                            print("[!] Error: ")
                            print("[+] Uso:\n\t/logs list - para listar los logs en la carpeta '/logs'\n\t/logs log-<fecha_del_log> - para ver un log específico")
                            continue

                        if args[0] == "list":
                            print("[+] Listando los logs disponibles...")
                            try:
                                # Verifica si hay logs en el directorio
                                log_files = os.listdir(logs_dir)
                                if not log_files:
                                    print("[!] No hay logs disponibles.")
                                
                                else:
                                    # Lista los archivos de log en el directorio
                                    print("[+] Logs disponibles:")
                                    for log_file in log_files:
                                        print(f"- {log_file}")

                            except Exception as e:
                                crearlog(f"[!] Error al listar los logs: {e}")
                                print(f"[!] Error al listar los logs: {e}")
                            continue

                        elif len(args) == 1:
                            log_name = args[0]
                            if log_name.startswith("log-"):
                                log_path = os.path.join(logs_dir, log_name)
                                if not os.path.exists(log_path):
                                    print(f"[!] El log '{log_name}' no existe.")
                                    continue
                            else:
                                print("[!] Uso:\n\t/logs list - para listar los logs en la carpeta '/logs'\n\t/logs log-<fecha_del_log> - para ver un log específico")
                                continue

                            try:
                                with open(log_path, 'r') as log_file:
                                    print(f"\n\t[+] Contenido del log '{log_name}':\n")
                                    print(log_file.read())
                            except Exception as e:
                                print(f"[!] Error al leer el log '{log_name}': {e}")
                            except Exception as e:
                                print(f"[!] Error al leer los logs: {e}")

                        else:
                            print("[!] Uso:\n\t/logs list - para listar los logs en la carpeta '/logs'\n\t/logs <nombre_del_log> - para ver un log específico")
                        continue
                    # Comando /exit
                    elif command == "exit":
                        print("[!] Warning: Comando '/exit' Ejeccutado!\n[!] Warning: Cerrando el servidor...")
                        time.sleep(0.2)
                        os.kill(os.getpid(), signal.SIGINT)
                        break
                    # Custom Commands
                    elif command in commands: # Si el comando es uno Custom
                        try:
                            ## Detector de output (Para poder guerdarlo en un .log)
                            buffer = io.StringIO() # Crea un buffer para capturar la salida del comando
                            with contextlib.redirect_stdout(buffer): # Redirige la salida al buffer
                                commands[command]['run'](*args)
                            output = buffer.getvalue()
                            print(output) # Imprime el output del comando
                            crearlog(f"Comando ejecutado: {command} con argumentos: {args}") # Registra como seejecuto el comando
                            crearlog(output) # Registra el output del comando
                        
                        except Exception as e: # Si ocurre un error al ejecutar el comando, muestra un mensaje de error
                            crearlog(f"[!] Error al ejecutar el comando {command}:\n{e}")
                            print(f"[!] Error al ejecutar el comando {command}:\n{e}")
                    
                    else: # Si el comando no existe, muestra un mensaje de error
                        crearlog(f"[!] Comando desconocido: {command}")
                        print(f"[!] Comando desconocido: {command} - Use '/help' para ver los comandos disponibles.")
                        continue
                # Si no es un comando (No Prefix/Default/Custom) muestra mensaje de error
                else:
                    print("[!] Error:\nEl prefix de los comandos es: '/'\nPor favor, usa el prefix para ejecutar los comandos.\n")
                    print("[?] Tip: Usa /help para ver la lista de los comandos disponibles.")
                    continue

            except (KeyboardInterrupt, EOFError):
                print("[!] Consola cerrada por el usuario!\n[!] Cerrando servidor...")
                time.sleep(0.2)
                os.kill(os.getpid(), signal.SIGINT)  # Termina el proceso actual
                break

#* ╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗
#* ║                                          < APP / DATABASE >                                         ║
#* ╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝

### Define la aplicación Flask
app = Flask(__name__)

### Configuración de la base de datos
## TODO: Hay que ponerlo con dotenv o con un JSON para que no sea tan directo XD.

db_config = {
    "user":"simbio",
    "password":"simbionte123",
    "host":"0.0.0.0",
    "database":"login_db"
}

###! Conexión a la base de datos
def conectar_base():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        crearlog(f"No se pudo conectar a la base de datos, error {err}")
        print(f"no se pudo conectar {err}")
        return None


#* ╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗
#* ║                                             ( ENDPONTS )                                            ║
#* ╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝

###? Registrar un usuario
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

#* -------------------------------------------------------------------------------------------------------

###? Verificar si un usuario y/o un correo ya existe
@app.route("/verify", methods=["GET"])
def verificar():
    user = request.args.get("user")
    mail = request.args.get("mail")

    if not user and not mail:
        crearlog("[!] No se proporcionó ni usuario ni correo para verificar")
        return "Se debe proporcionar 'user' o 'mail'", 400

    conexion = conectar_base()
    if conexion is None:
        crearlog("[!] Error al conectar a la base de datos para verificar")
        return "Error al conectar con la base de datos", 500

    cursor = conexion.cursor()
    respuesta = {}

    try:
        if user:
            cursor.execute("SELECT username FROM users WHERE username = %s", (user,))
            resultado_user = cursor.fetchone()
            existe_user = bool(resultado_user)
            respuesta["user"] = existe_user
            if existe_user:
                crearlog(f"[!] El usuario '{user}' ya existe en la base de datos")
                print(f"[!] El usuario '{user}' ya existe en la base de datos")
            else:
                crearlog(f"[+] El usuario '{user}' no existe en la base de datos")
                print(f"[+] El usuario '{user}' no existe en la base de datos")

        if mail:
            cursor.execute("SELECT correo FROM users WHERE correo = %s", (mail,))
            resultado_mail = cursor.fetchone()
            existe_mail = bool(resultado_mail)
            respuesta["mail"] = existe_mail
            if existe_mail:
                crearlog(f"[!] El correo '{mail}' ya existe en la base de datos")
                print(f"[!] El correo '{mail}' ya existe en la base de datos")
            else:
                crearlog(f"[+] El correo '{mail}' no existe en la base de datos")
                print(f"[+] El correo '{mail}' no existe en la base de datos")

        return jsonify(respuesta), 200

    except Error as e:
        crearlog(f"[!] Error al verificar: {e}")
        print(f"[!] Error al verificar: {e}")
        return f"Error al verificar: {e}", 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#* -------------------------------------------------------------------------------------------------------

###? Loggear un usuario
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
        login_query_sql = "SELECT passwd FROM users WHERE username = %s"
        cursor.execute(login_query_sql,(username,))
        resultado = cursor.fetchone()

        rank_query_sql = "SELECT user_type FROM users WHERE username = %s"
        cursor.execute(rank_query_sql,(username,))
        user_rank = cursor.fetchone()


        if resultado is None:
            return "El usuario no existe",404
        
        passwd_db = resultado[0].encode()

        if bcrypt.checkpw(password.encode(), passwd_db):
            crearlog(f"[+] Inicio de sesión exitoso: {username} | {user_rank[0]} desde: {ip}")
            print(f"[+] Inicio de sesión exitoso: {username} | {user_rank[0]} desde: {ip}")
            return f"Inicio de sesión exitoso: {username}, desde: {ip}",200
        else:
            crearlog(f"El usuario: {username} desde: {ip} ingreso mal la contraseña")
            print(f"El usuario: {username} desde: {ip} ingreso mal la contraseña")
            return f"Contraseña incorrecta",401
    except Error as r:
        crearlog(f"La dirección: {ip} tuvo un problema de MySQL para iniciar sesión como {username} error:{r}")
        print(f"La dirección: {ip} tuvo un problema de MySQL para iniciar sesión como {username} error:{r}")
        return f"Error de SQL {r}",500
    
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

#* ╔═════════════════════════════════════════════════════════════════════════════════════════════════════╗
#* ║                                       > INICIO DEL SERVIDOR <                                       ║
#* ╚═════════════════════════════════════════════════════════════════════════════════════════════════════╝

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        console = threading.Thread(target=server_cli,daemon=True,args=())
        console.start()

app.run(host=serverip,port=serverport,debug=True)