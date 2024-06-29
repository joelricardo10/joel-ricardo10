import tkinter as tk
from tkinter import Toplevel
import subprocess

def abrir_ventana(numero):
    if numero == 1:
        subprocess.Popen(['python', 'Calculadora.py'])
    elif numero == 2:
        subprocess.Popen(['python', 'LogViewer.py'])
    elif numero == 3:
        subprocess.Popen(['python', 'API_AbuseIP.py'])
    #paso 3    
    elif numero == 4:
        subprocess.Popen(['python', 'AnalisisPC.py'])
    else:
        ventana_nueva = Toplevel()
        ventana_nueva.title(f"Ventana {numero}")
        ventana_nueva.geometry("400x400")
        etiqueta = tk.Label(ventana_nueva, text=f"Esta es la ventana {numero}")
        etiqueta.pack(padx=20, pady=20)

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Ventanas con Tkinter")
ventana_principal.geometry("1200x1200")

# Cargar la imagen de fondo
background_image = tk.PhotoImage(file="interfaz.png")
background_label = tk.Label(ventana_principal, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Configurar el grid de la ventana principal
ventana_principal.columnconfigure([0, 1], weight=1)
ventana_principal.rowconfigure([0, 1], weight=1)

# Crear y colocar botones
boton1 = tk.Button(ventana_principal, text="Ventana 1", command=lambda: abrir_ventana(1), bg="green", fg="white", font=("Helvetica", 14), height=2, width=12)
boton1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

boton2 = tk.Button(ventana_principal, text="Ventana 2", command=lambda: abrir_ventana(2), bg="green", fg="white", font=("Helvetica", 14), height=2, width=12)
boton2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

boton3 = tk.Button(ventana_principal, text="Ventana 3", command=lambda: abrir_ventana(3), bg="green", fg="white", font=("Helvetica", 14), height=2, width=12)
boton3.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

boton4 = tk.Button(ventana_principal, text="Ventana 4", command=lambda: abrir_ventana(4), bg="green", fg="white", font=("Helvetica", 14), height=2, width=12)
boton4.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

# Ejecutar el bucle principal de Tkinter
ventana_principal.mainloop()

