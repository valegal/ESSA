from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

def login_sac(driver):
    # Esperar a que el selector esté disponible
    WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlDominios")))

    # Seleccionar la opción ESSADIRECTACT
    select_element = driver.find_element(By.ID, "ContentPlaceHolder1_ddlDominios")
    select = Select(select_element)
    select.select_by_value("D_ESSA_DIRECTACT")

    # Esperar a que se recargue el DOM
    WebDriverWait(driver, 300).until(EC.staleness_of(select_element))

    # Esperar a que el input de usuario esté disponible y digitar el Usuario
    WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtUsuario")))
    select_element = driver.find_element(By.ID, "ContentPlaceHolder1_txtUsuario")
    input_usuario = driver.find_element(By.ID, "ContentPlaceHolder1_txtUsuario")
    input_usuario.send_keys("EMONTANC")

    # Esperar a que el input de contraseña esté presente en el DOM y visible
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.ID, "txtPassword")))
    input_pass = driver.find_element(By.ID, "txtPassword")

    # Hacer clic en el campo de contraseña para asegurarse de que sea activado
    ActionChains(driver).move_to_element(input_pass).click().perform()
    # Enviar la contraseña
    input_pass.send_keys("edmcESSA08**")

    # Desplazarse hasta el botón de login
    login_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnLogin")
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)

    # Luego hacer click
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnLogin"))).click()
