from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from navigation import switch_to_iframe, navigate_home
from config import USER
import time

#--------------------------------------------------------------------------------------------

def search_estado_registro(driver):
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")

    try:
        # Buscar el número 8 en Estado Registro
        input_estado_registro = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".textfield.associated0_19")))

        input_estado_registro.clear()
        time.sleep(1)
        input_estado_registro.send_keys("8")
        time.sleep(1)

        # Buscar y hacer clic en el botón de búsqueda
        boton_buscar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "hc_Find"))
        )
        boton_buscar.click()

        # Esperar a que los resultados carguen
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "JSSelectGrid"))
        )
        time.sleep(5)

        # Buscar los radio buttons dentro de JSSelectGrid
        radio_buttons = WebDriverWait(driver, 50).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//input[@type='radio' and @name='grs0_1']"))
        )

        if len(radio_buttons) == 10:
            ruta_archivo = "C:/Users/vgaleanc/Escritorio/fallo.txt"
            print(f"✅ Se encontraron {len(radio_buttons)} radio button(s).")
            with open(ruta_archivo, "w") as file:
                file.write("Hay demasiados registros con estado 8.")
            print(f"📁 Archivo guardado en: {ruta_archivo}")
            driver.quit()
            print("🚪 Navegador cerrado.")

        if radio_buttons:
            print(f"✅ Se encontraron {len(radio_buttons)} radio button(s).")
            for index in range(len(radio_buttons)): 
                print(f"▶ Procesando radio button {index + 1}/{len(radio_buttons)}")
                
                # Reubicar los radio buttons en cada iteración
                radio_buttons = WebDriverWait(driver, 50).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//input[@type='radio' and @name='grs0_1']"))
                )
                
                radio_button = radio_buttons[index]  # Selecciona el radio button de la lista actualizada
                driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
                
                actions = ActionChains(driver)
                actions.move_to_element(radio_button).double_click().perform()
                print("🖱️ Doble clic en el radio button realizado.")
                time.sleep(3)

                input_nit = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "C0_36"))
                )

                input_nit.clear()
                time.sleep(2)
                print("✅ Se borró el contenido del input NIT Suscriptor.")

                boton_ok = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.ID, "hc_OK"))
                )
                time.sleep(1) 
                actions.move_to_element(boton_ok).double_click().perform()
                print("🖱️ Doble clic en el botón OK realizado.")
                time.sleep(2)

            print("✅ Se procesaron todos los radio buttons correctamente.")
        else:
            print("⚠️ No se encontraron radio buttons.")
            navigate_home(driver)
        
        time.sleep(3)

        boton_buscar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "hc_Find"))
        )
        boton_buscar.click()

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "JSSelectGrid"))
        )
        time.sleep(3)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        navigate_home(driver)

    finally:
        print("🔄 Proceso de revisión de hechos económicos finalizado.")


#--------------------------------------------------------------------------------------------

def revision_comprobante(driver):

    # Volver al iframe principal
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")

    # Ingresar user en el input de ID usuario
    id_input = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='qbeRow0_1']/td[9]/div/nobr/input"))
    )
    id_input.click()
    id_input.clear()
    id_input.send_keys(USER)

    time.sleep(1)

    boton_buscar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "hc_Find"))
        )
    boton_buscar.click()
    time.sleep(7)
    



