import tkinter as tk
def loginscreen(abrir_registro,comprobar_login):
    def switchpass():
        if switchshowpass.get():
            pinput.config(show="")
        else:
            pinput.config(show="•")
    global loginw
    loginw = tk.Tk()
    loginw.config(background="#FFFFFF")
    loginw.title("Login Master v1.1")
    loginw.geometry("400x600")
    loginw.minsize("380","600")

    header = tk.Frame(loginw,bg="#6a86eb")
    header.place(x=0,y=0,relwidth=1,relheight=0.3)
    ltitle = tk.Label(header,text="Login Master v1.1",font="Arial 30 bold",fg="#FFFFFF",background="#6a86eb",anchor=tk.CENTER)
    ltitle.pack(expand=True)


    formulario = tk.Frame(loginw,background="#FFFFFF")
    formulario.place(x=0,y=180,relwidth=1,relheight=1)

    tlabel1 = tk.Label(formulario,text="Iniciar Sesión",font="Arial 16 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel1.pack(anchor="n",pady=10)

    tlabel2 = tk.Label(formulario,text="Usuario",font="Arial 12 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel2.pack(anchor="n",pady=20)

    uinput = tk.Entry(formulario,width=25,highlightcolor="#000000",highlightthickness=2,highlightbackground="#000000",bd=0,font="Arial 12")
    uinput.pack()

    tlabel3 = tk.Label(formulario,text="Contraseña",font="Arial 12 bold",fg="#000000",background="#FFFFFF",anchor=tk.CENTER)
    tlabel3.pack(anchor="n",pady=10)

    pinput = tk.Entry(formulario,width=25,highlightcolor="#000000",highlightthickness=2,highlightbackground="#000000",bd=0,font="Arial 12",show="•")
    pinput.pack()

    switchshowpass = tk.BooleanVar()

    mostrarpass = tk.Checkbutton(formulario,text="Mostrar contraseña",variable=switchshowpass,command=switchpass,cursor="hand2",background="#FFFFFF")
    mostrarpass.pack()

    linktoregister = tk.Label(formulario,text="Si no tienes cuenta, registrate acá",fg="blue",cursor="hand2",font=("Helvetica 10 underline"),background="#FFFFFF")
    linktoregister.pack()
    linktoregister.bind("<Button-1>",lambda e: abrir_registro())


    def recolectar():
        usuario = uinput.get()
        passwd = pinput.get()
        comprobar_login(usuario,passwd)
        
    loginsubmit = tk.Button(formulario,text="Iniciar Sesión",fg="#000000",bg="#FFFFFF",activeforeground="black",
                            activebackground="#6a86eb",highlightbackground="black",highlightthickness=1,bd=1,relief="solid",
                            font=("Arial 12 bold"),cursor="hand2",command=recolectar)
    loginsubmit.pack(pady=30)
    loginw.mainloop()

def cerrar_login():
    loginw.destroy()

if __name__ == "__main__":
    print("Importar interfaz con loginscreen()")