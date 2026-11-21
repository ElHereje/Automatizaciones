'''
Incorporamos ventana TKinter para elegir carpeta,
prescindimos de los elif
usamos dicc. para asociar extensiones con carpetas
'''


import shutil
import os
from tkinter import Tk, filedialog

# ruta de los archivos a ordenar

ventana = Tk()
ventana.withdraw() #eliminamos la ventana adcional de command

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