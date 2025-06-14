import tkinter as tk
from tkinter import ttk

def cerrar_home_notepad():
    ventana.destroy()

# === CONFIGURACIÓN INICIAL ===
def notepad_home(usuario):
    global ventana
    ventana = tk.Tk()
    ventana.title("Mis LoginNotes")
    ventana.geometry("600x400")
    ventana.configure(bg="#e0e0e0")

    title = tk.Label(ventana,text="Mis LoginNotes",font="Arial 20 bold",bg="#e0e0e0")
    title.place(anchor="center",rely=0.06,relx=0.5)

    max_columns = 3  # Cuántos servidores por fila
    notas = []

    # === CONTENEDOR PRINCIPAL CENTRADO ===
    container = ttk.Frame(ventana)
    container.place(relx=0.5, rely=0.5, anchor="center")

    # === CAJA VISUAL CON BORDE ===
    box_frame = ttk.Frame(container, padding=20, relief="solid", borderwidth=2)
    box_frame.pack()

    # === FRAME CON SCROLL ===
    canvas = tk.Canvas(box_frame, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(box_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", on_configure)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === FUNCIÓN PARA AGREGAR SERVIDORES ===
    def agregar_notas(nombre=None):
        index = len(notas)
        row = index // max_columns
        col = index % max_columns
        nombre = nombre or f"Nota {index + 1}"

        def abrir_registro():
            print(f"simbio {index +1}")
        frame = ttk.Frame(scrollable_frame, padding=10, relief="ridge", borderwidth=2,cursor="hand2")
        label = ttk.Label(frame, text=nombre,cursor="hand2")
        label.pack(padx=10, pady=10)
        frame.bind("<Button-1>", lambda e: abrir_registro())
        label.bind("<Button-1>", lambda e: abrir_registro())
        frame.grid(row=row, column=col, padx=10, pady=10)
        notas.append(frame)

    # === BOTÓN PARA AGREGAR SERVIDORES ===
    btn_add = ttk.Button(ventana, text="Agregar LoginNotes", command=agregar_notas)
    btn_add.place(relx=0.5, rely=0.95, anchor="s")

    # Agrega algunos servidores iniciales (opcional)
    for _ in range(4):
        agregar_notas()


# === INICIAR LOOP DE LA APP ===
    ventana.mainloop()

if __name__ == "__main__":
    notepad_home("simbio")