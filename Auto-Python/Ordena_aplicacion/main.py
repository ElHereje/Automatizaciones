import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from organizador import GestorArchivos, CATEGORIAS_EXTENSIONES


class AplicacionOrganizador:
    """Interfaz gráfica en Tkinter bajo Programación Orientada a Objetos."""

    def __init__(self, root):
        self.root = root
        self.root.title("Organizador Automático de Archivos")
        self.root.geometry("680x560")
        self.root.minsize(620, 520)

        # Variables de control
        self.ruta_var = tk.StringVar()
        self.vars_categorias = {}
        self.checkbuttons = []

        # Instancia del gestor lógico pasando el método de log de la UI
        self.gestor = GestorArchivos(callback_log=self.agregar_log)

        self._construir_interfaz()

        # Gestionar el cierre de la ventana con la "X"
        self.root.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def _construir_interfaz(self):
        """Crea y organiza todos los widgets de la ventana."""
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        marco_principal = ttk.Frame(self.root, padding="15")
        marco_principal.pack(fill=tk.BOTH, expand=True)

        # --- SECCIÓN 1: Selección de Carpeta ---
        marco_ruta = ttk.LabelFrame(marco_principal, text=" 1. Carpeta a vigilar y ordenar ", padding="10")
        marco_ruta.pack(fill=tk.X, pady=(0, 10))

        self.entry_ruta = ttk.Entry(marco_ruta, textvariable=self.ruta_var, state="readonly")
        self.entry_ruta.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.btn_buscar = ttk.Button(marco_ruta, text="Buscar carpeta...", command=self.seleccionar_carpeta)
        self.btn_buscar.pack(side=tk.RIGHT)

        # --- SECCIÓN 2: Checkboxes de Extensiones ---
        marco_ext = ttk.LabelFrame(marco_principal, text=" 2. Tipos de archivo a organizar ", padding="10")
        marco_ext.pack(fill=tk.X, pady=(0, 10))

        # Botones auxiliares para marcar/desmarcar todo
        marco_sel_rapida = ttk.Frame(marco_ext)
        marco_sel_rapida.pack(fill=tk.X, pady=(0, 8))

        self.btn_marcar_todo = ttk.Button(marco_sel_rapida, text="Seleccionar todo", command=lambda: self.cambiar_todos_checks(True))
        self.btn_marcar_todo.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_desmarcar_todo = ttk.Button(marco_sel_rapida, text="Deseleccionar todo", command=lambda: self.cambiar_todos_checks(False))
        self.btn_desmarcar_todo.pack(side=tk.LEFT)

        # Cuadrícula de Checkboxes
        marco_grid_checks = ttk.Frame(marco_ext)
        marco_grid_checks.pack(fill=tk.X)

        columnas = 2
        for idx, (categoria, extensiones) in enumerate(CATEGORIAS_EXTENSIONES.items()):
            var = tk.BooleanVar(value=True)
            self.vars_categorias[categoria] = var

            # Mostramos el nombre de la categoría y un resumen de sus extensiones
            resumen_ext = ", ".join(extensiones[:4]) + ("..." if len(extensiones) > 4 else "")
            texto_check = f"{categoria} ({resumen_ext})"

            chk = ttk.Checkbutton(marco_grid_checks, text=texto_check, variable=var)
            fila = idx // columnas
            col = idx % columnas
            chk.grid(row=fila, column=col, sticky="w", padx=10, pady=4)
            self.checkbuttons.append(chk)

        # --- SECCIÓN 3: Controles de Inicio y Fin ---
        marco_controles = ttk.Frame(marco_principal)
        marco_controles.pack(fill=tk.X, pady=(0, 10))

        self.btn_iniciar = ttk.Button(marco_controles, text="▶ Iniciar Vigilancia", command=self.iniciar_proceso)
        self.btn_iniciar.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.btn_finalizar = ttk.Button(marco_controles, text="■ Finalizar Vigilancia", command=self.detener_proceso, state="disabled")
        self.btn_finalizar.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))

        # --- SECCIÓN 4: Registro de actividad (Log en tiempo real) ---
        marco_log = ttk.LabelFrame(marco_principal, text=" Registro de actividad ", padding="10")
        marco_log.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(marco_log)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.texto_log = tk.Text(marco_log, height=8, state="disabled", yscrollcommand=scrollbar.set, font=("Consolas", 9))
        self.texto_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.texto_log.yview)

        # Barra de estado inferior
        self.estado_var = tk.StringVar(value="Estado: Detenido. Selecciona una carpeta y las extensiones.")
        lbl_estado = ttk.Label(self.root, textvariable=self.estado_var, relief=tk.SUNKEN, anchor="w", padding=(10, 3))
        lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccione la carpeta a ordenar")
        if carpeta:
            self.ruta_var.set(carpeta)
            self.agregar_log(f"Carpeta seleccionada: {carpeta}")

    def cambiar_todos_checks(self, estado):
        for var in self.vars_categorias.values():
            var.set(estado)

    def alternar_estado_controles(self, ejecutando):
        """Bloquea los ajustes mientras el observador está activo."""
        estado_config = "disabled" if ejecutando else "normal"
        self.btn_buscar.config(state=estado_config)
        self.btn_marcar_todo.config(state=estado_config)
        self.btn_desmarcar_todo.config(state=estado_config)

        for chk in self.checkbuttons:
            chk.config(state=estado_config)

        self.btn_iniciar.config(state="disabled" if ejecutando else "normal")
        self.btn_finalizar.config(state="normal" if ejecutando else "disabled")

    def iniciar_proceso(self):
        ruta = self.ruta_var.get()
        if not ruta or not os.path.isdir(ruta):
            messagebox.showwarning("Ruta inválida", "Por favor, selecciona una carpeta válida antes de iniciar.")
            return

        seleccionadas = [cat for cat, var in self.vars_categorias.items() if var.get()]
        if not seleccionadas:
            messagebox.showwarning("Sin selección", "Debes marcar al menos un tipo de archivo para ordenar.")
            return

        self.gestor.configurar(ruta, seleccionadas)
        self.alternar_estado_controles(ejecutando=True)
        self.estado_var.set(f"Estado: Vigilando '{os.path.basename(ruta)}'...")
        self.gestor.iniciar_vigilancia()

    def detener_proceso(self):
        self.gestor.detener_vigilancia()
        self.alternar_estado_controles(ejecutando=False)
        self.estado_var.set("Estado: Detenido.")

    def agregar_log(self, mensaje):
        """Inserta mensajes de forma segura en el cuadro de texto desde cualquier hilo."""
        def _insertar():
            self.texto_log.config(state="normal")
            self.texto_log.insert(tk.END, mensaje + "\n")
            self.texto_log.see(tk.END)
            self.texto_log.config(state="disabled")

        self.root.after(0, _insertar)

    def al_cerrar(self):
        """Asegura detener el hilo de watchdog antes de cerrar la ventana."""
        if self.gestor.vigilando:
            self.gestor.detener_vigilancia()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionOrganizador(root)
    root.mainloop()
