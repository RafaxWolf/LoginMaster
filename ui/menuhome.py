import tkinter as tk
usuario = None
def main_home(usuario):
    if not usuario:
        usuario = "null"
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

    l1 = tk.Label(mainpage,text="LoginMaster Services:",fg="#000000",font="Arial 29 bold" ,bg="#FFFFFF")
    l1.pack(pady=30)

    mainhomew.mainloop()

if __name__ == "__main__":
    main_home(None)