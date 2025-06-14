import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk ###Para insertar imagenes
import os
usuario = None
def main_home(usuario,cerrar_sesion,rango):
    if not usuario:
        usuario = "null"
    messagebox.showinfo(title="exito",message=f"{rango}")
    global mainhomew
    mainhomew = tk.Tk()
    mainhomew.geometry("600x600")
    mainhomew.minsize("600","600")
    mainhomew.title("LoginMaster | Home")
    mainhomew.config(bg="#FFFFFF")

    header = tk.Frame(mainhomew,bg="#6D8397")
    header.place(relwidth=1,relheight=0.1)

    lwelcome = tk.Label(header,text=f"Bienvenido {usuario}",font="Arial 21 bold",fg="#FFFFFF",bg="#6D8397")
    lwelcome.pack(anchor="w",pady=20,padx=20)

    mainpage = tk.Frame(mainhomew,bg="#FFFFFF")
    mainpage.place(relwidth=1,relheight=0.9,rely=0.1)

    cerrarbutton = tk.Button(header,text="Cerrar Sesión",command=cerrar_sesion)
    cerrarbutton.place(relx=0.93,rely=0.25,anchor="ne",width=100,height=30)

    l1 = tk.Label(mainpage,text="LoginMaster Services:",fg="#000000",font="Arial 29 bold" ,bg="#FFFFFF")
    l1.pack(pady=30)

    carpeta_actual = os.path.dirname(__file__)
    ruta_imagen = os.path.join(carpeta_actual,"img","loginotes.png")
    loginapp1route = Image.open(ruta_imagen)
    loginapp1img = ImageTk.PhotoImage(loginapp1route)
    loginapp1 = tk.Label(mainpage,image=loginapp1img,cursor="hand2")
    loginapp1.pack(anchor="center")

    ruta_imagen2 = os.path.join(carpeta_actual,"img","sappico.png")
    loginapp2route = Image.open(ruta_imagen2)
    loginapp2img = ImageTk.PhotoImage(loginapp2route)
    loginapp2 = tk.Label(mainpage,image=loginapp2img,cursor="hand2")
    loginapp2.pack(anchor="center",pady=30)

    mainhomew.mainloop()

def cerrar_home():
    mainhomew.destroy()

if __name__ == "__main__":
    main_home(None,None,"normal")