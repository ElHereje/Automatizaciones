'''
Creamos interface gráfica
'''
import os

import tkinter as tk
from tkinter import filedialog, messagebox


def seleccionar_carpeta():
    ruta = filedialog.askdirectory()
    entrada_carpeta.insert(0, ruta)
    
def renombrar():
    # creamos las variables necesarias
    carpeta = entrada_carpeta.get()
    prefijo = entrada_prefijo.get()
    extensiones = tuple(entrada_extensiones.get().split(","))
    
    #guardamos en una lista los archivos necesarios
    archivos = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith(extensiones):
            archivos.append(archivo)
            

    # creamos el .bat para revertir el proceso
    ruta_deshacer = os.path.join(carpeta, 'revertir.bat')

    with open(ruta_deshacer, 'w', encoding='utf-8') as deshacer_mem:

        #enumeramos y renombramos los archivos
        for i, nombre_actual in enumerate(archivos, start=1):
            
            #separamos el nombre de la extensión (nombre.extension = 0.1)
            extension_actual = os.path.splitext(nombre_actual)[1]
            
            nuevo_nombre = f"{prefijo}{i:03}{extension_actual}"
            ruta_actual = os.path(carpeta, nombre_actual)
            ruta_nueva = os.path(carpeta, nuevo_nombre)
            os.rename(ruta_actual, ruta_nueva)
            
            #escribimos el bat
            deshacer_mem.write(f'rename "{nuevo_nombre}" "{nombre_actual}"\n')
            
        # eliminamos el .bat cuando se ejecuta
        deshacer_mem.write("del \"%~f0\"\n")
        
    messagebox.showinfo("Éxito", f"Renombrado completo. Para revertir, ejecuta el .bat generado \n")


    

#------------------------Interface grafica---------------------------------


ventana = tk.Tk()
ventana.title("Renombrando arcvhivos...")
ventana.geometry('400x260')
ventana.resizable(False, False)

tk.Label(ventana, text="Carpeta de trabajo:").pack(pady=5)
frame_carpeta = tk.Frame(ventana)
frame_carpeta.pack()
entrada_carpeta = tk.Entry(frame_carpeta, width=40)
entrada_carpeta.pack(side=tk.LEFT, padx=5)
tk.Button(frame_carpeta, text="Examinar", command=seleccionar_carpeta).pack(side=tk.LEFT)

tk.Label(ventana, text="Prefijo de archivos:").pack(pady=5)
entrada_prefijo = tk.Entry(ventana, width=50)
entrada_prefijo.insert(0, "imagen_")
entrada_prefijo.pack()

tk.Label(ventana, text="Extensiones (separadas con coma): ").pack(pady=5)
entrada_extensiones = tk.Entry(ventana, width=50)
entrada_extensiones.insert(0, ".jpg,.png")
entrada_extensiones.pack()

tk.Button(ventana, text="Renombrar", command=renombrar, bg='#04ba04', fg='white', padx=10).pack(pady=15)

ventana.mainloop()