import os
import shutil
import getpass
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Diccionario por defecto agrupado por categorías y extensiones típicas
CATEGORIAS_EXTENSIONES = {
    "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff"],
    "Documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
    "Hojas de Cálculo": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentaciones": [".ppt", ".pptx", ".odp"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Audio": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"],
    "Vídeo": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"],
    "Ejecutables": [".exe", ".msi", ".bat", ".sh", ".apk", ".dmg"],
    "Código y Datos": [".py", ".js", ".html", ".css", ".json", ".xml", ".sql", ".java", ".cpp"]
}


class ManejadorEventos(FileSystemEventHandler):
    """Manejador de eventos del sistema de archivos para watchdog."""

    def __init__(self, gestor):
        super().__init__()
        self.gestor = gestor

    def on_created(self, event):
        if not event.is_directory:
            self.gestor.ordenar_archivos()

    def on_moved(self, event):
        # Útil cuando los navegadores terminan una descarga y renombran el archivo temporal (.crdownload / .part)
        if not event.is_directory:
            self.gestor.ordenar_archivos()


class GestorArchivos:
    """Clase encargada de la lógica de clasificación, movimiento y vigilancia de archivos."""

    def __init__(self, callback_log=None):
        self.usuario = getpass.getuser()
        self.ruta = ""
        self.extensiones_activas = {}
        self.observador = None
        self.vigilando = False
        self.callback_log = callback_log

    def _registrar_mensaje(self, mensaje):
        """Envía mensajes a la interfaz gráfica si hay un callback configurado."""
        if self.callback_log:
            self.callback_log(mensaje)

    def configurar(self, ruta, categorias_seleccionadas):
        """Configura la ruta objetivo y construye el mapa de extensiones activas."""
        self.ruta = ruta
        self.extensiones_activas.clear()

        for categoria in categorias_seleccionadas:
            if categoria in CATEGORIAS_EXTENSIONES:
                for ext in CATEGORIAS_EXTENSIONES[categoria]:
                    self.extensiones_activas[ext.lower()] = categoria

    def esperar_archivo_libre(self, ruta_archivo, intentos=10, espera=0.5):
        """Comprueba si el archivo ha terminado de escribirse y no está bloqueado."""
        for _ in range(intentos):
            try:
                if not os.path.exists(ruta_archivo):
                    return False
                with open(ruta_archivo, "rb"):
                    return True
            except (PermissionError, OSError):
                time.sleep(espera)
        return False

    def _obtener_destino_unico(self, carpeta_destino, nombre_archivo):
        """Evita sobrescribir archivos si ya existe uno con el mismo nombre en destino."""
        destino = os.path.join(carpeta_destino, nombre_archivo)
        if not os.path.exists(destino):
            return destino

        nombre, ext = os.path.splitext(nombre_archivo)
        contador = 1
        while True:
            nuevo_nombre = f"{nombre}_{contador}{ext}"
            nuevo_destino = os.path.join(carpeta_destino, nuevo_nombre)
            if not os.path.exists(nuevo_destino):
                return nuevo_destino
            contador += 1

    def ordenar_archivos(self):
        """Recorre la carpeta raíz y mueve los archivos según su extensión y fecha."""
        if not self.ruta or not os.path.isdir(self.ruta):
            return

        try:
            archivos = os.listdir(self.ruta)
        except OSError as e:
            self._registrar_mensaje(f"Error al leer directorio: {e}")
            return

        for archivo in archivos:
            ruta_archivo = os.path.join(self.ruta, archivo)

            # Ignorar directorios, el archivo de log y descargas temporales incompletas
            if not os.path.isfile(ruta_archivo) or archivo == "log_mov.txt":
                continue

            _, ext = os.path.splitext(archivo)
            ext = ext.lower()

            if ext in self.extensiones_activas:
                if not self.esperar_archivo_libre(ruta_archivo):
                    continue

                try:
                    fecha_mod = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
                    subcarpeta_fecha = fecha_mod.strftime("%Y-%m-%d")

                    carpeta_tipo = os.path.join(self.ruta, self.extensiones_activas[ext])
                    carpeta_fecha = os.path.join(carpeta_tipo, subcarpeta_fecha)

                    os.makedirs(carpeta_fecha, exist_ok=True)

                    destino = self._obtener_destino_unico(carpeta_fecha, archivo)
                    shutil.move(ruta_archivo, destino)

                    # Guardar registro en archivo de texto
                    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    linea_log = f"{marca_tiempo} - Usuario: {self.usuario} - Movido: {archivo} -> {destino}"

                    with open(os.path.join(self.ruta, "log_mov.txt"), "a", encoding="utf-8") as log:
                        log.write(linea_log + "\n")

                    self._registrar_mensaje(f"[{datetime.now().strftime('%H:%M:%S')}] Movido: {archivo} -> {self.extensiones_activas[ext]}/{subcarpeta_fecha}/")

                except Exception as e:
                    self._registrar_mensaje(f"Error moviendo {archivo}: {e}")

    def iniciar_vigilancia(self):
        """Realiza una limpieza inicial y arranca el observador en segundo plano."""
        if self.vigilando:
            return

        # Ordenamiento inicial de los archivos existentes
        self.ordenar_archivos()

        manejador = ManejadorEventos(self)
        self.observador = Observer()
        self.observador.schedule(manejador, self.ruta, recursive=False)
        self.observador.start()
        self.vigilando = True
        self._registrar_mensaje(f"Vigilancia iniciada en: {self.ruta}")

    def detener_vigilancia(self):
        """Detiene de forma segura el hilo del observador."""
        if self.vigilando and self.observador:
            self.observador.stop()
            self.observador.join()
            self.observador = None
            self.vigilando = False
            self._registrar_mensaje("Vigilancia detenida correctamente.")
