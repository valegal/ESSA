import tkinter as tk
from tkinter import ttk, scrolledtext
from tkcalendar import DateEntry
import threading
from pathlib import Path

# Simulación de ejecución
def ejecutar_sac_process(fecha):
    print(f"Ejecución Completo: {fecha}")

def ejecutar_sac_detallado(fecha, fase):
    print(f"Ejecución Detallada: {fecha}, fase: {fase}")

def ejecutar_con_cierre(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.start()
    root.after(3000, root.destroy)

# Ventana principal
root = tk.Tk()
root.title("Proceso Interfaz Facturación")
root.geometry("850x500")
root.configure(bg="white")
root.resizable(False, False)

# Centrar pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = (screen_width - 850) // 2
y_coord = (screen_height - 500) // 2
root.geometry(f"850x500+{x_coord}+{y_coord}")

try:
    root.iconbitmap("logo.ico")
except:
    pass

# Estilos mejorados
style = ttk.Style()
style.configure("TLabel", font=("Arial", 11), background="white", foreground="#01085A")
style.configure("ThinSeparator.TFrame", background="#e0e0e0", height=1)
style.configure("TButton", font=("Arial", 11), padding=6)
style.configure("Blue.TButton", background="#264796", foreground="white", font=("Arial", 11, "bold"))
style.map("Blue.TButton", 
          background=[('active', '#17356d'), ('pressed', '#17356d')],
          foreground=[('active', 'white')])
style.configure("TEntry", font=("Arial", 11))
style.configure("Title.TLabel", font=("Arial", 15, "bold"), background="white", foreground="#01085A")
style.configure("Separator.TFrame", background="#e0e0e0")

# Frame principal dividido
main_frame = tk.Frame(root, bg="white")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Frame izquierdo para modos (60% del ancho)
frame_izq = tk.Frame(main_frame, bg="white", width=540)
frame_izq.pack(side="left", fill="both", expand=True)

# Línea separadora vertical
separator = ttk.Separator(main_frame, orient="vertical", style="Separator.TFrame")
separator.pack(side="left", fill="y", padx=5) 

# Frame derecho de configuración (40% del ancho)
frame_config = tk.Frame(main_frame, bg="white", width=300)
frame_config.pack(side="right", fill="both", expand=True)

# Contenedor con scroll para configuración avanzada
config_container = tk.Frame(frame_config, bg="white")
config_container.pack(fill="both", expand=True)

canvas = tk.Canvas(config_container, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(config_container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white", padx=5)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Agregar esto después de crear el canvas y scrollable_frame
scrollable_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units")))
scrollable_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

# Switch entre modos
modo = tk.StringVar(value="Completo")

def cambiar_modo():
    if modo.get() == "Completo":
        frame_detallado.pack_forget()
        frame_completo.pack(fill="both", expand=True, padx=10, pady=10)
    else:
        frame_completo.pack_forget()
        frame_detallado.pack(fill="both", expand=True, padx=10, pady=10)

# Título de configuración avanzada con botón de expandir/contraer
config_header = tk.Frame(frame_config, bg="white")
config_header.pack(fill="x", pady=(0, 5))

ttk.Label(config_header, text="Configuración avanzada", style="Title.TLabel").pack(side="left")

show_advanced = tk.BooleanVar(value=False)
toggle_btn = ttk.Checkbutton(config_header, text="Mostrar", variable=show_advanced, 
                            command=lambda: canvas.pack_forget() if not show_advanced.get() else canvas.pack(side="left", fill="both", expand=True))
toggle_btn.pack(side="right")

# Vista COMPLETO
frame_completo = tk.Frame(frame_izq, bg="white", padx=10, pady=10)

# Título con separador
ttk.Label(frame_completo, text="Proceso Interfaz Facturación Completo (5 fases)", style="Title.TLabel").pack(pady=(0, 15))
separator_h = ttk.Separator(frame_completo, orient="horizontal", style="Separator.TFrame")
separator_h.pack(fill="x", pady=5)

form_frame = tk.Frame(frame_completo, bg="white")
form_frame.pack(fill="x", pady=5)

ttk.Label(form_frame, text="Fecha contable:").pack(anchor="w", pady=2)
fecha_completo = DateEntry(form_frame, width=10, background="#01085A", foreground="white",
                         borderwidth=2, date_pattern="dd/mm/yyyy", font=("Arial", 11))
fecha_completo.pack(fill="x", pady=5)

btn_frame = tk.Frame(frame_completo, bg="white")
btn_frame.pack(fill="x", pady=15)

# Botón con bordes redondeados
btn_completo = tk.Button(btn_frame, text="EJECUTAR", bg="#264796", fg="white", 
                      font=("Arial", 11, "bold"), bd=0, padx=20, pady=5,
                      command=lambda: ejecutar_con_cierre(ejecutar_sac_process, fecha_completo.get()),
                      cursor="hand2", relief="flat", highlightthickness=0)
btn_completo.pack(pady=10, ipadx=20, ipady=5)
btn_completo.bind("<Enter>", lambda e: btn_completo.config(cursor="hand2"))

# Vista DETALLADA
frame_detallado = tk.Frame(frame_izq, bg="white", padx=10, pady=10)

# Título con separador
ttk.Label(frame_detallado, text="Proceso Interfaz Facturación fase única", style="Title.TLabel").pack(pady=(0, 15))
separator_h = ttk.Separator(frame_detallado, orient="horizontal", style="Separator.TFrame")
separator_h.pack(fill="x", pady=5)

form_frame = tk.Frame(frame_detallado, bg="white")
form_frame.pack(fill="x", pady=5)

ttk.Label(form_frame, text="Fecha contable:").pack(anchor="w", pady=2)
fecha_detallada = DateEntry(form_frame, width=8, background="#01085A", foreground="white",
                            borderwidth=2, date_pattern="dd/mm/yyyy", font=("Arial", 11))
fecha_detallada.pack(fill="x", pady=5)

ttk.Label(form_frame, text="Seleccione la fase (1-5):").pack(anchor="w", pady=(10, 2))
combo_fase = ttk.Combobox(form_frame, values=["1", "2", "3", "4", "5"], 
                         font=("Arial", 11), state="readonly", width=5)
combo_fase.set("1")
combo_fase.pack(anchor="w", pady=5)

btn_frame = tk.Frame(frame_detallado, bg="white")
btn_frame.pack(fill="x", pady=15)

# Botón con bordes redondeados
btn_detallado = tk.Button(btn_frame, text="EJECUTAR DETALLADO", bg="#264796", fg="white", 
                         font=("Arial", 11, "bold"), bd=0, padx=20, pady=5,
                         command=lambda: ejecutar_con_cierre(ejecutar_sac_detallado, fecha_detallada.get(), combo_fase.get()),
                         cursor="hand2", relief="flat", highlightthickness=0)
btn_detallado.pack(pady=10, ipadx=20, ipady=5)
btn_detallado.bind("<Enter>", lambda e: btn_detallado.config(cursor="hand2"))

# Selector de modo con separador
modo_frame = tk.Frame(frame_izq, bg="white", pady=10)
modo_frame.pack(fill="x")

ttk.Label(modo_frame, text="Seleccione el tipo de ejecución:").pack(side="left", padx=(0, 10))
modo_switch = ttk.Combobox(modo_frame, values=["Completo", "Detallado"], 
                          textvariable=modo, state="readonly", width=15)
modo_switch.pack(side="left")
modo_switch.bind("<<ComboboxSelected>>", lambda e: cambiar_modo())

separator_h = ttk.Separator(frame_izq, orient="horizontal", style="ThinSeparator.TFrame")
separator_h.pack(fill="x", pady=5)

# ========== CONFIGURACIÓN AVANZADA ==========
def config_entry(label_text, default):
    frame = tk.Frame(scrollable_frame, bg="white")
    frame.pack(fill="x", pady=3)
    
    ttk.Label(frame, text=label_text).pack(anchor="w", pady=(2, 0))
    e = ttk.Entry(frame, width=30)
    e.insert(0, str(default))
    e.pack(fill="x", pady=2)
    return e

# Configuración avanzada (oculta inicialmente)
CHROMEDRIVER_PATH = Path.home() / "Escritorio" / "chromedriver" / "chromedriver-win64" / "chromedriver.exe"
WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
EXCEL_PATH = Path.home() / "OneDrive - Grupo EPM" / "Documentos" / "InterfazFacturacion" / "07.  FFN014-V1-Formato Registro BATCH-ABRIL.xlsx"
RUTA_RES_CARGA = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "res_carga.txt"
USER = "EMONTANC"
PASS = "edmcESSA07**"
FOLDER_R5609FCT = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "R5609FCT"
FOLDER_DINAMICAS = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "ReportesDinamicaContable"
FOLDER_ORIGEN = Path.home() / "OneDrive - Grupo EPM" / "Descargas"
fecha_gen = "20250407"
fecha_con = "20250402"
fecha_con_lib = f"*{fecha_con}*"

entries = {}
entries['CHROMEDRIVER_PATH'] = config_entry("Ruta Chromedriver:", CHROMEDRIVER_PATH)
entries['WEBSITE_URL_JDE'] = config_entry("URL JDE:", WEBSITE_URL_JDE)
entries['EXCEL_PATH'] = config_entry("Ruta Excel:", EXCEL_PATH)
entries['RUTA_RES_CARGA'] = config_entry("Ruta resultado carga:", RUTA_RES_CARGA)
entries['USER'] = config_entry("Usuario:", USER)
entries['PASS'] = config_entry("Contraseña:", PASS)
entries['FOLDER_R5609FCT'] = config_entry("Carpeta R5609FCT:", FOLDER_R5609FCT)
entries['FOLDER_DINAMICAS'] = config_entry("Carpeta Reportes Dinámicos:", FOLDER_DINAMICAS)
entries['FOLDER_ORIGEN'] = config_entry("Carpeta Origen PDFs:", FOLDER_ORIGEN)
entries['fecha_gen'] = config_entry("Fecha generación:", fecha_gen)
entries['fecha_con'] = config_entry("Fecha contable:", fecha_con)
entries['fecha_con_lib'] = config_entry("Fecha contable lib:", fecha_con_lib)

# Ocultar configuración avanzada inicialmente
canvas.pack_forget()

# Mostrar vista correcta desde el inicio
cambiar_modo()
root.mainloop()
