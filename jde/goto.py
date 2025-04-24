from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from navigation import navigate_home
from login import recargar_pagina
import time


# ---------------------------------------------------------------------------------

def debug_print(message):
    """Función auxiliar para mensajes de depuración"""
    print(f"🔍 [DEBUG] {message}")


# ---------------------------------------------------------------------------------
def goto_verificar(driver, files):
    """
    Esta función automatiza la verificación del estado de trabajo de las tareas
    con múltiples capas de depuración.
    """
    debug_print("Iniciando función goto_verificar")
   
    # Lista para almacenar tareas
    tareas = []

    try:
        # Verificar número real de filas visibles
        filas_visibles = driver.find_elements(By.XPATH, "//tr[contains(@id, 'G0_1_R')]")
        debug_print(f"Total de filas encontradas: {len(filas_visibles)}")
       
        # Verificar input de usuario como prueba de que la página está cargada
        try:
            input_usuario = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="C0_29"]'))
            )
            valor = input_usuario.get_attribute("value")
            debug_print(f"Valor del input 'ID del usuario': {valor}")
        except Exception as e:
            debug_print(f"No se pudo encontrar el input de usuario: {str(e)}")

        # Limitar el número de filas a procesar al mínimo entre files y filas reales
        files_to_process = min(files, len(filas_visibles))
        debug_print(f"Procesando {files_to_process} filas")

        for i in range(files_to_process):
            try:
                debug_print(f"\nProcesando fila {i}")
               
                # Construir XPaths alternativos
                xpath_alternatives = [
                    f"//*[@id='G0_1_R{i}']/td[4]/div",  # XPath original
                    f"//tr[contains(@id, 'G0_1_R')][{i+1}]/td[4]/div",  # XPath más flexible
                    f"(//tr[starts-with(@id, 'G0_1_R')])[{i+1}]/td[4]/div"  # Otra variante
                ]
               
                tarea_element = None
                estado_element = None
               
                # Intentar diferentes variantes de XPath para la tarea
                for xpath in xpath_alternatives:
                    try:
    
                        debug_print("Icono de cerrar clickeado")
                        tarea_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, xpath))
                        )
                        debug_print(f"Encontrada tarea con XPath: {xpath}")
                        break
                    except Exception as e:
                        debug_print(f"XPath fallido para tarea ({xpath}): {str(e)}")
                        continue
               
                if not tarea_element:
                    raise NoSuchElementException(f"No se pudo encontrar elemento de tarea en fila {i}")

                # Intentar diferentes variantes de XPath para el estado
                estado_xpath_alternatives = [
                    f"//*[@id='G0_1_R{i}']/td[9]/div",  # XPath original
                    f"//tr[contains(@id, 'G0_1_R')][{i+1}]/td[9]/div",  # XPath más flexible
                    f"(//tr[starts-with(@id, 'G0_1_R')])[{i+1}]/td[9]/div"  # Otra variante
                ]
               
                for xpath in estado_xpath_alternatives:
                    try:
                        estado_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, xpath))
                        )
                        debug_print(f"Encontrado estado con XPath: {xpath}")
                        break
                    except Exception as e:
                        debug_print(f"XPath fallido para estado ({xpath}): {str(e)}")
                        continue
               
                if not estado_element:
                    raise NoSuchElementException(f"No se pudo encontrar elemento de estado en fila {i}")

                # Obtener textos
                tarea_text = tarea_element.text
                estado_text = estado_element.text
                debug_print(f"Fila {i}: Tarea='{tarea_text}', Estado='{estado_text}'")
               
                tareas.append((tarea_text, estado_text))

                time.sleep(1)

               
            except Exception as e:
                debug_print(f"Error procesando fila {i}: {str(e)}")
                continue

    except Exception as e:
        debug_print(f"Error general en goto_verificar: {str(e)}")
        raise

    # Hacer clic en el icono de buscar
    buscar = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='hc_Find']"))
    )
    ActionChains(driver).move_to_element(buscar).click().perform()

    debug_print(f"Resultados obtenidos: {tareas}")
    return tareas
# ---------------------------------------------------------------------------------

def actualizar_informes_recientes(driver):
    """Actualiza la lista de informes recientes con doble clic"""
    debug_print("Intentando actualizar informes recientes")
   
    try:
        update_button = WebDriverWait(driver, 50).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='listRecRptsPositionHelper']/a"))
        )
       
        # Desplazar el elemento a la vista si es necesario
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", update_button)
        time.sleep(1)  # Pequeña pausa para el desplazamiento
       
        # Hacer doble clic
        ActionChains(driver).double_click(update_button).perform()
        debug_print("Actualización de informes realizada")
        time.sleep(2)  # Esperar a que se complete la actualización
    except Exception as e:
        debug_print(f"Error al actualizar informes: {str(e)}")
        raise
# ---------------------------------------------------------------------------------

def esperar_tareas_completas(driver, files, max_retries=60, retry_interval=35):
    """
    Ejecuta goto_verificar hasta que todas las tareas estén en estado 'Hecho'
    con múltiples capas de depuración.
    """
    debug_print("Iniciando espera de tareas completas")
   
    try:
        # Hacer clic en el icono de la tabla
        icono = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='listRRpt_WSJ']/table/tbody/tr/td[1]"))
        )
        icono.click()
        debug_print("Icono de tabla clickeado")
        time.sleep(4)

        # Cambiar al iframe
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "e1menuAppIframe")))
        driver.switch_to.frame(driver.find_element(By.ID, "e1menuAppIframe"))
        debug_print("Cambiado al iframe e1menuAppIframe")

        for intento in range(max_retries):
            debug_print(f"\nIntento {intento + 1}/{max_retries}")
           
            try:
                tareas = goto_verificar(driver, files)
               
                if not tareas:
                    debug_print("No se encontraron tareas. Reintentando...")
                    time.sleep(retry_interval)
                    continue
               
                # Verificar estados
                estados = [estado for _, estado in tareas]
                debug_print(f"Estados encontrados: {estados}")
               
                if all(estado == "Hecho" for estado in estados):
                    debug_print("✅ Todas las tareas están en estado 'Hecho'")
                    time.sleep(3)
                    # Hacer clic en el icono de cerrar
                    cerrar = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='hc_Close']"))
                    )
                    cerrar.click()

                    time.sleep(1)
                    navigate_home(driver)
                    return True
               
                # Contar tareas pendientes
                pendientes = sum(1 for estado in estados if estado != "Hecho")
                debug_print(f"⚠️ {pendientes} tareas pendientes de {len(tareas)}")

                                
                # Hacer clic en el icono de buscar PARA REFRESCAR LOS DATOS
                buscar = WebDriverWait(driver, 100).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='hc_Find']"))
                        )
                buscar.click()
               
                # Esperar para el próximo intento
                debug_print(f"Esperando {retry_interval} segundos...")
                time.sleep(retry_interval)
      
               
            except Exception as e:
                debug_print(f"Error en el intento {intento + 1}: {str(e)}")
                time.sleep(retry_interval)
                continue

        debug_print("Se alcanzó el tiempo máximo de espera")
        return False

    except Exception as e:
        debug_print(f"Error general en esperar_tareas_completas: {str(e)}")
        raise
