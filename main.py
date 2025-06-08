from ui.login_ui import loginscreen, cerrar_login
from ui.register_ui import registerscreen, cerrar_register
from tkinter import messagebox
import requests
urlregistrar = "http://127.0.0.1:5000/registrar"
def linkregistro():
    cerrar_login()
    input()

def abrir_login():
    print("abriendo login")
    cerrar_register()
    loginscreen(linkregistro,abrir_registro)

def comprobardatos(usuario,correo,passwd,conpasswd): ###comprueba si los datos del registro se pueden mandar a la base de datos
    if not usuario or not correo or not passwd or not conpasswd:
         messagebox.showerror(title="Error",message="Uno o más campos estan vacios.")
    elif " " in usuario or " " in correo or " " in passwd or " " in conpasswd:
        messagebox.showerror(title="Error",message="Los campos no pueden contener espacios!!")
    elif len(usuario) > 20:
        messagebox.showerror(title="Error",message="El campo usuario es de 20 cáracteres max.")
    elif len(correo) > 40:
        messagebox.showerror(title="Error",message="El campo correo es de 40 cáracteres max.")
    elif len(passwd) > 40:
        messagebox.showerror(title="Error",message="El campo contraseña es de 40 cáracteres max.")
    elif len(usuario) < 3:
        messagebox.showerror(title="Error",message="El nombre de usuario es muy corto.")  
    elif len(correo) < 3:
        messagebox.showerror(title="Error",message="El correo es muy corto.")  
    elif len(passwd) < 6:
        messagebox.showerror(title="Error",message="la contraseña tiene que se de mas de 6 caracteres.")  
    elif not "@" in correo:
        messagebox.showerror(title="Error",message="Ingresa un correo válido")  
    elif passwd != conpasswd:
        messagebox.showerror(title="Error",message="Las contraseñas no coinciden!")
    else:
        try:
            solicitud = requests.get(urlregistrar)

            if solicitud.status_code == 200:
                cuenta = {
                    "user":usuario,
                    "mail":correo,
                    "password":passwd
                }
                solicitudpost = requests.post(urlregistrar,json=cuenta)

                messagebox.showinfo(title="Exito",message=f"te conectaste con exito a la api: {solicitudpost.text}")

                if solicitudpost.status_code == 205:
                    messagebox.showinfo(title="exito",message=f"{solicitudpost.text}")
                elif solicitud.status_code == 206:
                    messagebox.showwarning(title="Atencion",message=f"{solicitudpost.text}")
                elif solicitud.status_code == 207:
                    messagebox.showerror(title="Error",message=f"{solicitudpost.text}")
                else:
                    messagebox.showerror(title="Error",message="Error fatal")                    
            else:
                messagebox.showerror(title="Error",message=f"{solicitud.status_code} {solicitud.text}")
        except requests.exceptions.RequestException as err:
            messagebox.showerror(title="Error",message=f"error critico: {err}")


def comprobar_login(usuario,passwd):
    if not usuario or not passwd:
        messagebox.showerror(title="ERROR",message="Hay un campo vacio.")
    elif " " in usuario or " " in passwd:
        messagebox.showerror(title="ERROR",message="No pongas espacios en los campos.")
    elif len(usuario) > 20:
        messagebox.showerror(title="ERROR",message="Los usuarios solo tienen 20 caracteres como maximo.")
    elif len(usuario) > 40:
        messagebox.showerror(title="ERROR",message="La contraseña es muy larga para una cuenta.")
    else:
        urlinicio = "http://127.0.0.1:5000/auth"
        data = {
            "username":usuario,
            "password":passwd
        }

        try:
            solicitudlogin = requests.post(urlinicio,json=data)

            if solicitudlogin.status_code == 200:
                messagebox.showinfo(title="Exito",message="Iniciaste sesión!")
                print("iniciaste sesion")
            elif solicitudlogin.status_code == 401:
                messagebox.showerror(title="Error",message="Contraseña incorrecta!")
                print("contraseña incorrecta")
            elif solicitudlogin.status_code == 404:
                messagebox.showerror(title="Error",message=f"No existe el usuario {usuario}.")
                print("No existe el usuario")
            else:
                messagebox.showerror(title="Error",message=f"Error imposible {solicitudlogin.status_code} === {solicitudlogin.text}")
                print(f"Error imposible {solicitudlogin.status_code} === {solicitudlogin.text}")

        except requests.exceptions.RequestException as rr:
            messagebox.showerror(title="Error",message=f"no hay conexion con el servidorss === {rr}")
            print(f"no hay conexion con el servidorss === {rr}")

def abrir_registro():
    print("abriendo registro")
    cerrar_login()
    registerscreen(comprobardatos,abrir_login)


if __name__ == "__main__":
    loginscreen(abrir_registro,comprobar_login)