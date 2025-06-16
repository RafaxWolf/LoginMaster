import socket
import time

# Necessary
name = "ping"
description = "Ping command for server"

# Command
def run(*args):
    print("[+] Obteniendo el tiempo de respuesta del servidor...")
    try:
        start_time = time.time()
        # Conectar al servidor
        socket.create_connection(("localhost", 5000), timeout=5)
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        print(f"[+] Tiempo de respuesta del servidor: {response_time:.2f} ms")
    except socket.timeout:
        print("[-] Tiempo de espera agotado al intentar conectar al servidor.")
        return
    except socket.error as e:
        print(f"[-] Error al conectarse con el servidor: {e}")
        return