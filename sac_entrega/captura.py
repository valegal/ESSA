# captura.py
import sys

class CapturaDeSalida:
    def __init__(self):
        self.texto = ""

    def write(self, texto):
        self.texto += texto

# Función para capturar la salida en un archivo
def capturar_output():
    captura = CapturaDeSalida()
    sys.stdout = captura  # Redirigir la salida estándar
    sys.stderr = captura  # Redirigir los errores también

    return captura
