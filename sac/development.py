# C:\Users\vgaleanc\Downloads\automate-py

import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
from captura import capturar_output
captura = capturar_output()
fecha = "" #(11/03/2025)

# Configuración del driver
website_sac = "https://essa-ws12.essa.com.co:9095/GEN/Vistas/Login/LOGIN_GEN.aspx"
path = r"C:\\Users\\vgaleanc\\Escritorio\\chromedriver\\chromedriver-win64\\chromedriver.exe"

# Inicializar el servicio y el driver
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

# Maximizar la ventana del navegador
driver.maximize_window()

# Abrir la página web
driver.get(website_sac)

# Esperar a que el selector esté disponible
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ddlDominios")))

# Seleccionar la opción ESSADIRECTACT
select_element = driver.find_element(By.ID, "ContentPlaceHolder1_ddlDominios")
select = Select(select_element)
select.select_by_value("D_ESSA_DIRECTACT")

# Esperar a que se recargue el DOM
WebDriverWait(driver, 10).until(EC.staleness_of(select_element))

# Esperar a que el input de usuario esté disponible y digitar el Usuario
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_txtUsuario")))
select_element = driver.find_element(By.ID, "ContentPlaceHolder1_txtUsuario")
input_usuario = driver.find_element(By.ID, "ContentPlaceHolder1_txtUsuario")
input_usuario.send_keys("")

# Esperar a que el input de contraseña esté presente en el DOM y visible
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "txtPassword")))
input_pass = driver.find_element(By.ID, "txtPassword")

# Hacer clic en el campo de contraseña para asegurarse de que sea activado
ActionChains(driver).move_to_element(input_pass).click().perform()
# Enviar la contraseña
input_pass.send_keys("")

# Desplazarse hasta el botón de login
login_button = driver.find_element(By.ID, "ContentPlaceHolder1_btnLogin")
driver.execute_script("arguments[0].scrollIntoView(true);", login_button)

# Luego hacer click
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_btnLogin"))).click()

#------------ HASTA AQUÍ EL INICIO DE SESIÓN EN SAC ----------------

time.sleep(15)
print("#--------  SAC PROCESS OUTPUTS  --------")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "cphContenedorMenuSuperior_Menu_lbl10332"))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cphContenedorMenuSuperior_Menu_lbt10333")))
procesos_element = driver.find_element(By.ID, "cphContenedorMenuSuperior_Menu_lbl10341")
ActionChains(driver).move_to_element(procesos_element).perform()
# Esperar a que el submenú de "Administrativos" aparezca
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cphContenedorMenuSuperior_Menu_lbt10342")))
administrativos_element = driver.find_element(By.ID, "cphContenedorMenuSuperior_Menu_lbt10342")
administrativos_element.click()
time.sleep(5)

print("Navegación hasta procesos administrativos completada con éxito.")

# Encuentra la segunda página de la tabla Procesos y Reportes
segundaTablaProcesos = driver.find_element(By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Page$2')\"]")
segundaTablaProcesos.click()
time.sleep(3)

print("INICIO generar interfaz 1")

# Espera explícita hasta que el enlace esté presente
faseVentas = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Select$1')\"]"))
)
faseVentas.click()
time.sleep(3)
des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
print(f"Ahora estamos en {des_rec}")
input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
input_fecha_param.click()
input_fecha_param.send_keys(fecha)

driver.implicitly_wait(10)
input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
input_fase_param.clear()
input_fase_param.send_keys("1")
# Ejecutar
driver.implicitly_wait(10)
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
print("FIN generar interfaz 1")

print("INICIO generar interfaz 2")

# Espera explícita hasta que el enlace esté presente
faseVentas = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Select$1')\"]"))
)
faseVentas.click()
time.sleep(3)
des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
print(f"Ahora estamos en {des_rec}")
input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
input_fecha_param.click()
input_fecha_param.send_keys(fecha)

driver.implicitly_wait(10)
input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
input_fase_param.clear()
input_fase_param.send_keys("2")
# Ejecutar
driver.implicitly_wait(10)
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

print("FIN generar interfaz 2")

print("INICIO generar interfaz 3")

# Espera explícita hasta que el enlace esté presente
faseVentas = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Select$1')\"]"))
)
faseVentas.click()
time.sleep(3)
des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
print(f"Ahora estamos en {des_rec}")
input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
input_fecha_param.click()
input_fecha_param.send_keys(fecha)

driver.implicitly_wait(10)
input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
input_fase_param.clear()
input_fase_param.send_keys("3")

driver.implicitly_wait(10)
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

print("FIN generar interfaz 3")

print("INICIO generar interfaz 4")

# Encuentra la primera página de la tabla Procesos y Reportes
primeraTablaProcesos = driver.find_element(By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Page$1')\"]")
primeraTablaProcesos.click()
time.sleep(3)

# Espera explícita hasta que el enlace esté presente
faseRecaudos = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Select$4')\"]"))
)
faseRecaudos.click()
time.sleep(3)
des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
print(f"Ahora estamos en {des_rec}")

input_fecha_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_0")
input_fecha_param.click()
input_fecha_param.send_keys(fecha)

driver.implicitly_wait(10)
input_fase_param = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_DgvParametros_TxtValor_1")
input_fase_param.clear()
input_fase_param.send_keys("4")

driver.implicitly_wait(10)
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

print("FIN generar interfaz 4")

print("INICIO generar interfaz 5")

# Espera explícita hasta que el enlace esté presente
faseCastigo = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//a[@href=\"javascript:__doPostBack('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder1$grcGenReportesCtrl$DgvReportes','Select$2')\"]"))
)
faseCastigo.click()
time.sleep(3)
des_rec = driver.find_element(By.ID, "ContentPlaceHolder1_ContentPlaceHolder1_grcGenReportesCtrl_TxtDescripcion").text
print(f"Ahora estamos en {des_rec}")
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

print("FIN generar interfaz 5")

#----- IMPRIMIR RESULTADOS GENERACIÓN DE INTERFACES -----

print("#----- RESULTADOS run sac_process.py")

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
                print(f"{mensaje_texto} en la fase{fase}")
            else:
                print(f"Fase{fase}: [Mensaje vacío o no disponible]")
        except Exception as e:
            print(f"Error al obtener mensaje {idx} para la fase {fase}: {e}")

# Guardar la salida capturada en un archivo
sys.stdout = sys.__stdout__  # Restaurar la salida estándar
with open("sac_process_console.txt", "w") as file_txt:
    file_txt.write(captura.texto)  # Escribir el contenido capturado

# Cerrar el navegador automáticamente
print("Cerrando el navegador...")
driver.quit()

