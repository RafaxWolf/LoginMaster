###LOGIN MASTER NOTEPAD VERSION 1.0 MADE BY LOGINMASTER_DEV_TEAM
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog
from tkinter import simpledialog

def guardar_archivo():
    print(notepad.get("1.0","end").strip())
    ruta = filedialog.asksaveasfilename(filetypes=[("All Files","*.*"),
                                                   ("Text File","*.txt"),
                                                   ("Python no Window File","*.pyw"),
                                                   ("Python File","*.py"),
                                                   ("HTML file","*.html"),
                                                   ("PHP File","*.php"),
                                                   ("CSS File","*.css"),
                                                   ("JavaScript File","*.js"),
                                                   ("C++ File","*.cpp")])
    if ruta:
        with open(ruta,"w") as guardarfile:
            guardarfile.write(notepad.get("1.0","end").strip())
            messagebox.showinfo(title="Exito",message="Guardaste el archivo con exito.")
    else:
        messagebox.showerror(title="Error",message="Selecciona una ruta válida.")

def abrir_archivo():
    abrirfile = filedialog.askopenfilename()

    if abrirfile:
        print(abrirfile)
        with open(abrirfile,"r",encoding="utf-8") as contentfile:
            notepad.delete("1.0",tk.END)
            notepad.insert(tk.END,contentfile.read())

    else:
        messagebox.showerror(title="Error",message="No seleccionaste una ruta válida.")

def pegar():
    if notepad.clipboard_get():
        portapapeles = notepadv.clipboard_get()
        notepad.insert(tk.END,portapapeles)
    else:
        print("no hay nada en el portapapeles.")
def copiar():
    notepadv.clipboard_clear()
    notepadv.clipboard_append(notepad.get("1.0","end").strip())

notepadv = tk.Tk()
notepadv.geometry("300x300")
notepadv.title("Notepad LoginMaster")


barra_menu = tk.Menu(notepadv)
menu_archivo = tk.Menu(barra_menu,tearoff=0)
menu_archivo.add_command(label="Abrir",command=abrir_archivo)
menu_archivo.add_command(label="Guardar",command=guardar_archivo)
barra_menu.add_cascade(label="Archivo",menu=menu_archivo)
editar_menu = tk.Menu(barra_menu,tearoff=0)
editar_menu.add_command(label="Pegar",command=pegar)

barra_menu.add_cascade(label="Editar",menu=editar_menu)
notepadv.config(menu=barra_menu) ### mostrar el menu

notepad = tk.Text(notepadv,font="Arial 12")
notepad.place(relwidth=1,relheight=1)
notepadv.mainloop()