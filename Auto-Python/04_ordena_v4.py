'''
Agregamos subcarpetas
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
    '.xls':'Excel',
    '.xlsx':'Excel',
    '.rar':'Compress',
    '.zip':'Compress',
    '.exe':'Ejecutables'
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
            
            # obteniendo la fecha de última modific.
            
            fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
            subcarpeta_fecha = fecha_mod.strftime("%Y-%m-%d") 
                       
            # creamos la subcarpeta
            
            carpeta_tipo = os.path.join(ruta, extensiones[ext])
            carpeta_fecha = os.path.join(carpeta_tipo, subcarpeta_fecha)
            
            if not os.path.exists(carpeta_fecha):
                os.makedirs(carpeta_fecha)
            
            # Ruta destino final
            
            destino = os.path.join(carpeta_fecha, archivo)
            
            shutil.move(ruta_archivo, destino)
            
            # REGISTRAMOS EN EL LOG
            
            with open(os.path.join(ruta, 'log_mov.txt'), "a", encoding="utf-8") as log:
                log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Usuario: {usuario} - Movido: {archivo} -> {destino}\n")