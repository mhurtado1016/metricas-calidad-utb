# conftest.py
# Configuracion compartida de pytest para la suite de pruebas de LuxeStay Hotels.
# Define fixtures reutilizables: driver de Selenium, URL base y opciones del navegador.
# El hook pytest_collection_modifyitems garantiza que los tests se ejecuten
# en orden descendente de criticidad segun la matriz de riesgos del proyecto.

import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


BASE_URL = "http://metricas-calidad-utb-main.s3-website.us-east-2.amazonaws.com"

# Segundos que el navegador permanece abierto tras finalizar cada test,
# para que el resultado sea visible antes de cerrarse.
PAUSA_CIERRE = 4


def crear_opciones_chrome(headless=False):
    """
    Crea y retorna las opciones de Chrome para el WebDriver.

    Args:
        headless: Si es True ejecuta el navegador en modo sin interfaz grafica.

    Returns:
        Objeto Options configurado.
    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    if headless:
        options.add_argument("--headless=new")
    return options


# Orden de ejecucion por nivel de criticidad (mayor riesgo primero).
# Riesgo = Probabilidad x Impacto segun matriz de riesgos del proyecto.
ORDEN_CRITICIDAD = [
    "test_cp01_registro_exitoso",    # Critico  | Riesgo 25
    "test_cp02_campos_vacios",       # Critico  | Riesgo 25
    "test_cp03_validacion_correo",   # Alto     | Riesgo 20
    "test_cp06_correo_duplicado",    # Alto     | Riesgo 20
    "test_cp05_seguridad_xss",       # Alto     | Riesgo 15
    "test_cp04_validacion_password", # Medio    | Riesgo 12
    "test_cp07_validacion_nombre",   # Bajo     | Riesgo  6
]


def pytest_collection_modifyitems(items):
    """
    Hook de pytest que reordena los tests recolectados segun ORDEN_CRITICIDAD.
    Los tests cuyo modulo no aparece en la lista se ubican al final.
    """
    def prioridad(item):
        nombre_modulo = item.module.__name__
        try:
            return ORDEN_CRITICIDAD.index(nombre_modulo)
        except ValueError:
            return len(ORDEN_CRITICIDAD)

    items.sort(key=prioridad)


@pytest.fixture(scope="function")
def driver():
    """
    Fixture que provee un WebDriver de Chrome para cada funcion de prueba.
    Navega automaticamente a BASE_URL antes de entregar el driver.
    Espera PAUSA_CIERRE segundos tras el test para que el resultado sea legible,
    luego cierra el navegador.

    Scope: function -> cada test recibe un navegador fresco y limpio.
    """
    options = crear_opciones_chrome(headless=False)
    drv = webdriver.Chrome(options=options)
    drv.get(BASE_URL)
    yield drv
    time.sleep(PAUSA_CIERRE)
    drv.quit()


@pytest.fixture(scope="function")
def driver_headless():
    """
    Variante headless del fixture driver, util para entornos de integracion continua.
    No aplica pausa de cierre ya que no hay ventana visible.
    """
    options = crear_opciones_chrome(headless=True)
    drv = webdriver.Chrome(options=options)
    drv.get(BASE_URL)
    yield drv
    drv.quit()
