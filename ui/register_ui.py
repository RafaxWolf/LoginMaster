import tkinter as tk
def registerscreen(comprobardatos,abrir_login):
    global registerw
    registerw = tk.Tk()
    registerw.config(background="#FFFFFF")
    registerw.title("Login Master v1.1")
    registerw.geometry("400x600")
    registerw.minsize("380","600")

    header = tk.Frame(registerw,bg="#6a86eb")
    header.place(x=0,y=0,relwidth=1,relheight=0.3)
    ltitle = tk.Label(header,text="Login Master v1.1",font="Arial 30 bold",fg="#FFFFFF",background="#6a86eb",anchor=tk.CENTER)
    ltitle.pack(expand=True)


    formulario = tk.Frame(registerw,background="#FFFFFF")
    formulario.place(x=0,y=180,relwidth=1,relheight=1)

    tlabel1 = tk.Label(formulario,text="Registrarte",font="Arial 16 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel1.pack(anchor="n",pady=10)

    tlabel2 = tk.Label(formulario,text="Username",font="Arial 12 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel2.pack(anchor="n",pady=2)

    userinput = tk.Entry(formulario,width=25,highlightcolor="#000000",highlightthickness=2,highlightbackground="#000000",bd=0,font="Arial 12")
    userinput.pack()

    tlabel3 = tk.Label(formulario,text="Correo",font="Arial 12 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel3.pack(anchor="n",pady=2)

    correoinput = tk.Entry(formulario,width=25,highlightcolor="#000000",highlightthickness=2,highlightbackground="#000000",bd=0,font="Arial 12")
    correoinput.pack()

    tlabel4 = tk.Label(formulario,text="Contraseña",font="Arial 12 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel4.pack(anchor="n",pady=10)

    pwdinput = tk.Entry(formulario,width=25,highlightcolor="#000000",highlightthickness=2,highlightbackground="#000000",bd=0,font="Arial 12",show="•")
    pwdinput.pack()

    tlabel5 = tk.Label(formulario,text="Confirmar Contraseña",font="Arial 12 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel5.pack(anchor="n",pady=10)

    conpwdinput = tk.Entry(formulario,width=25,highlightcolor="#000000",highlightthickness=2,highlightbackground="#000000",bd=0,font="Arial 12",show="•")
    conpwdinput.pack()


    linktologin = tk.Label(formulario,text="Si no tienes cuenta, registrate acá",fg="blue",cursor="hand2",font=("Helvetica 10 underline"),background="#FFFFFF")
    linktologin.pack()
    linktologin.bind("<Button-1>",lambda e: abrir_login())


    def mandardatos():
        usuario = userinput.get()
        correo = correoinput.get()
        passwd = pwdinput.get()
        confpasswd = conpwdinput.get()
        comprobardatos(usuario,correo,passwd,confpasswd)
    registersubmit = tk.Button(formulario,text="Registrarse",fg="#000000",bg="#FFFFFF",activeforeground="black",
                            activebackground="#6a86eb",highlightbackground="black",highlightthickness=1,bd=1,relief="solid",
                            font=("Arial 12 bold"),cursor="hand2",command=mandardatos)
    registersubmit.pack(pady=30)
    registerw.mainloop()

def cerrar_register():
    registerw.destroy()

if __name__ == "__main__":
    print("Ejecutar desde main.py!!")