# Necessary
name = "iptrace"
description = "<ip_address> - Find the IP address of a given domain or hostname."

# Command
def run(*args):
    if not args:
        print("[!] Syntax Error: Argumento Faltante.")
        print(f"[+] Uso:\n\t /{name} {description}")
        return
    
    ip = args[0]
    print(f"[!] Buscando datos de la direccion IP: {ip} [!]")
    
    