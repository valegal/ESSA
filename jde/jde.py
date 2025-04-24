import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
import threading
from pathlib import Path
from datetime import datetime
import logging
from config import config
from main import main as ejecutar_proceso_completo
from main_detallado import main_detallado as ejecutar_proceso_detallado

class JDEGUI:
    def __init__(self, root):
        self.root = root
        self.running_process = False
        self.process_thread = None
        self.setup_ui()
        self.setup_logging()
        
    def setup_ui(self):
        """Configura la interfaz gráfica completa"""
        self.root.title("Automación JDE - Interfaz Facturación")
        self.root.geometry("1500x800")
        self.root.configure(bg="white")
        self.center_window()
        
        try:
            self.root.iconbitmap(str(config.BASE_DIR / "resources" / "logo.ico"))
        except Exception as e:
            logging.warning(f"No se pudo cargar el icono: {str(e)}")

        self.setup_styles()
        self.create_main_frames()
        self.setup_execution_panel()
        self.setup_config_panel()
        self.show_completo_view()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_styles(self):
        """Configura los estilos visuales simplificados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilos generales con fondo blanco
        style.configure(".", background="white")
        style.configure("TLabel", background="white", foreground="black", font=("Arial", 11))
        style.configure("Title.TLabel", font=("Arial", 14, "bold"), background="white")
        style.configure("TButton", padding=6, font=("Arial", 11))
        style.configure("Accent.TButton", background="#0078D7", foreground="white")
        style.configure("TEntry", font=("Arial", 11))
        style.configure("TCombobox", font=("Arial", 11))
        
        # Estilo para botones deshabilitados
        style.map("Accent.TButton",
                background=[('active', '#005A9E'), ('disabled', '#E1E1E1')],
                foreground=[('disabled', '#7F7F7F')])

    def create_main_frames(self):
        """Crea los marcos principales de la interfaz"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo (ejecución - 60% del ancho)
        self.exec_frame = ttk.Frame(self.main_frame, width=600)
        self.exec_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Separador vertical
        ttk.Separator(self.main_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Frame derecho (configuración - 40% del ancho)
        self.config_frame = ttk.Frame(self.main_frame, width=400)
        self.config_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    def setup_execution_panel(self):
        """Configura el panel de ejecución"""
        # Selector de modo
        modo_frame = ttk.Frame(self.exec_frame)
        modo_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(modo_frame, text="Modo de ejecución:").pack(side=tk.LEFT, padx=5)
        self.modo_var = tk.StringVar(value="Completo")
        modo_combo = ttk.Combobox(modo_frame, textvariable=self.modo_var, 
                                values=["Completo", "Detallado"], state="readonly", width=15)
        modo_combo.pack(side=tk.LEFT)
        modo_combo.bind("<<ComboboxSelected>>", lambda e: self.toggle_mode())

        # Separador
        ttk.Separator(self.exec_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Vista completa
        self.completo_frame = ttk.Frame(self.exec_frame)
        self.setup_completo_view()

        # Vista detallada
        self.detallado_frame = ttk.Frame(self.exec_frame)
        self.setup_detallado_view()

        # Área de logs
        self.setup_log_panel()

        # Botón de detener
        self.setup_stop_button()

    def setup_completo_view(self):
        """Configura la vista de ejecución completa"""
        ttk.Label(self.completo_frame, text="Ejecución Completa", 
                 style="Title.TLabel").pack(pady=10)
        
        # Fecha contable
        fecha_frame = ttk.Frame(self.completo_frame)
        fecha_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fecha_frame, text="Fecha Contable:").pack(side=tk.LEFT, padx=5)
        self.fecha_completo = DateEntry(fecha_frame, date_pattern="dd/mm/yyyy", font=("Arial", 11))
        self.fecha_completo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Botón de ejecución
        btn_frame = ttk.Frame(self.completo_frame)
        btn_frame.pack(pady=20)
        
        self.ejecutar_completo_btn = ttk.Button(btn_frame, text="EJECUTAR PROCESO COMPLETO", 
                                              style="Accent.TButton", 
                                              command=self.ejecutar_completo)
        self.ejecutar_completo_btn.pack(ipadx=20, ipady=5)

    def setup_detallado_view(self):
        """Configura la vista de ejecución detallada"""
        ttk.Label(self.detallado_frame, text="Ejecución por Fase", 
                 style="Title.TLabel").pack(pady=10)
        
        # Fecha contable
        fecha_frame = ttk.Frame(self.detallado_frame)
        fecha_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fecha_frame, text="Fecha Contable:").pack(side=tk.LEFT, padx=5)
        self.fecha_detallado = DateEntry(fecha_frame, date_pattern="dd/mm/yyyy", font=("Arial", 11))
        self.fecha_detallado.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Selección de fase
        fase_frame = ttk.Frame(self.detallado_frame)
        fase_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fase_frame, text="Fase:").pack(side=tk.LEFT, padx=5)
        self.fase_var = tk.StringVar(value="1")
        fase_combo = ttk.Combobox(fase_frame, textvariable=self.fase_var, 
                                values=["1", "2", "3", "4", "5"], state="readonly", width=5)
        fase_combo.pack(side=tk.LEFT)
        
        # Botón de ejecución
        btn_frame = ttk.Frame(self.detallado_frame)
        btn_frame.pack(pady=20)
        
        self.ejecutar_detallado_btn = ttk.Button(btn_frame, text="EJECUTAR FASE SELECCIONADA", 
                                               style="Accent.TButton", 
                                               command=self.ejecutar_detallado)
        self.ejecutar_detallado_btn.pack(ipadx=20, ipady=5)

    def setup_log_panel(self):
        """Configura el panel de registro de actividad"""
        log_frame = ttk.LabelFrame(self.exec_frame, text="Registro de Actividad", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=80, height=15, 
                                                font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.configure(state=tk.DISABLED)

    def setup_stop_button(self):
        """Configura el botón de detener proceso"""
        self.stop_btn = ttk.Button(self.exec_frame, text="DETENER PROCESO", 
                                 style="Accent.TButton", command=self.stop_process)
        self.stop_btn.pack(pady=5)
        self.stop_btn.config(state=tk.DISABLED)

    def setup_config_panel(self):
        """Configura el panel de configuración con scroll"""
        ttk.Label(self.config_frame, text="Configuración", style="Title.TLabel").pack(pady=10)
        
        # Panel con scroll
        canvas = tk.Canvas(self.config_frame, highlightthickness=0, bg="white")
        scrollbar = ttk.Scrollbar(self.config_frame, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scroll_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set, bg="white")
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configuraciones editables para todos los campos de config.py
        self.config_entries = {}
        config_fields = [
            ("CHROMEDRIVER_PATH", "Ruta Chromedriver:", config.CHROMEDRIVER_PATH),
            ("WEBSITE_URL_JDE", "URL JDE:", config.WEBSITE_URL_JDE),
            ("EXCEL_PATH", "Ruta Excel:", config.EXCEL_PATH),
            ("RUTA_RES_CARGA", "Ruta resultado carga:", config.RUTA_RES_CARGA),
            ("USER", "Usuario:", config.USER),
            ("PASS", "Contraseña:", config.PASS),  # Este será especial
            ("FOLDER_R5609FCT", "Carpeta R5609FCT:", config.FOLDER_R5609FCT),
            ("FOLDER_DINAMICAS", "Carpeta Reportes Dinámicos:", config.FOLDER_DINAMICAS),
            ("FOLDER_ORIGEN", "Carpeta Origen PDFs:", config.FOLDER_ORIGEN),
        ]
        
        # Usar grid para mejor organización
        for row, (key, label, value) in enumerate(config_fields):
            # Etiqueta
            lbl = ttk.Label(scroll_frame, text=label)
            lbl.grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
            
            # Campo de entrada especial para contraseña
            if key == "PASS":
                pass_frame = ttk.Frame(scroll_frame)
                pass_frame.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=3)
                
                entry = ttk.Entry(pass_frame, show="*")
                entry.insert(0, str(value))
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Botón para mostrar/ocultar contraseña
                eye_btn = ttk.Button(pass_frame, text="👁", width=3,
                                   command=lambda e=entry: self.toggle_password_visibility(e))
                eye_btn.pack(side=tk.RIGHT)
            else:
                # Campos normales
                entry = ttk.Entry(scroll_frame)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=3)
            
            self.config_entries[key] = entry
        
        # Configurar peso de columnas para que se expandan
        scroll_frame.columnconfigure(1, weight=1)
        
        # Botón guardar configuración DENTRO del scroll_frame, después de todos los inputs
        save_frame = ttk.Frame(scroll_frame)
        save_frame.grid(row=len(config_fields)+1, column=0, columnspan=2, sticky=tk.EW, pady=(20, 10))
        
        # Definir estilo para el botón de guardar (verde)
        style = ttk.Style()
        style.configure("Save.TButton", background="white", foreground="blue", font=("Arial", 11, "bold"))
        style.map("Save.TButton",
                background=[('active', '#d4e9ff'), ('disabled', '#cccccc')],
                foreground=[('disabled', '#888888')])
        
        save_btn = ttk.Button(save_frame, text="GUARDAR CONFIGURACIÓN", 
                            style="Save.TButton", command=self.save_config)
        save_btn.pack(ipadx=20, ipady=5)
        
    def toggle_password_visibility(self, entry):
        """Alterna entre mostrar y ocultar la contraseña"""
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')

    def setup_logging(self):
        """Configura el sistema de logging"""
        self.log_handler = TextHandler(self.log_text)
        self.log_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(self.log_handler)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_mode(self):
        """Alterna entre vistas completa y detallada"""
        if self.modo_var.get() == "Completo":
            self.detallado_frame.pack_forget()
            self.completo_frame.pack(fill=tk.BOTH, expand=True)
        else:
            self.completo_frame.pack_forget()
            self.detallado_frame.pack(fill=tk.BOTH, expand=True)

    def show_completo_view(self):
        """Muestra la vista de ejecución completa"""
        self.completo_frame.pack(fill=tk.BOTH, expand=True)
        self.detallado_frame.pack_forget()

    def save_config(self):
        """Guarda la configuración desde la interfaz"""
        try:
            ui_settings = {key: entry.get() for key, entry in self.config_entries.items()}
            config.update_from_ui(ui_settings)
            messagebox.showinfo("Configuración", "Configuración guardada exitosamente")
            logging.info("Configuración actualizada desde la interfaz")
        except Exception as e:
            logging.error(f"Error al guardar configuración: {str(e)}")
            messagebox.showerror("Error", f"No se pudo guardar la configuración: {str(e)}")

    def toggle_buttons_state(self, running):
        """Habilita/deshabilita botones durante la ejecución"""
        state = tk.DISABLED if running else tk.NORMAL
        self.ejecutar_completo_btn.config(state=state)
        self.ejecutar_detallado_btn.config(state=state)
        self.stop_btn.config(state=tk.NORMAL if running else tk.DISABLED)
        self.running_process = running

    def ejecutar_completo(self):
        """Ejecuta el proceso completo en un hilo separado"""
        if self.running_process:
            messagebox.showwarning("Proceso en ejecución", "Ya hay un proceso en ejecución")
            return
            
        fecha = self.fecha_completo.get_date()
        
        if not fecha:
            messagebox.showerror("Error", "Debe seleccionar una fecha válida")
            return
            
        self.toggle_buttons_state(True)
        
        self.process_thread = threading.Thread(
            target=self._run_completo, 
            args=(fecha,),
            daemon=True
        )
        self.process_thread.start()

    def _run_completo(self, fecha):
        """Función interna para ejecutar el proceso completo"""
        try:
            logging.info("Iniciando proceso completo...")
            success = ejecutar_proceso_completo(fecha)
            
            if success:
                logging.info("Proceso completado exitosamente")
                messagebox.showinfo("Éxito", "Proceso completado correctamente")
            else:
                logging.error("El proceso completo encontró errores")
                messagebox.showerror("Error", "Ocurrieron errores durante el proceso")
                
        except Exception as e:
            logging.error(f"Error en ejecución completa: {str(e)}")
            messagebox.showerror("Error", f"Error durante la ejecución: {str(e)}")
        finally:
            self.toggle_buttons_state(False)
            self.process_thread = None

    def ejecutar_detallado(self):
        """Ejecuta una fase específica en un hilo separado"""
        if self.running_process:
            messagebox.showwarning("Proceso en ejecución", "Ya hay un proceso en ejecución")
            return
            
        fecha = self.fecha_detallado.get_date()
        fase = self.fase_var.get()  # Esto ya es un string
        
        if not fecha:
            messagebox.showerror("Error", "Debe seleccionar una fecha válida")
            return
            
        # Convertir fase a formato de dos dígitos
        fase = f"{int(fase):02d}"  # Esto convierte "1" en "01", "2" en "02", etc.
        
        self.toggle_buttons_state(True)
        
        self.process_thread = threading.Thread(
            target=self._run_detallado,
            args=(fecha, fase),  # Ahora pasamos el string ya formateado
            daemon=True
        )
        self.process_thread.start()

    def _run_detallado(self, fecha, fase):
        """Función interna para ejecutar proceso detallado"""
        try:
            logging.info(f"Iniciando fase {fase}...")
            success = ejecutar_proceso_detallado(fecha, fase)  # Pasa el string formateado
            
            if success:
                logging.info(f"Fase {fase} completada exitosamente")
                messagebox.showinfo("Éxito", f"Fase {fase} completada correctamente")
            else:
                logging.error(f"La fase {fase} encontró errores")
                messagebox.showerror("Error", f"Ocurrieron errores en la fase {fase}")
                
        except Exception as e:
            logging.error(f"Error en fase {fase}: {str(e)}")
            messagebox.showerror("Error", f"Error durante la fase {fase}: {str(e)}")
        finally:
            self.toggle_buttons_state(False)
            self.process_thread = None
            
    def stop_process(self):
        """Detiene el proceso en ejecución"""
        if self.running_process:
            if messagebox.askyesno("Confirmar", "¿Está seguro de detener el proceso actual?"):
                logging.warning("Proceso detenido por el usuario")
                self.toggle_buttons_state(False)
                self.process_thread = None

    def on_close(self):
        """Maneja el evento de cierre de la ventana"""
        if self.running_process:
            if messagebox.askokcancel("Salir", "Hay un proceso en ejecución. ¿Desea detenerlo y salir?"):
                self.stop_process()
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

class TextHandler(logging.Handler):
    """Manejador de logs para mostrar en el ScrolledText"""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
    
    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + "\n")
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.see(tk.END)
        self.text_widget.update()

if __name__ == "__main__":
    # Configuración inicial del logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[]
    )
    
    root = tk.Tk()
    app = JDEGUI(root)
    app.run()