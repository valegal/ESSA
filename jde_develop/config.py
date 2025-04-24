from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import logging
from pathlib import Path
import os

#========= Configuración general ==========

# Rutas
CHROMEDRIVER_PATH = os.path.join(os.path.dirname(__file__), 'driver', 'chromedriver.exe')
WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
EXCEL_PATH = Path.home() / "OneDrive - Grupo EPM" / "Documentos" / "InterfazFacturacion" / "07.  FFN014-V1-Formato Registro BATCH-ABRIL.xlsx"
RUTA_RES_CARGA = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "res_carga.txt"

# Credenciales
USER = "EMONTANC"
PASS = "edmcESSA08**"

# Carpeta con los archivos PDF
FOLDER_R5609FCT = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "R5609FCT"
FOLDER_DINAMICAS = Path.home() / "OneDrive - Grupo EPM" / "Descargas" / "ReportesDinamicaContable"
FOLDER_ORIGEN = Path.home() / "OneDrive - Grupo EPM" / "Descargas" 

# Variables modificables por el usuario
fecha_gen = "20250410"
fecha_con = "20250404"
fecha_con_lib = f"*{fecha_con}*"

#-------------------------------------------------------------------------------------------------------

def setup_driver():
    """Configura y retorna el driver de Selenium."""
    
    # Ignorar errores SSL
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors=yes')  # Esto también ayuda a ignorar los errores SSL

    # Redirigir los logs de Chrome para evitar mostrar mensajes de SSL en consola
    options.add_argument('--disable-logging')
    # options.add_argument('--log-level=3')  # Esto suprime los mensajes de log

    # Crear el driver de Selenium con la configuración de opciones
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    # Ajustar ventana del navegador
    # driver.set_window_position(0, -1080)
    driver.maximize_window()
    
    return driver
