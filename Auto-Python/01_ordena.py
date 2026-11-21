import shutil
import os

# ruta de los archivos a ordenar

ruta = 'C:/Users/imad/Downloads'

# creamos las carpetas

tipos=['Images','PDFs','Compress','DOCs']

for carpeta in tipos:
    ruta_carpeta=os.path.join(ruta, carpeta)
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        
# movemos los archivos por tipo

for archivo in os.listdir(ruta):
    if archivo.endswith('.jpg') or archivo.endswith('.png'):
        shutil.move(os.path.join(ruta,archivo), os.path.join(ruta,'Images',archivo) )
    elif archivo.endswith('.pdf'):
        shutil.move(os.path.join(ruta,archivo), os.path.join(ruta,'PDFs',archivo) )
    elif archivo.endswith('.doc') or archivo.endswith('.docx'):
            shutil.move(os.path.join(ruta,archivo), os.path.join(ruta,'DOCs',archivo) ) 
    elif archivo.endswith('.zip') or archivo.endswith('.rar'):
            shutil.move(os.path.join(ruta,archivo), os.path.join(ruta,'Compress',archivo) )      
            
'''
Como práctica adicional, se puede crear entorno en TKinter
'''
     