import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import threading
from sac_process import ejecutar_sac_process
from sac_detallado import ejecutar_sac_detallado
import config_sac

def ejecutar_con_cierre(funcion, *args):
    def run_and_notify():
        try:
            funcion(*args)
            tk.messagebox.showinfo("Finalizado", "El proceso ha terminado correctamente.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")
    thread = threading.Thread(target=run_and_notify)
    thread.start() 

def cambiar_modo():
    if modo.get() == "Completo":
        frame_detallado.pack_forget()
        frame_completo.pack(fill="both", expand=True, padx=20, pady=10)
    else:
        frame_completo.pack_forget()
        frame_detallado.pack(fill="both", expand=True, padx=20, pady=10)

def toggle_config_panel():
    if config_frame.winfo_ismapped():
        config_frame.pack_forget()
        toggle_btn.config(text="Mostrar Configuración ▲")  
    else:
        config_frame.pack(fill="x", padx=20, pady=(0, 10))
        toggle_btn.config(text="Ocultar Configuración ▼") 

def save_config():
    config_sac.WEBSITE_SAC = website_entry.get()
    config_sac.USER = user_entry.get()
    config_sac.PASS = pass_entry.get()
    tk.messagebox.showinfo("Guardado", "Configuración guardada correctamente")

# --- Interfaz principal ---
root = tk.Tk()
root.title("Ejecutar Interfaz Facturación")
root.geometry("600x600")  # Aumentamos el tamaño para acomodar el panel de configuración
root.configure(bg="white")
root.resizable(False, False)

# Centrado en pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = (screen_width - 600) // 2
y_coord = (screen_height - 600) // 2
root.geometry(f"600x600+{x_coord}+{y_coord}")

# Icono
try:
    root.iconbitmap("logo.ico")
except:
    print("No se encontró el archivo logo.ico")

# Estilos
style = ttk.Style()
style.configure("Title.TLabel", font=("Arial", 14, "bold"), background="white", foreground="#01085A")
style.configure("Small.TLabel", font=("Arial", 9), background="white")
style.configure("TLabel", font=("Arial", 11), background="white")
style.configure("TButton", font=("Arial", 10), padding=6)

# Título y descripción
ttk.Label(root, text="Ejecución Interfaz Facturación | SAC", style="Title.TLabel").pack(pady=(15, 3))
ttk.Label(root, text="Seleccione fase y fecha contable para generar las interfaces de facturación en SAC.",
          wraplength=500, justify="center", style="Small.TLabel").pack(pady=(0, 10))

# Botón para mostrar/ocultar configuración
toggle_btn = ttk.Button(root, text="Mostrar Configuración ▲", command=toggle_config_panel)
toggle_btn.pack(pady=(0, 5))

# Panel de configuración (inicialmente oculto)
config_frame = tk.Frame(root, bg="white", bd=1, relief="solid", padx=10, pady=10)

# Campos de configuración
ttk.Label(config_frame, text="Configuración de Conexión", style="Title.TLabel", background="white").pack(anchor="w")

form_config = tk.Frame(config_frame, bg="white")
form_config.pack(fill="x", pady=5)

ttk.Label(form_config, text="URL SAC:", background="white").grid(row=0, column=0, sticky="w", pady=2)
website_entry = ttk.Entry(form_config, width=40)
website_entry.insert(0, config_sac.WEBSITE_SAC)
website_entry.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(form_config, text="Usuario:", background="white").grid(row=1, column=0, sticky="w", pady=2)
user_entry = ttk.Entry(form_config, width=40)
user_entry.insert(0, config_sac.USER)
user_entry.grid(row=1, column=1, padx=5, pady=2)

ttk.Label(form_config, text="Contraseña:", background="white").grid(row=2, column=0, sticky="w", pady=2)
pass_entry = ttk.Entry(form_config, width=40, show="•")
pass_entry.insert(0, config_sac.PASS)
pass_entry.grid(row=2, column=1, padx=5, pady=2)

save_btn = ttk.Button(config_frame, text="Guardar Configuración", command=save_config)
save_btn.pack(pady=(5, 0))

# Selector de modo
modo = tk.StringVar(value="Completo")
frame_modo = tk.Frame(root, bg="white")
frame_modo.pack(pady=(0, 10), anchor="w", padx=30)

ttk.Label(frame_modo, text="Seleccione el modo:").pack(side="left", padx=(0, 10))
ttk.Radiobutton(frame_modo, text="Completo", variable=modo, value="Completo", command=cambiar_modo).pack(side="left")
ttk.Radiobutton(frame_modo, text="Detallado", variable=modo, value="Detallado", command=cambiar_modo).pack(side="left")

# Contenedor principal
frame_izq = tk.Frame(root, bg="white")
frame_izq.pack(fill="both", expand=True)

# Vista COMPLETO
frame_completo = tk.Frame(frame_izq, bg="white", padx=10, pady=10)
ttk.Label(frame_completo, text="Generar todas las fases", style="Title.TLabel").pack(pady=(0, 10))
ttk.Separator(frame_completo, orient="horizontal").pack(fill="x", pady=5)

form_c = tk.Frame(frame_completo, bg="white")
form_c.pack(pady=10)

ttk.Label(form_c, text="Fecha contable:").pack(anchor="center", pady=2)
fecha_completo = DateEntry(form_c, width=18, background="#01085A", foreground="white",
                       borderwidth=2, date_pattern="dd/mm/yyyy", font=("Arial", 11))
fecha_completo.pack(pady=5)

btn_completo = tk.Button(frame_completo, text="Ejecutar", bg="#264796", fg="white",
                     font=("Arial", 11, "bold"), bd=0, padx=20, pady=5,
                     command=lambda: ejecutar_con_cierre(ejecutar_sac_process, fecha_completo.get()),
                     cursor="hand2", relief="flat", highlightthickness=0)
btn_completo.pack(pady=15)

# Vista DETALLADO
frame_detallado = tk.Frame(frame_izq, bg="white", padx=10, pady=10)
ttk.Label(frame_detallado, text="Generar fases(1-5)", style="Title.TLabel").pack(pady=(0, 10))
ttk.Separator(frame_detallado, orient="horizontal").pack(fill="x", pady=5)

form_d = tk.Frame(frame_detallado, bg="white")
form_d.pack(pady=10)

ttk.Label(form_d, text="Fecha contable:").pack(anchor="center", pady=2)
fecha_detallada = DateEntry(form_d, width=18, background="#01085A", foreground="white",
                        borderwidth=2, date_pattern="dd/mm/yyyy", font=("Arial", 11))
fecha_detallada.pack(pady=5)

ttk.Label(form_d, text="Seleccione la fase (1-5):").pack(anchor="center", pady=(10, 2))
combo_fase = ttk.Combobox(form_d, values=["1", "2", "3", "4", "5"],
                      font=("Arial", 11), state="readonly", width=18)
combo_fase.set("1")
combo_fase.pack(pady=5)

btn_detallado = tk.Button(frame_detallado, text="Ejecutar detallado", bg="#264796", fg="white",
                      font=("Arial", 11, "bold"), bd=0, padx=20, pady=5,
                      command=lambda: ejecutar_con_cierre(ejecutar_sac_detallado, fecha_detallada.get(), combo_fase.get()),
                      cursor="hand2", relief="flat", highlightthickness=0)
btn_detallado.pack(pady=15)

# Mostrar vista por defecto
cambiar_modo()

# Ejecutar ventana
root.mainloop()