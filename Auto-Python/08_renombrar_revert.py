'''
Vamos a revertir el renombrado a través de un .bat
este archivo se creará en la misma carpeta donde se han
renombrado los archivos
'''
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