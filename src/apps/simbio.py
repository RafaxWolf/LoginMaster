import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import os
import socket
import threading
from dotenv import load_dotenv
load_dotenv()

def recibir(con_server):
    while True:
        try:
            recibirdatos = str(con_server.recv(1024).decode("utf-8"))
            if ":" in recibirdatos:
                user, mensajedeluser = recibirdatos.split(":",1)
                user = user.strip()
                mensajedeluser = mensajedeluser.strip()

                box.config(state="normal")
                box.insert("end",f"\n{user}",("color","bold"))
                box.insert("end",f": {mensajedeluser}",("chat"))
            #user = recibirdatos.split(":",1)[0]
            #mensajedeluser = recibirdatos.split(":",1)[1]
            #box.insert("end",f"\n{user}",("color","bold"))
            #box.insert("end",f"{mensajedeluser}",("chat"))
            #user.box.insert("end"f"{recibirdatos},{color})
            #usuario,mensaje = recibirdatos.split(":",1)
            #usuario = usuario.strip(conectar_server.datos(recibirdatos.strip()))
            #usuario = usuario.strip()
            #mensaje = mensaje.strip()
            #box.insert("end",f"\n{usuario} {mensaje}",("chat"))
            #box.insert("end",f"\n{recibirdatos}",("chat"))
                box.config(state="disabled")
            else:
                if "se ha conectado" in recibirdatos:
                    box.config(state="normal")
                    box.insert("end",f"\n{recibirdatos}",("red","bold"))
                    box.config(state="disabled")
                else:
                    box.config(state="normal")
                    box.insert("end",f"\n{recibirdatos}",("chat"))
                    box.config(state="disabled")
            print(recibirdatos)
        except:
            print("no se pudo recibir datos")
            break


ipserver = os.getenv('SIMBIO_SERVER')
port = int(os.getenv('SIMBIO_PORT'))

con_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
con_server.connect((ipserver,port))


## pedir nickname
while True:
    nombre = simpledialog.askstring("nickname","Ingresa tu nickname (12 caracteres max.): ")
    if len(nombre) > 12 or len(nombre) <= 2:
        messagebox.showerror(title="Error",message="Ingresa un nombre válido.")
        continue
    else:
        con_server.send((f"{nombre} se ha conectado.\n").encode("utf-8"))
        break

### interfaz
ventana = tk.Tk()
ventana.geometry("600x600")
ventana.resizable(0,0)
ventana.title("Simbionte v1.1")



def enviar(event=None):
    global cont
    if mensaje.get() == "" or mensaje.get() == " ":
        messagebox.showerror(title="Error",message="Ingresa un mensaje válido.")
        
        mensaje.delete(0,tk.END)    ### poner el entry en blanco.
    else:
        ###enviar datos a server
        con_server.send((f"{nombre}: {mensaje.get()}\n").encode("utf-8"))
        box.config(state="normal")
        box.config(state="disabled")
        
        ### borrar contenido del entry al mandar
        mensaje.delete(0,tk.END)


def imprimir(): ### imprimir por consola todo el chat
    print(box.get("1.0","end").strip())



#logo = tk.PhotoImage(file="img/logosimbio.png")
#mostrarlogo = tk.Label(image=logo)
#mostrarlogo.place(x=60,y=0)

###frame de chat
frame = tk.Frame(ventana)
frame.place(x=60,y=100,width=500,height=400)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

box = tk.Text(frame, height=10, width=40, yscrollcommand=scrollbar.set)
box.place(x=0,y=0,relwidth=0.95,relheight=1.0)
scrollbar.config(command=box.yview)

###configurar fuentes
box.tag_configure("bold", font=("Arial", 10, "bold"))
box.tag_configure("chat", font=("Arial", 10))
box.tag_configure("color", foreground="blue")
box.tag_configure("red", foreground="red")
box.tag_configure("green", foreground="green")


### tirar un mensaje y cerrar acceso a esrcribir
"""
box.insert("1.0","User1",("bold","color"))
box.insert("1.end"," : hola mundo","chat")
box.config(state="disabled")
"""

mensaje = tk.Entry(ventana,width=70)
mensaje.place(x=60,y=501)
mensaje.bind("<Return>",enviar) ##usar enter para mandar un comando poner , enviar
benviar = tk.Button(ventana,text="Mandar",width=10,command=enviar) ## poner command=enviar
benviar.place(x=480,y=500)

"""
b1 = tk.Button(ventana, text="Enviar", command=imprimir)
b1.pack()
"""


print(f"[+] Debug:\n Conectado con exito a {ipserver}:{port}\n")
box.insert("end",f"Conectado con éxito al server.",("bold","green"))

hilodatos = threading.Thread(target=recibir,args=(con_server,))
hilodatos.start()

ventana.mainloop()