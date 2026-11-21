'''
Clasificamos subcarpetas por fechas
Creamos log con info de movimietno
'''

import shutil
import os
import getpass

from tkinter import Tk, filedialog
from datetime import datetime

# identificamos el usuario logado

usuario = getpass.getuser()

# creamos la ventana de búsqueda

ventana = Tk()
ventana.withdraw() #eliminamos la ventana adcional de command

# ruta de los archivos a ordenar

ruta = filedialog.askdirectory(title="Seleccione la carpeta a ordenar")

# creamos diccionario para asociar carpetas y archivos
extensiones = {
    '.jpg':'Imagenes',
    '.png':'Imagenes',
    '.pdf':'PDFs',
    '.doc':'DOCs',
    '.docx':'DOCs',
    '.rar':'Compress',
    '.zip':'Compress'
}

#recorremos el diccionario
for carpeta in set(extensiones.values()):
    ruta_carpeta=os.path.join(ruta, carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        
# movemos los archivos por tipo
for archivo in os.listdir(ruta):
    ruta_archivo = os.path.join(ruta, archivo)
    
    if os.path.isfile(ruta_archivo):  
        nombre, ext = os.path.splitext(archivo)
        ext = ext.lower()
        
        if ext in extensiones:
            destino = os.path.join(ruta, extensiones[ext], archivo)
            shutil.move(ruta_archivo, destino)
            
            # REGISTRAMOS EN EL LOG
            
            with open(os.path.join(ruta, 'log_mov.txt'), "a", encoding="utf-8") as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario: {usuario} - Movido: {archivo} -> {destino}\n")