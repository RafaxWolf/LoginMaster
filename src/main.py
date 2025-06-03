import os, json
import tkinter as tk
from tkinter import messagebox

def quit():
    print("[!] Salindo...")
    #messagebox.showinfo(title="Info",message="Saliendo del programa.")
    exit()

def regwindow():
    def backreg():
        print("[!] Volviendo...")
        regwindow.destroy()
        mainWindow()

    def registrarse():
        if userreg.get() == "" or " " in userreg.get():
            messagebox.showerror(title="Error",message="Ingresa un usuario válido.")
        else:
            if os.path.exists("database.json"):
                with open("database.json", "r") as database:
                    diccionario = json.load(database)
                    print("Base de datos cargada.")
            else:
                diccionario = {}
                with open("database.json","w") as imprimir:
                    json.dump(diccionario, imprimir,indent= 4)

            with open("database.json", "r") as verify:
                cuentas = json.load(verify)
                if userreg.get() in cuentas:
                    messagebox.showerror(title="Error",message="Ya existe una cuenta con ese nombre.")
                else:
                    diccionario[userreg.get()] = passreg.get()
                    with open("database.json","w") as registrarendata:
                        json.dump(diccionario,registrarendata,indent=4)
                    messagebox.showinfo(title="Exito",message="Cuenta creada con exito.")
                    backreg()

    regwindow = tk.Tk()
    regwindow.geometry("300x300+800+350")
    regwindow.title("Registrarse.")

    li1 = tk.Label(regwindow,text="Registrarse",font="Arial 20 bold")
    li1.place(x=70,y=20) 
    li2 = tk.Label(regwindow,text="usuario:",font="Arial 10 bold")
    li2.place(x=125,y=60)

    userreg = tk.Entry(regwindow,width=30)
    userreg.place(x=60,y=80)


    li3 = tk.Label(regwindow,text="Contraseña:",font="Arial 10 bold")
    li3.place(x=115,y=120)

            
    passreg = tk.Entry(regwindow,width=30,show="*")
    passreg.place(x=60,y=140)

    inicio = tk.Button(regwindow,text="Registrarse",width=20,command=registrarse)
    inicio.place(x=80,y=190)
    
    volver = tk.Button(regwindow,text="Volver",command=backreg)
    volver.place(x=135,y=250)

    regwindow.mainloop()



def loginwindow():

    def back():
        print("[!] Volviendo...")
        loginwindow.destroy()
        mainWindow()

    def login():
        if userlogin.get() == "" or " " in userlogin.get():
            messagebox.showerror(title="Error",message="Ingresa un usuario válido.")
        elif passlogin.get() == "" or " " in passlogin.get():
            messagebox.showerror(title="Error",message="Ingresa una contraseña válida.")
        else:
            if os.path.exists("database.json"):
                with open("database.json", "r") as database:
                    diccionario = json.load(database)
                    print("Base de datos cargada.")

                    if userlogin.get() in diccionario and diccionario[userlogin.get()] == passlogin.get():
                        print("iniciaste sesion")
                        messagebox.showinfo(title="Inicio de sesion",message=f"Iniciaste sesion como {userlogin.get()}")
                        
                        session = userlogin.get()
                        loginwindow.destroy()
                        
                        import apps.simbio as simbio

                    else:
                        messagebox.showerror(title="Error",message="Usuario o contraseña no valido!")
                        print("[!] Usuario o contraseña no valido")
                        back()

    loginwindow = tk.Tk()
    loginwindow.geometry("300x300+800+350")
    loginwindow.title("Iniciar Sesión.")


    li1 = tk.Label(loginwindow,text="Iniciar Sesión",font="Arial 20 bold")
    li1.place(x=60,y=20)
            
    li2 = tk.Label(loginwindow,text="Usuario:",font="Arial 10 bold")
    li2.place(x=125,y=60)

    userlogin = tk.Entry(loginwindow,width=30)
    userlogin.place(x=60,y=80)


    li3 = tk.Label(loginwindow,text="Contraseña:",font="Arial 10 bold")
    li3.place(x=115,y=120)

            
    passlogin = tk.Entry(loginwindow,width=30,show="*")
    passlogin.place(x=60,y=140)

    inicio = tk.Button(loginwindow,text="Iniciar Sesión",width=20,command=login)
    inicio.place(x=80,y=190)
    
    volver = tk.Button(loginwindow,text="Volver",command=back)
    volver.place(x=135,y=250)

    loginwindow.mainloop()



def register(): # Registro
    print("[+] Debug Backend: Iniciando una nueva entrada en la base de datos...")
    v.destroy()
    regwindow()

def login():

    if os.path.exists("database.json"):
        print("[+] Debug Backend: Intentando un inicio de sesion...")
        v.destroy()
        loginwindow()
    else:
        print("[!] Debug Backend: No hay base de datos!")
        messagebox.showerror(title="Error",message="No hay usuarios registrados.")


def mainWindow(): # Principal

    # Ventana Principal
    global v
    v = tk.Tk()
    v.title("LoginMaster")
    v.geometry("300x400+800+350")
    v.resizable(0,0)

    l1 = tk.Label(v,text="LoginMaster Pre-Alpha v2.0",font="Arial 10 bold")
    l1.place(x=65,y=20)

    # Boton Inicio de sesion
    b1 = tk.Button(v,text="Iniciar sesión",width=30,command=login)
    b1.place(x=40,y=60)

    l2 = tk.Label(v,text="",font="Arial 14 bold")
    l2.pack()

    # Boton Registrarse
    b2 = tk.Button(v,text="Registrarse",width=30,command=register)
    b2.place(x=40,y=120)


    l3 = tk.Label(v,text="Todos los derechos reservados. 2025 ©",font="Arial 9 bold")
    l3.place(x=30,y=360)

    # Boton de salir
    b3 = tk.Button(v,text="Salir",width=30,command=quit)
    b3.place(x=40,y=180)

    v.mainloop()


mainWindow()