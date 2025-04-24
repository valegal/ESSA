from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from navigation import navigate_home
import time
import pyautogui
from config import USER

#================================================================================

def buscar_revisiones_AD(driver, valores):
    try:
        
        # Switch back to default content
        driver.switch_to.default_content()
        # Switch to the iframe
        WebDriverWait(driver, 150).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "e1menuAppIframe"))
        )

        # Process each batch number in the valores dictionary
        for key, valor in valores.items():
            print(f"Processing batch number: {valor}")
           
            # Step 1: Enter user ID
            input_field = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='qbeRow0_1']/td[2]/div/nobr/input"))
            )
            input_field.click()
            input_field.clear()
            input_field.send_keys(USER)
            time.sleep(2)

            # Step 2: Enter batch number
            input_batch = driver.find_element(By.XPATH, "//*[@id='C0_106']")
            input_batch.click()
            input_batch.send_keys(Keys.BACKSPACE * 10)  # Clear the field
            for digito in str(valor):
                input_batch.send_keys(digito)
                time.sleep(0.2)

            # Click search button
            boton_buscar = driver.find_element(By.XPATH, "//*[@id='hc_Find']")
            ActionChains(driver).move_to_element(boton_buscar).click().perform()

            # Espera después del clic en Buscar
            esperar_elemento_con_movimiento(driver, "//*[@id='G0_1_R0']/td[1]/div/input")

            # Doble clic en el radio button
            radio_button = WebDriverWait(driver, 80).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='G0_1_R0']/td[1]/div/input"))
            )
            ActionChains(driver).double_click(radio_button).perform()


            # Espera específica para que el campo del número de lote aparezca o detectar si se regresó al menú
            max_intentos_doble_click = 3
            intentos = 0
            while intentos < max_intentos_doble_click:
                try:
                    WebDriverWait(driver, 50).until(
                        EC.presence_of_element_located((By.XPATH, "//*[@id='C0_9']"))
                    )
                    break  # Si se encuentra el campo esperado, salir del bucle
                except:
                    # Verificar si volvió al menú principal (presencia del label inesperado)
                    try:
                        driver.find_element(By.XPATH, '//*[@id="div0_81"]/span/nobr/label')
                        print("Detectado retorno al menú principal. Reintentando doble clic en el radio button...")
                        
                        # Rehacer el doble clic
                        radio_button = WebDriverWait(driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, "//*[@id='G0_1_R0']/td[1]/div/input"))
                        )
                        ActionChains(driver).double_click(radio_button).perform()
                        time.sleep(3)
                        intentos += 1
                    except:
                        # Si no está el menú principal, asumimos otro error y rompemos
                        raise TimeoutError("No se encontró el campo 'C0_9' ni el label de retorno al menú.")
            else:
                raise TimeoutError("No se pudo acceder al detalle del lote después de múltiples intentos.")


            time.sleep(5)

            # Get batch number confirmation
            batch_confirmation = driver.find_element(By.XPATH, "//*[@id='C0_9']")
            print(f"Confirmed batch number: {batch_confirmation.get_attribute('value')}")

            # Get the batch date
            fecha_ad_batch = driver.find_element(By.XPATH, "//*[@id='C0_121']").get_attribute('value')
           
            # Get document type and map to description
            doc_type_element = driver.find_element(By.XPATH, "//*[@id='C0_115']")
            doc_type = doc_type_element.get_attribute('value')
           
            doc_type_mapping = {
                'J1': 'FACTURACIÓN',
                'DT': 'AUTOCONSUMOS',
                'DY': 'AJUSTES',
                'DZ': 'RECAUDOS',
                'DX': 'CASTIGO'
            }
           
            doc_description = doc_type_mapping.get(doc_type, 'DESCONOCIDO')
           
            # Update the explanation field
            explanation_field = driver.find_element(By.XPATH, "//*[@id='C0_129']")
            explanation_field.click()
            explanation_field.clear()
            new_explanation = f"{doc_description} {fecha_ad_batch}"
            explanation_field.send_keys(new_explanation)
           
            # Click OK button
            ok_button = driver.find_element(By.XPATH, "//*[@id='hc_OK']")
            ok_button.click()

            # Special handling for RECAUDOS (DZ) batches
            if doc_type == 'DZ':
                print("Processing RECAUDOS batch - handling potential errors...")
                time.sleep(7)
                handle_recaudos_errors(driver)
    
            # Wait for processing to complete
            time.sleep(5)
            print(f"Completed processing for batch {valor}")
           
        print("Todos los lotes se procesaron correctamente.")
       
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Switch back to default content
        driver.switch_to.default_content()
        navigate_home(driver)


#================================================================================

def handle_recaudos_errors(driver):
    """Maneja errores de los lotes tipo DZ en JD Edwards (RECAUDOS)"""
    try:
        # Volver al iframe en caso de que nos hayamos salido
        driver.switch_to.default_content()
        WebDriverWait(driver, 40).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "e1menuAppIframe"))
        )

        print("Esperando aparición del panel de errores...")
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Libro mayor auxiliar 00077777 y A  no válidos')]"))
        )
        print("Errores detectados. Procesando...")

        errores_procesados = set()
        intentos = 0
        max_intentos = 25

        while intentos < max_intentos:
            intentos += 1

            # Scroll para asegurar que todos los errores estén visibles
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Captura todos los errores visibles
            bloques_error = driver.find_elements(By.XPATH, "//a[contains(@href, 'inyfeHandler.goToError')]")

            if not bloques_error:
                print("No se encontraron más errores visibles.")
                break

            nuevos = [e for e in bloques_error if e.get_attribute('href') not in errores_procesados]

            if not nuevos:
                print("Todos los errores han sido procesados.")
                break
            

            for link in nuevos:
                try:
                    href = link.get_attribute('href')
                    print(f"Procesando error: {link.text}")

                    # Hacer clic en el link "Ir a error"
                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(0.5)
                    link.click()
                    errores_procesados.add(href)
                    time.sleep(2)

                    # Espera breve por si aparece un campo editable o algo
                    ActionChains(driver).send_keys("9443").send_keys(Keys.ARROW_DOWN).perform()
                    time.sleep(2)

                except Exception as e:
                    print(f"Error al hacer clic en error: {e}")
                    continue

            time.sleep(2)

    except Exception as e:
        print(f"No se detectaron errores o hubo una excepción: {e}")

    # Intentar cerrar con OK al final del manejo de errores
    try:
        print("Esperando que la interfaz se asiente tras corregir errores...")
        time.sleep(8)  # Espera base tras corrección de errores

        # Espera extendida para que reaparezca el botón OK
        ok_button = WebDriverWait(driver, 120).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='hc_OK']"))
        )
        print("Botón OK detectado, intentando presionar...")

        # Intentamos un clic normal
        ok_button.click()
        time.sleep(3)

        # Verificamos si seguimos en la misma pantalla (por si no funcionó el clic)
        reintentos = 0
        while reintentos < 3:
            try:
                # Si el botón OK sigue presente, quizás no hizo efecto
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='hc_OK']"))
                )
                print("Botón OK aún presente, intentando doble clic.")
                ActionChains(driver).double_click(ok_button).perform()
                time.sleep(3)
                reintentos += 1
            except:
                break

        print("Esperando retorno a la vista principal...")
        esperar_elemento_con_movimiento(driver, "//*[@id='qbeRow0_1']/td[2]/div/nobr/input", timeout=600)
        print("Retorno confirmado.")

    except Exception as e:
        print(f"Fallo al intentar presionar el segundo OK o al volver al menú principal: {e}")
    
    time.sleep(2)


#================================================================================

def esperar_elemento_con_movimiento(driver, xpath_objetivo, timeout=900):
    """
    Espera hasta 15 minutos (por defecto) que un elemento esté presente,
    o que desaparezca la animación de carga. Mientras tanto, mueve el mouse
    de forma sutil para mantener activa la sesión.
    """
    inicio = time.time()
    while (time.time() - inicio) < timeout:
        try:
            # Si el elemento objetivo está presente, salir del bucle
            if driver.find_elements(By.XPATH, xpath_objetivo):
                return True

            # Si no hay más gifs de carga, también se puede salir
            loading = driver.find_elements(By.XPATH, "//img[@src='/jde/img/fetch_animation.gif']")
            if not loading:
                return True

        except Exception as e:
            print(f"Esperando... {e}")

        # Movimiento sutil del mouse
        try:
            pyautogui.moveRel(1, 0, duration=0.1)
            pyautogui.moveRel(-1, 0, duration=0.1)
        except:
            pass

        time.sleep(2)  # Esperar antes del siguiente intento

    raise TimeoutError(f"No se encontró el elemento {xpath_objetivo} tras {timeout} segundos.")