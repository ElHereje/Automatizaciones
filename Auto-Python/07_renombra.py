import os

# creamos las variables necesarias
carpeta = 'C:/Users/imad/Downloads/pruebas'
prefijo = 'imagen_'
extensiones = ('.jpg', '.png', 'gif', '.bmp')

#guardamos en una lista los archivos necesarios
archivos = []
for archivo in os.listdir(carpeta):
    if archivo.endswith(extensiones):
        archivos.append(archivo)
        
#enumeramos y renombramos los archivos
for i, nombre_actual in enumerate(archivos, start=1):
    
    #separamos el nombre de la extensión (nombre.extension = 0.1)
    extension_actual = os.path.splitext(nombre_actual)[1]
    
    nuevo_nombre = f"{prefijo}{i:03}{extension_actual}"
    ruta_actual = os.path(carpeta, nombre_actual)
    ruta_nueva = os.path(carpeta, nuevo_nombre)
    os.rename(ruta_actual, ruta_nueva)