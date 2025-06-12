from ui.login_ui import loginscreen, cerrar_login
from ui.register_ui import registerscreen, cerrar_register
from ui.menuhome import main_home
from tkinter import messagebox
import requests
import bcrypt

### URL del servidor de registro
### Cambiar esta URL por la de tu servidor si es necesario
urlregistrar = "http://52.71.116.141:5000/registrar"

### Funcion para abrir el home
def abrir_home(usuario):
    cerrar_login()
    main_home(usuario)



def comprobardatos(usuario,correo,passwd,conpasswd): ### Comprueba si los datos del registro se pueden mandar a la base de datos
    ### Si los campos estan vacios, muestra un mensaje de error
    if not usuario or not correo or not passwd or not conpasswd:
         messagebox.showerror(title="Error",message="Uno o más campos estan vacios.")

    ### Si los campos tienen espacios, muestra un mensaje de error
    elif " " in usuario or " " in correo or " " in passwd or " " in conpasswd:
        messagebox.showerror(title="Error",message="Los campos no pueden contener espacios!!")

    ### Si los campos son demasiado largos o cortos, muestra un mensaje de error
    elif len(usuario) > 20:
        messagebox.showerror(title="Error",message="El campo usuario es de 20 cáracteres max.")
    elif len(correo) > 40:
        messagebox.showerror(title="Error",message="El campo correo es de 40 cáracteres max.")
    elif len(passwd) > 40:
        messagebox.showerror(title="Error",message="El campo contraseña es de 40 cáracteres max.")
    
    ### Si el usuario, correo o contraseña son demasiado cortos, muestra un mensaje de error
    elif len(usuario) < 3:
        messagebox.showerror(title="Error",message="El nombre de usuario es muy corto.")  
    elif len(correo) < 3:
        messagebox.showerror(title="Error",message="El correo es muy corto.")  
    elif len(passwd) < 6:
        messagebox.showerror(title="Error",message="la contraseña tiene que se de mas de 6 caracteres.")

    ### Si el correo no tiene un formato valido, muestra un mensaje de error  
    elif not "@" in correo:
        messagebox.showerror(title="Error",message="Ingresa un correo válido")

    ### Si las contraseñas no coinciden, muestra un mensaje de error  
    elif passwd != conpasswd:
        messagebox.showerror(title="Error",message="Las contraseñas no coinciden!")
    else:
        try: ### Si todo es correcto, manda los datos a la base de datos
            solicitud = requests.get(urlregistrar)

            def hash_password(password):
                salt = bcrypt.gensalt()
                return bcrypt.hashpw(password.encode(), salt).decode()

            if solicitud.status_code == 200:
                cuenta = {
                    "user":usuario,
                    "mail":correo,
                    "password":hash_password(passwd)
                }
                solicitudpost = requests.post(urlregistrar,json=cuenta)

                ##! jajaja, API le pone, la wea no da ni pa proyecto de colegio TP
                messagebox.showinfo(title="Exito",message=f"te conectaste con exito a la api: {solicitudpost.text}")

                if solicitudpost.status_code == 205:
                    messagebox.showinfo(title="Exito",message=f"{solicitudpost.text}")
                elif solicitud.status_code == 206:
                    messagebox.showwarning(title="Atencion",message=f"{solicitudpost.text}")
                elif solicitud.status_code == 207:
                    messagebox.showerror(title="Error",message=f"{solicitudpost.text}")
                else:
                    messagebox.showerror(title="Error",message="Error fatal")                    
            else:
                messagebox.showerror(title="Error",message=f"{solicitud.status_code} {solicitud.text}")
        except requests.exceptions.RequestException as err:
            messagebox.showerror(title="Error",message=f"Error critico: {err}")

### Verifica si los campos de login son correctos
def comprobar_login(usuario,passwd):
    ### Si el usuario o la contraseña estan vacios, muestra un mensaje de error
    if not usuario or not passwd:
        messagebox.showerror(title="ERROR",message="Hay un campo vacio.")

    ### Si el usuario o la contraseña tienen espacios, muestra un mensaje de error
    elif " " in usuario or " " in passwd:
        messagebox.showerror(title="ERROR",message="No pongas espacios en los campos.")

    ### Si el usuario o la contraseña son demasiado cortos o largos, muestra un mensaje de error
    elif len(usuario) > 20:
        messagebox.showerror(title="ERROR",message="Los usuarios solo tienen 20 caracteres como maximo.")
    elif len(usuario) > 40:
        messagebox.showerror(title="ERROR",message="La contraseña es muy larga para una cuenta.")
    else:

        ### URL de inicio de sesión
        urlinicio = "http://52.71.116.141:5000/auth"
        data = {
            "username":usuario,
            "password":passwd
        }

        try:  ### Codigos HTTP
            solicitudlogin = requests.post(urlinicio,json=data)

            ### Si es 200 inicia la sesion
            if solicitudlogin.status_code == 200:
                messagebox.showinfo(title="Exito",message="Iniciaste sesión!")
                abrir_home(usuario)

            ### Si es 401, contraseña incorrecta
            elif solicitudlogin.status_code == 401:
                messagebox.showerror(title="Error",message="Contraseña incorrecta!")
                print("contraseña incorrecta")

            ### Si es 404, usuario no existe
            elif solicitudlogin.status_code == 404:
                messagebox.showerror(title="Error",message=f"No existe el usuario {usuario}.")
                print("No existe el usuario")
            else:
                ##! Si... eh?    Que mierda es esto?
                messagebox.showerror(title="Error",message=f"Error imposible {solicitudlogin.status_code} === {solicitudlogin.text}")
                print(f"Error imposible {solicitudlogin.status_code} === {solicitudlogin.text}")

        ### Si hay un error de conexion muestra un mensaje de error
        except requests.exceptions.RequestException as rr:
            messagebox.showerror(title="Error",message=f"No hay conexion con el servidor! === {rr}")
            print(f"No hay conexion con el servidor === {rr}")

##! Bugfix
### Funcion para abrir el login
def abrir_login():
    print("abriendo login")
    cerrar_register()
    loginscreen(abrir_registro,comprobar_login)
### Funcion para abrir el registro
def abrir_registro():
    print("abriendo registro")
    cerrar_login()
    registerscreen(comprobardatos,abrir_login)

### Main
if __name__ == "__main__":
    loginscreen(abrir_registro,comprobar_login)