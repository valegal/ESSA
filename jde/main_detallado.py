from config import config, setup_driver
from login import login, logout, recargar_pagina
from navigation import (
    navigate_to_carga_archivo, navigate_to_revision_hechos, navigate_control_archivos_cargados,
    navigate_home, navigate_agrupacion_hechos, navigate_generar_mov_contable,
    navigate_AD, navigate_pasa_comprobante_F0911Z1, navigate_revision_comprobante
)
from verify import verify_control_archivos
from update import cargar_una_fase, agrupar_uno, generar_movimiento_contable_uno, contabilizar_uno
from search import search_estado_registro
from goto import esperar_tareas_completas, actualizar_informes_recientes
from review import review_pdf_unico
from pull import paso_al_f0911
from batch_revisiones import buscar_revisiones_AD
import ctypes
import time
import logging

def main_detallado(fecha_contable=None, fase="01"):
    """Ejecuta una fase específica del proceso"""
    try:
        # Actualizar fecha si se proporciona
        if fecha_contable:
            config.fecha_con = fecha_contable.strftime("%Y%m%d")
            config.fecha_con_lib = f"*{config.fecha_con}*"
        
        prevent_screen_lock()
        driver = setup_driver() 
        start_time = time.time()

        logging.info("Iniciando proceso completo de automatización")
        logging.info(f"Fecha contable: {config.fecha_con}")
        
        #============= PASO 1: LOGIN Y CARGA ARCHIVO =============
        logging.info("Paso 1: Iniciando sesión y Navegando a 'Carga de archivo'")
        login(driver, config.USER, config.PASS)
        
        #============= PASO 2: CARGAR ARCHIVOS =============
        navigate_to_carga_archivo(driver)
        time.sleep(3)
        logging.info(f"Paso 2: Cargando fase {fase}")
        logging.info("Cargando fases con fecha: %s", config.fecha_con)
        cargar_una_fase(driver, config.fecha_con_lib, fase)

        actualizar_informes_recientes(driver)
        time.sleep(3)
        esperar_tareas_completas(driver, 1)
        recargar_pagina(driver)

        #============= PASO 3: VERIFICACIÓN =============
        logging.info("Paso 3: Verificando control de archivos")
        navigate_control_archivos_cargados(driver)
        time.sleep(3)
        res_carga = verify_control_archivos(driver)
        batch_num = res_carga.get(f"Fase {fase}", "")
        
        if not batch_num:
            raise ValueError(f"No se encontró número de batch para fase {fase}")

        with open(config.RUTA_RES_CARGA, "w") as file:
            file.write(f"Fase {fase} = {batch_num}\n")
        
        navigate_home(driver)
        recargar_pagina(driver)

        #============= PASO 4: AGRUPACIÓN =============
        logging.info(f"Paso 4: Agrupando fase {fase}")
        navigate_agrupacion_hechos(driver)
        time.sleep(3)
        agrupar_uno(driver, batch_num)
        
        actualizar_informes_recientes(driver)
        esperar_tareas_completas(driver, 1)
        recargar_pagina(driver)

        #============= PASO 5: MOVIMIENTO CONTABLE =============
        logging.info(f"Paso 5: Generando movimiento para fase {fase}")
        navigate_generar_mov_contable(driver)
        time.sleep(3)
        generar_movimiento_contable_uno(driver, batch_num)
        
        actualizar_informes_recientes(driver)
        esperar_tareas_completas(driver, 1)
        recargar_pagina(driver)

        #============= PASO 6: REVISIÓN REPORTE =============
        logging.info(f"Paso 6: Revisando reporte fase {fase}")
        valor_columna = review_pdf_unico(driver, fase, batch_num)
        navigate_home(driver)
        recargar_pagina(driver)

        #============= PASO 7: REVISIÓN AD =============
        logging.info(f"Paso 7: Revisión AD fase {fase}")
        navigate_AD(driver)
        time.sleep(5)
        buscar_revisiones_AD(driver, valor_columna)
        navigate_home(driver)
        recargar_pagina(driver)

        #============= PASO 8: PASA COMPROBANTE =============
        logging.info(f"Paso 8: Pasando comprobante fase {fase}")
        navigate_pasa_comprobante_F0911Z1(driver)
        time.sleep(5)
        paso_al_f0911(driver, valor_columna, valor_columna)
        
        actualizar_informes_recientes(driver)
        esperar_tareas_completas(driver, 1)

        #============= PASO 9: CONTABILIZAR =============
        logging.info(f"Paso 9: Contabilizando fase {fase}")
        navigate_revision_comprobante(driver)
        contabilizar_uno(driver)
        navigate_home(driver)

        logging.info(f"Fase {fase} completada exitosamente")
        logout(driver)
        
        end_time = time.time()
        logging.info(f"Tiempo total fase {fase}: {(end_time - start_time)/60:.2f} minutos")
        
        return True
        
    except Exception as e:
        logging.error(f"Error en fase {fase}: {str(e)}")
        return False
    finally:
        try:
            driver.quit()
        except:
            pass
        restore_screen_lock()

def prevent_screen_lock():
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    except:
        pass

def restore_screen_lock():
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
    except:
        pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        from datetime import datetime
        fecha = datetime.strptime(sys.argv[1], "%Y%m%d").date()
        fase = int(sys.argv[2])
        main_detallado(fecha, fase)