from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from navigation import navigate_home
from config import WEBSITE_URL_JDE

def login(driver, username, password):
    """Realiza el inicio de sesión en la aplicación."""
    driver.get(WEBSITE_URL_JDE)

    # Localizar y completar el formulario de inicio de sesión
    driver.find_element(By.ID, "User").send_keys(username)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Conexión']").click()

    # Esperar unos segundos para asegurar la carga
    time.sleep(10)

#----------------------------------------------------------------------------

def logout(driver):
        # Volver al contenido principal
    driver.switch_to.default_content()

    # Hacer clic en el menú de usuario
    user_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "userSessionDropdownArrow"))
    )
    user_menu.click()
    time.sleep(2)

    # Hacer clic en "Desconexión"
    logout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signOutLinkDiv"))
    )
    logout_button.click()
    time.sleep(1)

    # Aceptar la alerta de cierre de sesión si aparece
    try:
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert.accept()
    except TimeoutException:
        print("No se encontró alerta de confirmación de cierre de sesión.")

    time.sleep(3)

#----------------------------------------------------------------------------

def recargar_pagina(driver, metodo="f5"):
    """
    Recarga la página en Selenium.

    :param driver: Instancia del WebDriver de Selenium.
    :param metodo: Método de recarga, puede ser "f5" o "ctrl+r".
    """
    if metodo == "f5":
        driver.refresh()  # Método estándar de Selenium
    elif metodo == "ctrl+r":
        driver.find_element("tag name", "body").send_keys(Keys.CONTROL, "r")  # Simula Ctrl + R
    else:
        raise ValueError("Método inválido. Usa 'f5' o 'ctrl+r'.")

    print("🔄 Página recargada")
    time.sleep(3)  # Esperar un poco para evitar problemas de carga

#----------------------------------------------------------------------------

def detener_proceso(driver):

    time.sleep(2)
    navigate_home(driver)
    logout(driver)
    time.sleep(2)
    driver.quit()



