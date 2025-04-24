# C:\Users\vgaleanc\Downloads\automate-py

import sys
import tkinter as tk
import random
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from ejecutar_jde import ejecutar_main_jde
from config_sac import WEBSITE_SAC, DRIVER_PATH
from login_sac import login_sac
import time
from captura import capturar_output
import threading

#------------ HASTA AQUÍ EL INICIO DE SESIÓN EN SAC ----------------
def ejecutar_sac_process(fecha):
    start_time = time.time() 
    print(f"Fecha seleccionada: {fecha}")
    captura = capturar_output()
    
    # Configuración del driver
    service = Service(executable_path=DRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.get(WEBSITE_SAC)
    
    login_sac(driver)

    time.sleep(15)
    print("#--------  SAC PROCESS OUTPUTS  --------")
    WebDriverWait(driver, 150).until(EC.element_to_be_clickable((By.ID, "cphContenedorMenuSuperior_Menu_lbl10332"))).click()
    WebDriverWait(driver, 150).until(EC.presence_of_element_located((By.ID, "cphContenedorMenuSuperior_Menu_lbt10333")))
    procesos_element = driver.find_element(By.ID, "cphContenedorMenuSuperior_Menu_lbl10341")
    ActionChains(driver).move_to_element(procesos_element).perform()
    # Esperar a que el submenú de "Administrativos" aparezca
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "cphContenedorMenuSuperior_Menu_lbt10342")))
    administrativos_element = driver.find_element(By.ID, "cphContenedorMenuSuperior_Menu_lbt10342")
    administrativos_element.click()
    time.sleep(5)

    print("Navegación hasta procesos administrativos completada con éxito.")

    # Encuentra la segunda página de la tabla Procesos y Reportes y espera hasta que sea visibe
    segundaTablaProcesos = WebDriverWait(driver, 150).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes a[href*='Page$2']"
        ))
    )

    segundaTablaProcesos.click()
    time.sleep(7)

    #----- Inicio generar interfaz 1 -----

    # Espera a que la nueva página cargue: puede ser por la aparición del ícono "Seleccionar"
    faseVentas = WebDriverWait(driver, 150).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "#ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes > tbody > tr:nth-child(3) > td:nth-child(1) > a > span.fa-play-circle-o"
        ))
    )
    faseVentas.click()
    time.sleep(3)
    des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
    print(des_rec)
    input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
    input_fecha_param.click()
    input_fecha_param.send_keys(fecha)

    driver.implicitly_wait(80)
    input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
    input_fase_param.clear()
    input_fase_param.send_keys("1")
    # Ejecutar
    driver.implicitly_wait(80)
    boton_ejecutar = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_LbtGenerar")
    boton_ejecutar.click()
    # Ejecutar y cerrar
    time.sleep(10)
    modal_visible = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage2"))
    )
    boton_cerrar_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal2"))
    )
    boton_cerrar_1.click()
    modal_visible_double = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage1"))
    )
    boton_cerrar_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal1"))
    )
    boton_cerrar_2.click()

    print("Se ha generdado 'Facturación' J1")

    #----- Inicio generar interfaz 2 -----

    # Espera explícita hasta que el enlace esté presente
    faseVentas = WebDriverWait(driver, 80).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes']/tbody/tr[3]/td[1]/a/span"))
    )
    faseVentas.click()
    time.sleep(3)
    des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
    print(des_rec)
    input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
    input_fecha_param.click()
    input_fecha_param.send_keys(fecha)

    driver.implicitly_wait(80)
    input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
    input_fase_param.clear()
    input_fase_param.send_keys("2")
    # Ejecutar
    driver.implicitly_wait(80)
    boton_ejecutar = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_LbtGenerar")
    boton_ejecutar.click()
    time.sleep(10)
    # Ejecutar y cerrar
    modal_visible = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage4"))
    )
    boton_cerrar_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal4"))
    )
    boton_cerrar_1.click()
    modal_visible_double = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage3"))
    )
    boton_cerrar_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal3"))
    )
    boton_cerrar_2.click()

    print("Se ha generdado 'Autoconsumos' DT")

    #----- Inicio generar interfaz 3 -----

    # Espera explícita hasta que el enlace esté presente
    faseVentas = WebDriverWait(driver, 80).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes']/tbody/tr[3]/td[1]/a/span"))
    )
    faseVentas.click()
    time.sleep(3)
    des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
    print(des_rec)
    input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
    input_fecha_param.click()
    input_fecha_param.send_keys(fecha)

    driver.implicitly_wait(80)
    input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
    input_fase_param.clear()
    input_fase_param.send_keys("3")

    driver.implicitly_wait(80)
    boton_ejecutar = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_LbtGenerar")
    boton_ejecutar.click()
    time.sleep(10)
    # Ejecutar y cerrar
    modal_visible = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage6"))
    )
    boton_cerrar_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal6"))
    )
    boton_cerrar_1.click()
    modal_visible_double = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage5"))
    )
    boton_cerrar_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal5"))
    )
    boton_cerrar_2.click()

    print("Se ha generdado 'Ajustes' DY")

    #----- Inicio generar interfaz 4 -----

    # Encuentra la primera página de la tabla Procesos y Reportes
    primeraTablaProcesos = driver.find_element(By.XPATH, "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes']/tbody/tr[4]/td/table/tbody/tr/td[1]/a")
    primeraTablaProcesos.click()
    time.sleep(3)

    # Espera explícita hasta que el enlace esté presente
    faseRecaudos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes']/tbody/tr[6]/td[1]/a/span"))
    )
    faseRecaudos.click()
    time.sleep(3)
    des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
    print(des_rec)

    input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
    input_fecha_param.click()
    input_fecha_param.send_keys(fecha)

    driver.implicitly_wait(80)
    input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
    input_fase_param.clear()
    input_fase_param.send_keys("4")

    driver.implicitly_wait(80)
    boton_ejecutar = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_LbtGenerar")
    boton_ejecutar.click()
    time.sleep(15)
    # Ejecutar y cerrar
    modal_visible = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage8"))
    )
    boton_cerrar_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal8"))
    )
    boton_cerrar_1.click()
    modal_visible_double = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage7"))
    )
    boton_cerrar_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal7"))
    )
    boton_cerrar_2.click()

    print("Se ha generdado 'Recaudos' J1")

    #----- Inicio generar interfaz 5 -----

    # Espera explícita hasta que el enlace esté presente
    faseCastigo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes']/tbody/tr[4]/td[1]/a/span"))
    )
    faseCastigo.click()
    time.sleep(3)
    des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
    print(des_rec)
    input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
    input_fecha_param.click()
    input_fecha_param.send_keys(fecha)

    driver.implicitly_wait(10)
    input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
    input_fase_param.clear()
    input_fase_param.send_keys("5")

    driver.implicitly_wait(10)
    boton_ejecutar = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_LbtGenerar")
    boton_ejecutar.click()
    time.sleep(15)
    # Ejecutar y cerrar
    modal_visible = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage10"))
    )
    boton_cerrar_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal10"))
    )
    boton_cerrar_1.click()
    modal_visible_double = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "divDialogMessage9"))
    )
    boton_cerrar_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnCerrarModal9"))
    )
    boton_cerrar_2.click()

    print("Se ha generdado 'Castigo' DX")

    #--------------------------------------
    print("\n#----- RESULTADOS run sac_process.py")

    mensaje_ids = {
        1: ["spaTextoMensaje1", "spaTextoMensaje2"],
        2: ["spaTextoMensaje3", "spaTextoMensaje4"],
        3: ["spaTextoMensaje5", "spaTextoMensaje6"],
        4: ["spaTextoMensaje7", "spaTextoMensaje8"],
        5: ["spaTextoMensaje9", "spaTextoMensaje10"]
    }

    div_mensajes = driver.find_element(By.ID, "divMensajes")

        # Iterar sobre las fases y sus mensajes
    for fase, ids in mensaje_ids.items():
        for idx, mensaje_id in enumerate(ids, start=1):
            try:
                mensaje_elemento = div_mensajes.find_element(By.ID, mensaje_id)
                mensaje_texto = mensaje_elemento.get_attribute('innerText').strip()
                if mensaje_texto:
                    print(f"{mensaje_texto} en la fase {fase}")
                else:
                    print(f"Fase {fase}: [Mensaje vacío o no disponible]")
            except Exception as e:
                print(f"Error al obtener mensaje {idx} para la fase {fase}: {e}")

    #--------------------------------------


    print("Cerrar sesión en SAC")
    time.sleep(5)
    # Esperar hasta que el botón esté presente
    logout_button = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.ID, "btnSalir")))
    driver.execute_script("arguments[0].scrollIntoView(true);", logout_button)
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "btnSalir"))).click()

    # Medir tiempo de ejecución
    end_time = time.time()
    execution_time = end_time - start_time

    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    formatted_time = f"{minutes}min {seconds}s"

    print(f"Tiempo total de ejecución: {execution_time:.2f} segundos")
    print(formatted_time)

    #----- IMPRIMIR RESULTADOS GENERACIÓN DE INTERFACES -----

    fecha_limpia = fecha.replace("/", "")
    random_number = random.randint(1000, 9999)

    # Crear el nombre del archivo
    nombre_archivo = f"sac_process_console{fecha_limpia}{random_number}.txt"

    # Restaurar la salida estándar antes de escribir en el archivo
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__  # Restaurar stderr también

    # Guardar la salida capturada en un archivo
    with open(nombre_archivo, "w", encoding="utf-8") as file_txt:
        file_txt.write(f"Fecha de ejecución: {fecha}\n")
        file_txt.write(f"ID único: {random_number}\n\n")
        file_txt.write(captura.texto)  # Escribir el contenido capturado

    time.sleep(2)
    print(f"Resumen guardado en: {nombre_archivo}")
    print("Cerrando el navegador...")
    driver.quit()
    ejecutar_main_jde()