import tkinter as tk
from tkinter import messagebox
import main
import config

def ejecutar_proceso():
    fecha_gen = entry_fecha_gen.get()
    fecha_con = entry_fecha_con.get()
    
    if not fecha_gen or not fecha_con:
        messagebox.showerror("Error", "Por favor, ingrese ambas fechas.")
        return
    
    # Pasar las fechas al módulo main antes de ejecutarlo
    config.fecha_gen = fecha_gen
    config.fecha_con = fecha_con
    
    try:
        main.main()  # Ejecutar el proceso principal
        messagebox.showinfo("Proceso Completado", "El proceso se ha ejecutado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Ejecutor de Selenium")
root.geometry("400x200")

tk.Label(root, text="Fecha Gen (YYYYMMDD):").pack()
entry_fecha_gen = tk.Entry(root)
entry_fecha_gen.pack()

tk.Label(root, text="Fecha Con (YYYYMMDD):").pack()
entry_fecha_con = tk.Entry(root)
entry_fecha_con.pack()

tk.Button(root, text="Ejecutar", command=ejecutar_proceso).pack()

root.mainloop()
