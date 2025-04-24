from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from navigation import switch_to_iframe
from selenium.webdriver.support.ui import Select
from config import USER

import time

#==================================================================================================

def paso_al_f0911(driver, campo_from_val, campo_to_val):
    # Volver al iframe principal
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")

    # Hacer tres clics en el input
    input_element = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='G0_1_R0']/td[1]/div/input"))
    )
    actions = ActionChains(driver)
    for _ in range(3):
        actions.click(input_element)
    actions.perform()

    # Click en checkbox
    checkbox = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "C0_23"))
    )
    checkbox.click()
    time.sleep(1)

    # Click en botón de envío
    send_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "divC0_30"))
    )
    send_button.click()
    time.sleep(3)


    # SELECCIONAR EL USUARIO

    # Selección en LeftOperand3
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "LeftOperand3")))
    select_element = driver.find_element(By.ID, "LeftOperand3")
    driver.execute_script("arguments[0].scrollIntoView(true);", select_element)
    select = Select(select_element)
    try:
        select.select_by_visible_text("IED - Nº de ID del usuario (F0911Z1) (EDUS) [BC]")
    except StaleElementReferenceException:
        time.sleep(1)
        select_element = driver.find_element(By.ID, "LeftOperand3")
        select = Select(select_element)
        select.select_by_visible_text("IED - Nº de ID del usuario (F0911Z1) (EDUS) [BC]")
    time.sleep(1)

    # Selección en Comparison3
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "Comparison3")))
    select_element = driver.find_element(By.ID, "Comparison3")
    select = Select(select_element)
    try:
        select.select_by_visible_text("es igual que")
    except StaleElementReferenceException:
        time.sleep(1)
        select_element = driver.find_element(By.ID, "Comparison3")
        select = Select(select_element)
        select.select_by_visible_text("es igual que")
    time.sleep(1)

    # Selección en RightOperand3
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "RightOperand3")))
    select_element = driver.find_element(By.ID, "RightOperand3")
    select = Select(select_element)
    try:
        select.select_by_visible_text("Literal")
    except StaleElementReferenceException:
        time.sleep(1)
        select_element = driver.find_element(By.ID, "RightOperand3")
        select = Select(select_element)
        select.select_by_visible_text("Literal")
    time.sleep(3)

    # Campo "LITtf"
    campo_from = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "LITtf"))
    )
    campo_from.clear()
    campo_from.send_keys(USER)
    print("✔ Texto EMONTANC escrito en 'LITtf'")
    time.sleep(1)

    # Click en botón OK
    boton_ok = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hc_Select"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", boton_ok)
    boton_ok.click()

    time.sleep(5)

    # SELECCIONAR LOS BATCH DE AGRUPACIÓN

    # Selección en LeftOperand3
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "LeftOperand4")))
    select_element = driver.find_element(By.ID, "LeftOperand4")
    driver.execute_script("arguments[0].scrollIntoView(true);", select_element)
    select = Select(select_element)
    try:
        select.select_by_visible_text("IED - Número de Batch (F0911Z1) (EDBT) [BC]")
    except StaleElementReferenceException:
        time.sleep(1)
        select_element = driver.find_element(By.ID, "LeftOperand4")
        select = Select(select_element)
        select.select_by_visible_text("IED - Número de Batch (F0911Z1) (EDBT) [BC]")
    time.sleep(1)

    # Selección en Comparison3
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "Comparison4")))
    select_element = driver.find_element(By.ID, "Comparison4")
    select = Select(select_element)
    try:
        select.select_by_visible_text("es igual que")
    except StaleElementReferenceException:
        time.sleep(1)
        select_element = driver.find_element(By.ID, "Comparison4")
        select = Select(select_element)
        select.select_by_visible_text("es igual que")
    time.sleep(1)

    # Selección en RightOperand3
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "RightOperand4")))
    select_element = driver.find_element(By.ID, "RightOperand4")
    select = Select(select_element)
    try:
        select.select_by_visible_text("Literal")
    except StaleElementReferenceException:
        time.sleep(1)
        select_element = driver.find_element(By.ID, "RightOperand4")
        select = Select(select_element)
        select.select_by_visible_text("Literal")
    time.sleep(3)

    # Click en la pestaña "Rango de valores"
    rango_pes = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='modelessTabHeaders']//a[contains(text(), 'Rango de valores')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", rango_pes)
    rango_pes.click()
    time.sleep(3)

    # Campo "From"
    campo_from = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "LITtfFrom"))
    )
    campo_from.clear()
    campo_from.send_keys(campo_from_val)
    print(f"✔ Número {campo_from_val} escrito en 'EtfFrom'")

    # Campo "To"
    campo_to = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "LITtfTo"))
    )
    campo_to.clear()
    campo_to.send_keys(campo_to_val)
    print(f"✔ Número {campo_to_val} escrito en 'EtfTo'")
    time.sleep(3)

    # Click en botón OK
    boton_ok = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hc_Select"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", boton_ok)
    boton_ok.click()
    time.sleep(3)
    print("✔ Botón 'OK' clickeado")
    time.sleep(1)


    # Click2 en botón OK
    boton_ok2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hc_Select"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", boton_ok2)
    boton_ok2.click()
    time.sleep(3)

    # Click en botón hc
    boton_hc = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hc_Select"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", boton_hc)
    boton_hc.click()
    time.sleep(3)

    # Click en botón ok
    boton_can = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hc_OK"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", boton_can)
    boton_can.click()
    time.sleep(3)

     # Click en botón SALIR
    boton_salir = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "hc_Close"))
    )
    driver.execute_script("arguments[0].scrollIntoView();", boton_salir)
    boton_salir.click()
    time.sleep(3)


#==================================================================================================