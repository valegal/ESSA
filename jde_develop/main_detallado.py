from config import setup_driver, fecha_con_lib, USER, PASS, RUTA_RES_CARGA
from login import login, logout, recargar_pagina
from navigation import (
    navigate_to_carga_archivo, navigate_to_revision_hechos, navigate_control_archivos_cargados,
    navigate_home, navigate_agrupacion_hechos, navigate_generar_mov_contable,
    navigate_AD, navigate_pasa_comprobante_F0911Z1, navigate_revision_comprobante
)
from verify import verify_control_archivos
from actions import action_cargar_fases, agrupar, generar_movimiento_contable, contabilizar
from search import search_estado_registro
from goto import esperar_tareas_completas, actualizar_informes_recientes
from review import review_pdfs
from pull import paso_al_f0911
from batch_revisiones import buscar_revisiones_AD
import ctypes
import time
import os
import logging
from datetime import datetime

# Crear carpeta de logs si no existe
if not os.path.exists("logs"):
    os.makedirs("logs")

# Configuración de logging
log_filename = f"logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

def main():
    prevent_screen_lock()
    driver = setup_driver()
    start_time = time.time()

    logging.info("Iniciando sesión en el sistema.")
    login(driver, USER, PASS)

    #============= PASO 1: CARGA ARCHIVO IF ============= 
    logging.info("Paso 1: Navegando a 'Carga de archivo'")
    navigate_to_carga_archivo(driver)

    logging.info("Cargando fases con fecha: %s", fecha_con_lib)
    action_cargar_fases(driver, fecha_con_lib)

    actualizar_informes_recientes(driver)
    time.sleep(3)
    esperar_tareas_completas(driver, 5)
    recargar_pagina(driver)

    #=============  PASO 2: REVISIÓN HECHOS ECONÓMICOS ============= 
    logging.info("Paso 2: Revisión de hechos económicos")
    navigate_home(driver)
    time.sleep(3)
    navigate_to_revision_hechos(driver)
    time.sleep(3)
    search_estado_registro(driver)
    navigate_home(driver)
    recargar_pagina(driver)
    time.sleep(3)

    #=============  PASO 3: CONTROL DE ARCHIVOS CARGADOS ============= 
    logging.info("Paso 3: Verificando control de archivos cargados")
    navigate_control_archivos_cargados(driver)
    time.sleep(3)
    res_carga = verify_control_archivos(driver)
    values = list(res_carga.values())
    batchcarga = {values[i + 1]: values[i] for i in range(0, len(values), 2)}
    numbatchcarga = len(batchcarga)

    with open(RUTA_RES_CARGA, "w") as file:
        for key, value in batchcarga.items():
            file.write(f"{key} = {value}\n")
    logging.info("Archivo de control guardado en: %s", RUTA_RES_CARGA)

    navigate_home(driver)
    time.sleep(3)
    recargar_pagina(driver)

    #=============  PASO 4: AGRUPACIÓN HECHOS ECONÓMICOS ============= 
    logging.info("Paso 4: Agrupación de hechos económicos")
    for _ in range(numbatchcarga):
        navigate_agrupacion_hechos(driver)
        time.sleep(3)
        agrupar(driver, list(batchcarga.values())[_])
        recargar_pagina(driver)
        time.sleep(5)

    actualizar_informes_recientes(driver)
    time.sleep(3)
    esperar_tareas_completas(driver, numbatchcarga)
    recargar_pagina(driver)

    #=============  PASO 5: GENERAR MOVIMIENTO CONTABLE ============= 
    logging.info("Paso 5: Generar movimiento contable")
    for _ in range(numbatchcarga):
        navigate_generar_mov_contable(driver)
        time.sleep(3)
        generar_movimiento_contable(driver, list(batchcarga.values())[_])
        recargar_pagina(driver)
        time.sleep(3)

    actualizar_informes_recientes(driver)
    time.sleep(3)
    esperar_tareas_completas(driver, numbatchcarga)
    recargar_pagina(driver)

    #=============  PASO 6: REVISIÓN DE REPORTES CONTABLES ============= 
    logging.info("Paso 6: Revisión de reportes contables")
    valores_columna_dos = review_pdfs(driver, numbatchcarga, batchcarga)
    valores_columna_dos = dict(sorted(valores_columna_dos.items(), key=lambda x: int(x[0])))
    navigate_home(driver)
    recargar_pagina(driver)
    time.sleep(1)

    #=============  PASO 7: REVISIONES DE AD ============= 
    logging.info("Paso 7: Revisiones de AD")
    navigate_AD(driver)
    time.sleep(5)
    buscar_revisiones_AD(driver, valores_columna_dos)
    navigate_home(driver)
    recargar_pagina(driver)

    #=============  PASO 9: PASA COMPROBANTE ============= 
    logging.info("Paso 9: Pasa comprobante F0911Z1 a F0911")
    navigate_pasa_comprobante_F0911Z1(driver)
    time.sleep(5)
    campo_to_val = max(valores_columna_dos.values(), key=int)
    campo_from_val = min(valores_columna_dos.values(), key=int)
    paso_al_f0911(driver, campo_from_val, campo_to_val)
    time.sleep(3)
    recargar_pagina(driver)
    time.sleep(3)
    actualizar_informes_recientes(driver)
    time.sleep(3)
    esperar_tareas_completas(driver, 1)

    #=============  PASO 10: REVISIÓN DEL COMPROBANTE ============= 
    logging.info("Paso 10: Revisión del comprobante")
    time.sleep(7)
    navigate_revision_comprobante(driver)
    contabilizar(driver)
    navigate_home(driver)
    time.sleep(3)

    logging.info("Cerrando sesión y finalizando proceso.")
    logout(driver)
    restore_screen_lock()
    driver.quit()

    end_time = time.time()
    execution_time = end_time - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    formatted_time = f"{minutes}min {seconds}s"

    logging.info("Tiempo total de ejecución: %.2f segundos (%s)", execution_time, formatted_time)

def prevent_screen_lock():
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

def restore_screen_lock():
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

if __name__ == "__main__":
    main()
