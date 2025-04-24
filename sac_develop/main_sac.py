import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import threading
from sac_process import ejecutar_sac_process

def ejecutar_sac_process_con_cierre(fecha):
    """Ejecuta el proceso en un hilo independiente y cierra la ventana después de unos segundos."""
    thread = threading.Thread(target=ejecutar_sac_process, args=(fecha,))
    thread.start()  # Inicia el hilo sin daemon=True para que continúe después de cerrar la ventana.
    root.after(3000, root.destroy)  # Cierra la ventana en 3 segundos.

if __name__ == "__main__":

    root = tk.Tk()
    root.title("    SAC Process")
    root.geometry("500x350")  # Aumentamos el tamaño
    root.configure(bg="white")  # Azul celeste de la paleta
    root.resizable(False, False)

    # Centrar en pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coord = (screen_width - 500) // 2
    y_coord = (screen_height - 350) // 2
    root.geometry(f"500x350+{x_coord}+{y_coord}")

    # Cambiar el icono de la ventana (requiere 'logo.ico' en la misma carpeta)
    try:
        root.iconbitmap("logo.ico")
    except:
        print("No se encontró el archivo logo.ico")

    # Estilos
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 14, "bold"), background="white", foreground="#01085A")
    style.configure("TButton", font=("Arial", 12), padding=6, background="#264796", foreground="#01085A")
    style.configure("TEntry", font=("Arial", 12))

    # Etiqueta principal
    label_fecha = ttk.Label(root, text="Seleccione la fecha:")
    label_fecha.pack(pady=(40, 5))

    # Descripción más pequeña debajo
    label_desc = ttk.Label(root, text="Primero escriba la fecha del día que desea generar las 5 fases para ejecutar el proceso de Interfaz de facturación en SAC:",
                            font=("Arial", 9), wraplength=450, justify="center")
    label_desc.pack(pady=(0, 10))

    # Selector de fecha más grande y ancho
    fecha_selector = DateEntry(root, width=18, background="#01085A", foreground="white",
                            borderwidth=3, date_pattern="dd/mm/yyyy", font=("Arial", 12))
    fecha_selector.pack(pady=10)

    # Botón de ejecución
    btn_ejecutar = ttk.Button(root, text="Ejecutar", command=lambda: ejecutar_sac_process_con_cierre(fecha_selector.get()))
    btn_ejecutar.pack(pady=20)

    # Ejecutar la ventana
    root.mainloop()
