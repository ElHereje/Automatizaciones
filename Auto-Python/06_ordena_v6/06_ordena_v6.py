'''
Creamos ejecutable, por lo que hay que hacer modificaciones.
Esto obliga a crear una pequeña intreface gráfica, con un botón que
detenga la ejecución. 
Esto lo hacemos sustituyendo nuestro While True por una ventana
emergente con botón de finalizar
'''

import shutil
import os
import getpass
import time
import threading

from tkinter import Tk, filedialog, Button, Label
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

# para evitar el error de permisos

def esperar_archivo_libre(ruta_archivo, intentos=10, espera=0.5):
    
    #no interesa nº de bucle, solo repetir por eso ->  "_"
    for _ in range(intentos):
        try:
            with open(ruta_archivo, "rb"): # si entra, es que el archivo está libre
                return True
        except (PermissionError, OSError):
            time.sleep(espera)    
            
    return False # si sigue ocupado, acaba y deja ese archivo


# movemos los archivos por tipo dentro de una función
def ordenar_archivos(ruta):
    for archivo in os.listdir(ruta):
        ruta_archivo = os.path.join(ruta, archivo)
        
        # excluimos carpetas y el archivo log
        if os.path.isfile(ruta_archivo) and archivo != 'log_mov.txt' :  
            
            # comprobamos 1º si está libre
            if not esperar_archivo_libre(ruta_archivo):
                continue # nos saltamos el archivo
            
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


# creamos la clase que controla el observados

class ManejadorEventos(FileSystemEventHandler):
    
    def on_created(self, event):
        if not event.is_directory: # no queremos que vigile directorios
            ordenar_archivos(ruta)

#recorremos el diccionario
for carpeta in set(extensiones.values()):
    ruta_carpeta=os.path.join(ruta, carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        
ordenar_archivos(ruta)
        
# creamos una instancia del observer

manejador_evento = ManejadorEventos()
observador = Observer()
observador.schedule(manejador_evento, ruta, recursive=False) # false para que no controle subcarpetas


def iniciar_vigilancia():
    observador.start()
    
def detener_vigilancia():
    observador.stop()
    observador.join()
    ventana.quit()
    
# creamos el entorno gráfico

ventana.deiconify()
ventana.title("Vigilancia de carpeta")
ventana.geometry("400x150")

Label(ventana, text=f"Vigilando la capeta: \n{ruta}", wraplength=350).pack(pady=10)
Button(ventana, text="Detener la vigilancia y salir.", command=detener_vigilancia).pack(pady=10)

hilo_vigilancia=threading.Thread(target=iniciar_vigilancia, daemon=True)
hilo_vigilancia.start()

ventana.mainloop()

# PARA CREAR EL EJECUTABLE --> pyinstaller --noconsole --onefile 06_ordena_v6.py
