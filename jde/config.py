import sys
import os
from pathlib import Path
import logging
from datetime import datetime

class Config:
    def __init__(self):
        # Rutas esenciales - Versión mejorada
        self.BASE_DIR = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(__file__).parent
        self.CHROMEDRIVER_PATH = str(Path(sys._MEIPASS) / "driver" / "chromedriver.exe") if hasattr(sys, '_MEIPASS') else str(self.BASE_DIR / "driver" / "chromedriver.exe")
        self.WEBSITE_URL_JDE = "https://epm-vws20c.corp.epm.com.co/jde/E1Menu.maf"
        self.EXCEL_PATH = str(Path.home() / "Documents" / "07.  FFN014-V1-Formato Registro BATCH-ABRIL.xlsx")
        self.RUTA_RES_CARGA = str(Path.home() / "Downloads" / "res_carga.txt")
        
        # Credenciales (se configurarán desde UI)
        self.USER = "EMONTANC"
        self.PASS = ""
        
        # Carpetas de descarga
        self.FOLDER_R5609FCT = str(Path.home() / "Downloads" / "R5609FCT")
        self.FOLDER_DINAMICAS = str(Path.home() / "Downloads" / "ReportesDinamicaContable")
        self.FOLDER_ORIGEN = str(Path.home() / "Downloads")
        
        # Fechas configurables
        self.fecha_gen = ""
        self.fecha_con = ""
        # self.fecha_con_lib = ""
        
        # Configuración de logging
        self.log_dir = self.BASE_DIR / "logs"
        self.setup_logging()

    def setup_logging(self):
        """Configura el sistema de logging"""
        if not self.log_dir.exists():
            self.log_dir.mkdir()
        
        log_file = self.log_dir / f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def update_from_ui(self, ui_settings):
        """Actualiza configuración desde la interfaz gráfica"""
        for key, value in ui_settings.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Actualizar fecha contable
        if self.fecha_con:
            self.fecha_con_lib = f"*{self.fecha_con}*"
        
        # Crear carpetas si no existen
        Path(self.FOLDER_R5609FCT).mkdir(exist_ok=True)
        Path(self.FOLDER_DINAMICAS).mkdir(exist_ok=True)

# Instancia global de configuración
config = Config()

# Configuración de Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def setup_driver():
    """Configura el WebDriver de Chrome"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors=yes")
        
        service = Service(executable_path=config.CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        return driver
    except Exception as e:
        logging.error(f"Error al configurar el driver: {str(e)}")
        raise