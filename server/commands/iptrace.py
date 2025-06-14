import socket

name = "iptrace"
description = "Find the IP address of a given domain or hostname"

def run(*args):
    if not args:
        return print("Uso: /iptrace <dominio_o_ip>")
    
    ip = args[0]


    print(f"[!] Buscando datos de la direccion IP: {ip}")
    