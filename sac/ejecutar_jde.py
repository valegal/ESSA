import subprocess
import time

def ejecutar_main_jde():
    """Ejecuta el script main.py en el directorio jde después de cerrar el navegador."""
    # Esperar un poco para asegurar que el navegador cerró completamente
    time.sleep(2)

    # Ruta del script a ejecutar
    script_jde_path = r"D:\OneDrive - Grupo EPM\Documentos\github\Advanced-Python\automate-general\auto_modules\jde\main.py"

    # Ejecutar el script main.py en jde
    try:
        print("Ejecutando main.py en jde...")
        subprocess.run(["python", script_jde_path], check=True, shell=True)
        print("main.py ejecutado con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar main.py: {e}")
