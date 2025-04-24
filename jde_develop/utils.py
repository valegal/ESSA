import time

def take_screenshot(driver, filename="screenshot.png"):
    """Toma una captura de pantalla del estado actual."""
    driver.save_screenshot(filename)
    print(f"Captura de pantalla guardada como {filename}")

def wait_and_print(message, seconds=2):
    """Imprime un mensaje y espera un tiempo especificado."""
    print(message)
    time.sleep(seconds)
