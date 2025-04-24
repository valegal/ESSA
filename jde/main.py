from config import config, setup_driver
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
import logging

def main(fecha_contable=None):
    """Ejecuta el proceso completo de automatización"""
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
        logging.info("Paso 2: Cargando fases")
        logging.info("Cargando fases con fecha: %s", config.fecha_con)
        action_cargar_fases(driver, config.fecha_con_lib)

        actualizar_informes_recientes(driver)
        time.sleep(3)
        esperar_tareas_completas(driver, 5)
        recargar_pagina(driver)
        
        #============= PASO 3: Revisión de hechos económicos =============
        logging.info("Paso 3: Revisión de hechos económicos")
        navigate_home(driver)
        time.sleep(3)
        navigate_to_revision_hechos(driver)
        time.sleep(3)
        search_estado_registro(driver)
        navigate_home(driver)
        recargar_pagina(driver)
        time.sleep(3)

        #============= PASO 4: VERIFICACIÓN =============
        logging.info("Paso 4: Control de archivos")
        navigate_control_archivos_cargados(driver)
        time.sleep(3)
        res_carga = verify_control_archivos(driver)
        values = list(res_carga.values())
        batchcarga = {values[i + 1]: values[i] for i in range(0, len(values), 2)}
        numbatchcarga = len(batchcarga)

        with open(config.RUTA_RES_CARGA, "w") as file:
            for key, value in batchcarga.items():
                file.write(f"{key} = {value}\n")
        
        navigate_home(driver)
        time.sleep(3)
        recargar_pagina(driver)

        #============= PASO 5: AGRUPACIÓN =============
        logging.info("Paso 5: Agrupando hechos económicos")
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

        #============= PASO 6: MOVIMIENTO CONTABLE =============
        logging.info("Paso 6: Generando movimiento contable")
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

        #============= PASO 7: REVISIÓN REPORTES =============
        logging.info("Paso 7: Revisando reportes contables")
        valores_columna_dos = review_pdfs(driver, numbatchcarga, batchcarga)
        valores_columna_dos = dict(sorted(valores_columna_dos.items(), key=lambda x: int(x[0])))
        navigate_home(driver)
        recargar_pagina(driver)
        time.sleep(1)

        #============= PASO 8: REVISIONES AD =============
        logging.info("Paso 8: Revisiones AD")
        navigate_AD(driver)
        time.sleep(5)
        buscar_revisiones_AD(driver, valores_columna_dos)
        navigate_home(driver)
        recargar_pagina(driver)

        #============= PASO 9: PASA COMPROBANTE =============
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

        #============= PASO 10: CONTABILIZAR =============
        logging.info("Paso 10: Contabilizando")
        navigate_revision_comprobante(driver)
        contabilizar(driver)
        navigate_home(driver)

        #============= FINALIZACIÓN =============
        logging.info("Proceso completado exitosamente")
        logout(driver)
        
        end_time = time.time()
        logging.info(f"Tiempo total: {(end_time - start_time)/60:.2f} minutos")
        
        return True
        
    except Exception as e:
        logging.error(f"Error en proceso completo: {str(e)}")
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
    main()