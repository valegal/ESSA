import time
import openpyxl
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from navigation import switch_to_iframe, navigate_home
from selenium.webdriver.common.keys import Keys
from config import fecha_con, EXCEL_PATH
from login import detener_proceso

#---------------------------------------------------------

def update_excel_with_lotes(res_carga):
    # Ruta del archivo Excel
    excel_path = EXCEL_PATH
    
    # Cargar el archivo Excel
    wb = openpyxl.load_workbook(excel_path)
    
    # Obtener el día del mes desde fecha_con
    dia = int(fecha_con[-2:])  # Extrae los últimos dos caracteres como día
    celda_destino = f"B{7 + dia}"  # Calcula la celda destino (B8 es el día 1, B9 el día 2...)
    
    for index in range(1, len(res_carga) // 2 + 1):
        nlote = res_carga.get(f'nlote{index}')
        faselote = res_carga.get(f'faselote{index}')
        
        if nlote and faselote:
            hoja_nombre = f"{faselote}-"
            if faselote == '1':
                hoja_nombre += "FACTURACIÓN"
            elif faselote == '2':
                hoja_nombre += "AUTOCONSUMOS"
            elif faselote == '3':
                hoja_nombre += "AJUSTES"
            elif faselote == '4':
                hoja_nombre += "RECAUDOS"
            elif faselote == '5':
                hoja_nombre += "CASTIGO"
            else:
                continue  # Si no es una hoja esperada, continuar con el siguiente
            
            try:
                hoja = wb[hoja_nombre]
                hoja[celda_destino] = nlote  # Escribir el número de lote en la celda correspondiente
            except KeyError:
                print(f"⚠️ No se encontró la hoja {hoja_nombre} en el archivo Excel.")
    
    # Guardar los cambios en el archivo
    wb.save(excel_path)
    wb.close()
    print("✅ Archivo Excel actualizado correctamente.")

#---------------------------------------------------------

def verify_control_archivos(driver):
    driver.switch_to.default_content()
    switch_to_iframe(driver, "e1menuAppIframe")
    
    # Buscar y llenar el input de fecha contable
    input_fecha_contable = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='C0_18']"))
    )
    input_fecha_contable.click()
    input_fecha_contable.clear()
    time.sleep(1)
    
    # Eliminar cualquier carácter existente antes de escribir
    input_fecha_contable.send_keys(Keys.BACKSPACE * 10)
    time.sleep(1)
    
    # Asegurar que fecha_con_lib es una cadena
    fecha_str = str(fecha_con)
    
    # Escribir la fecha carácter por carácter
    for char in fecha_str:
        input_fecha_contable.send_keys(char)
        time.sleep(0.2)  # Pequeña pausa entre caracteres
    
    time.sleep(1)

    # Buscar y hacer clic en el botón de búsqueda
    boton_buscar = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "hc_Find"))
    )
    boton_buscar.click()
    
    # Esperar a que los resultados carguen
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "JSSelectGrid"))
    )
    time.sleep(5)

    # Buscar todas las filas de la tabla
    filas = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tr[starts-with(@id, 'G0_1_R')]"))
    )
    
    # Inicializar variables dinámicas
    res_carga = {}
    
    for index, fila in enumerate(filas):
        try:
            # Extraer número de lote (columna 6)
            nlote_element = fila.find_element(By.XPATH, ".//td[6]/div")
            nlote_value = nlote_element.text.replace(",", "").strip()
            
            # Extraer fase de lote (columna 0)
            faselote_element = fila.find_element(By.XPATH, ".//td[2]/div")
            faselote_value = faselote_element.text.strip()
            
            # Asignar valores a variables dinámicas
            res_carga[f'nlote{index+1}'] = nlote_value
            res_carga[f'faselote{index+1}'] = faselote_value
            
        except NoSuchElementException:
            print(f"⚠️ No se encontró uno de los valores en la fila {index+1}.")

    # Actulizar Excel con Batch de carga
    update_excel_with_lotes(res_carga)


    # Validación para detener el proceso si no hay faselote 1 o 4
    faselotes = [res_carga[key] for key in res_carga if key.startswith('faselote')]
    if len(faselotes) == 1 or all(f not in ('1', '4') for f in faselotes):
        print("🛑 No se encontraron faselotes 1 o 4. Deteniendo el proceso...")
        detener_proceso(driver)
        return None


    return res_carga

#---------------------------------------------------------
