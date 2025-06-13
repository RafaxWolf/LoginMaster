import socket

name = "ipfind"
description = "Find the IP address of a given domain or hostname"

def run(*args):
    if not args:
        return "Uso: /ipfind <dominio o ip>", 400
    
    domain = args[0]
    