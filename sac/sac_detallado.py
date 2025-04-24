import sys
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from ejecutar_jde import ejecutar_main_jde
from config_sac import WEBSITE_SAC, DRIVER_PATH
from login_sac import login_sac
from captura import capturar_output
def ejecutar_sac_detallado(fecha, fase):
   """Ejecuta el proceso SAC detallado para una fase específica"""
   start_time = time.time()
   print(f"Fecha seleccionada: {fecha}")
   print(f"Fase seleccionada: {fase}")
   captura = capturar_output()
   driver = None
   resultado = ""
   try:
       # Configuración del driver con opciones para suprimir logs no esenciales
       service = Service(executable_path=DRIVER_PATH)
       options = webdriver.ChromeOptions()
       options.add_experimental_option('excludeSwitches', ['enable-logging'])
       options.add_argument('--log-level=3')
       driver = webdriver.Chrome(service=service, options=options)
       driver.maximize_window()
       driver.get(WEBSITE_SAC)
       # Login al sistema
       login_sac(driver)
       time.sleep(3)
       print("#-------- SAC PROCESS OUTPUTS --------")
       # Navegación al módulo de procesos
       WebDriverWait(driver, 30).until(
           EC.element_to_be_clickable((By.ID, "cphContenedorMenuSuperior_Menu_lbl10332"))
       ).click()
       WebDriverWait(driver, 30).until(
           EC.presence_of_element_located((By.ID, "cphContenedorMenuSuperior_Menu_lbt10333"))
       )
       procesos_element = driver.find_element(By.ID, "cphContenedorMenuSuperior_Menu_lbl10341")
       ActionChains(driver).move_to_element(procesos_element).perform()
       # Clic en Administrativos
       WebDriverWait(driver, 30).until(
           EC.element_to_be_clickable((By.ID, "cphContenedorMenuSuperior_Menu_lbt10342"))
       ).click()
       print("Navegación hasta procesos administrativos completada con éxito.")
       # Ejecutar fase seleccionada
       if fase == '1':
           resultado = ejecutar_fase(driver, fecha, fase, "Facturación", 2, 3,
                                  "divDialogMessage2", "btnCerrarModal2",
                                  "divDialogMessage1", "btnCerrarModal1")
       elif fase == '2':
           resultado = ejecutar_fase(driver, fecha, fase, "Autoconsumos", 2, 3,
                                  "divDialogMessage2", "btnCerrarModal2",
                                  "divDialogMessage1", "btnCerrarModal1")
       elif fase == '3':
           resultado = ejecutar_fase(driver, fecha, fase, "Ajustes", 2, 3,
                                  "divDialogMessage2", "btnCerrarModal2",
                                  "divDialogMessage1", "btnCerrarModal1")
       elif fase == '4':
           resultado = ejecutar_fase(driver, fecha, fase, "Recaudos", 1, 6,
                                  "divDialogMessage2", "btnCerrarModal2",
                                  "divDialogMessage1", "btnCerrarModal1")
       elif fase == '5':
           resultado = ejecutar_fase(driver, fecha, fase, "Castigo", 1, 4,
                                  "divDialogMessage2", "btnCerrarModal2",
                                  "divDialogMessage1", "btnCerrarModal1")
       else:
           raise ValueError(f"Fase inválida: {fase}")
       # Mostrar resultados
       mostrar_resultados(driver)
       # Cerrar sesión
       cerrar_sesion(driver)
       # Guardar resultados
       nombre_archivo = guardar_resultados(fecha, captura, start_time, fase)
       return True, nombre_archivo
   except Exception as e:
       error_msg = f"Error durante la ejecución: {str(e)}"
       print(error_msg)
       if driver:
           driver.quit()
       return False, error_msg
   finally:
       if driver:
           driver.quit()
def ejecutar_fase(driver, fecha, fase, nombre_fase, pagina, fila, modal1, boton1, modal2, boton2):
   """Ejecuta una fase específica del proceso SAC"""
   print(f"\nIniciando fase {fase} - {nombre_fase}")
   # Navegar a la página correcta
   if pagina > 1:
       WebDriverWait(driver, 30).until(
           EC.element_to_be_clickable((By.CSS_SELECTOR,
               f"#ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes a[href*='Page${pagina}']"))
       ).click()
       time.sleep(2)
   # Seleccionar proceso
   WebDriverWait(driver, 30).until(
       EC.element_to_be_clickable((By.CSS_SELECTOR,
           f"#ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvReportes > tbody > tr:nth-child({fila}) > td:nth-child(1) > a > span.fa-play-circle-o"))
   ).click()
   time.sleep(2)
   # Obtener descripción
   descripcion = WebDriverWait(driver, 30).until(
       EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion"))
   ).text
   print(descripcion)
   # Ingresar parámetros
   input_fecha = WebDriverWait(driver, 30).until(
       EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0"))
   )
   input_fecha.clear()
   input_fecha.send_keys(fecha)
   input_fase = WebDriverWait(driver, 30).until(
       EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1"))
   )
   input_fase.clear()
   input_fase.send_keys(fase)
   # Ejecutar
   WebDriverWait(driver, 30).until(
       EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_LbtGenerar"))
   ).click()
   # Manejar modales
   manejar_modales(driver, modal1, boton1, modal2, boton2)
   mensaje_exito = f"Se ha generado '{nombre_fase}' correctamente"
   print(mensaje_exito)
   return mensaje_exito
def manejar_modales(driver, modal1, boton1, modal2, boton2):
   """Maneja los cuadros de diálogo modales después de ejecutar una fase"""
   try:
       WebDriverWait(driver, 60).until(
           EC.presence_of_element_located((By.ID, modal1))
       )
       WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.ID, boton1))
       ).click()
       WebDriverWait(driver, 60).until(
           EC.presence_of_element_located((By.ID, modal2))
       )
       WebDriverWait(driver, 10).until(
           EC.element_to_be_clickable((By.ID, boton2))
       ).click()
   except Exception as e:
       print(f"Advertencia al manejar modales: {str(e)}")
def mostrar_resultados(driver):
   """Muestra los resultados de la ejecución"""
   print("\n#----- RESULTADOS -----")
   mensaje_ids = {
       '1': ["spaTextoMensaje1", "spaTextoMensaje2"],
       '2': ["spaTextoMensaje3", "spaTextoMensaje4"],
       '3': ["spaTextoMensaje5", "spaTextoMensaje6"],
       '4': ["spaTextoMensaje7", "spaTextoMensaje8"],
       '5': ["spaTextoMensaje9", "spaTextoMensaje10"]
   }
   try:
       div_mensajes = WebDriverWait(driver, 30).until(
           EC.presence_of_element_located((By.ID, "divMensajes"))
       )
       for fase, ids in mensaje_ids.items():
           for idx, mensaje_id in enumerate(ids, start=1):
               try:
                   mensaje = div_mensajes.find_element(By.ID, mensaje_id)
                   texto = mensaje.get_attribute('innerText').strip()
                   if texto:
                       print(f"{texto} en la fase {fase}")
               except:
                   continue
   except Exception as e:
       print(f"Error al obtener mensajes: {str(e)}")
def cerrar_sesion(driver):
   """Cierra la sesión en SAC"""
   print("\nCerrando sesión en SAC")
   time.sleep(3)
   try:
       logout_button = WebDriverWait(driver, 30).until(
           EC.presence_of_element_located((By.ID, "btnSalir"))
       )
       driver.execute_script("arguments[0].scrollIntoView(true);", logout_button)
       WebDriverWait(driver, 30).until(
           EC.element_to_be_clickable((By.ID, "btnSalir"))
       ).click()
       time.sleep(2)
   except Exception as e:
       print(f"Error al cerrar sesión: {str(e)}")
def guardar_resultados(fecha, captura, start_time, fase):
   """Guarda los resultados en un archivo de texto"""
   # Calcular tiempo de ejecución
   end_time = time.time()
   execution_time = end_time - start_time
   minutes = int(execution_time // 60)
   seconds = int(execution_time % 60)
   formatted_time = f"{minutes}min {seconds}s"
   print(f"\nTiempo total de ejecución: {formatted_time}")
   # Generar nombre de archivo
   fecha_limpia = fecha.replace("/", "")
   random_number = random.randint(1000, 9999)
   nombre_archivo = f"sac_detallado_{fecha_limpia}_{random_number}.txt"
   # Restaurar salida estándar
   sys.stdout = sys.__stdout__
   sys.stderr = sys.__stderr__
   # Guardar resultados
   with open(nombre_archivo, "w", encoding="utf-8") as f:
       f.write(f"Fecha de ejecución: {fecha}\n")
       f.write(f"Fase ejecutada: {fase}\n")
       f.write(f"ID único: {random_number}\n")
       f.write(f"Tiempo de ejecución: {formatted_time}\n\n")
       f.write(captura.texto)
   print(f"Resumen guardado en: {nombre_archivo}")
   print("Proceso SAC completado exitosamente")
   return nombre_archivo