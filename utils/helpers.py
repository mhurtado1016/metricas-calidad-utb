# utils/helpers.py
# Funciones modulares reutilizables para la suite de pruebas de LuxeStay Hotels.
# Centraliza interacciones comunes con Selenium para evitar duplicacion de codigo.

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    NoAlertPresentException,
    ElementNotInteractableException,
)


# ── Constantes de espera ─────────────────────────────────────────────────────
TIMEOUT_DEFECTO = 10
TIMEOUT_CORTO   = 5
PAUSA_POST_SUBMIT = 1.5


# ─────────────────────────────────────────────────────────────────────────────
# 1. ESPERAS EXPLICITAS
# ─────────────────────────────────────────────────────────────────────────────

def esperar_elemento(driver, by, valor, timeout=TIMEOUT_DEFECTO):
    """
    Espera hasta que el elemento este presente en el DOM.

    Args:
        driver:  WebDriver de Selenium.
        by:      Estrategia de localizacion (By.ID, By.CSS_SELECTOR, etc.).
        valor:   Selector del elemento.
        timeout: Segundos maximos de espera.

    Returns:
        WebElement encontrado.

    Raises:
        TimeoutException: Si el elemento no aparece en el tiempo dado.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, valor))
        )
    except TimeoutException:
        raise TimeoutException(
            f"Elemento '{valor}' no encontrado en {timeout}s usando {by}."
        )


def esperar_visible(driver, by, valor, timeout=TIMEOUT_DEFECTO):
    """
    Espera hasta que el elemento sea visible en la pagina.

    Returns:
        WebElement visible.

    Raises:
        TimeoutException: Si el elemento no se vuelve visible.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, valor))
        )
    except TimeoutException:
        raise TimeoutException(
            f"Elemento '{valor}' no visible en {timeout}s."
        )


def esperar_clickable(driver, by, valor, timeout=TIMEOUT_DEFECTO):
    """
    Espera hasta que el elemento sea clickeable.

    Returns:
        WebElement clickeable.

    Raises:
        TimeoutException: Si el elemento no es clickeable.
    """
    try:
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, valor))
        )
    except TimeoutException:
        raise TimeoutException(
            f"Elemento '{valor}' no es clickeable en {timeout}s."
        )


# ─────────────────────────────────────────────────────────────────────────────
# 2. INTERACCION CON EL FORMULARIO
# ─────────────────────────────────────────────────────────────────────────────

def llenar_campo(driver, campo_id, valor):
    """
    Espera que el campo este presente y escribe el valor dado.

    Args:
        driver:   WebDriver.
        campo_id: ID del elemento input.
        valor:    Texto a escribir.

    Raises:
        TimeoutException: Si el campo no aparece.
        ElementNotInteractableException: Si el campo no es interactuable.
    """
    try:
        campo = esperar_elemento(driver, By.ID, campo_id)
        campo.clear()
        campo.send_keys(valor)
    except ElementNotInteractableException:
        raise ElementNotInteractableException(
            f"El campo '{campo_id}' existe pero no es interactuable."
        )


def llenar_formulario(driver, nombre="", correo="", contrasena=""):
    """
    Rellena los tres campos del formulario de registro.
    Deja un campo vacio si se pasa cadena vacia (no llama send_keys).

    Args:
        driver:     WebDriver.
        nombre:     Valor para el campo nombre.
        correo:     Valor para el campo correo.
        contrasena: Valor para el campo contrasena.
    """
    if nombre:
        llenar_campo(driver, "nombre", nombre)
    if correo:
        llenar_campo(driver, "correo", correo)
    if contrasena:
        llenar_campo(driver, "contrasena", contrasena)


def hacer_submit(driver):
    """
    Localiza el boton de submit y hace clic en el.

    Raises:
        TimeoutException: Si el boton no es clickeable.
    """
    btn = esperar_clickable(driver, By.ID, "submitBtn")
    btn.click()


def enviar_formulario(driver, nombre="", correo="", contrasena=""):
    """
    Funcion de conveniencia: rellena el formulario y hace submit en un solo paso.
    """
    llenar_formulario(driver, nombre, correo, contrasena)
    hacer_submit(driver)


# ─────────────────────────────────────────────────────────────────────────────
# 3. LECTURA DE RESULTADOS
# ─────────────────────────────────────────────────────────────────────────────

def obtener_alerta(driver, timeout=TIMEOUT_DEFECTO):
    """
    Espera y retorna el texto del #alert-box visible.

    Returns:
        Texto del alert-box.

    Raises:
        TimeoutException: Si el alert-box no se muestra.
    """
    caja = esperar_visible(driver, By.ID, "alert-box", timeout)
    return caja.text


def obtener_errores_campo(driver, campo_id):
    """
    Retorna el texto del contenedor de errores de un campo.

    Args:
        campo_id: ID base del campo (ej. 'nombre' -> div id='nombre-errors').

    Returns:
        Texto del contenedor de errores (puede ser cadena vacia si no hay errores).

    Raises:
        NoSuchElementException: Si el contenedor de errores no existe en el DOM.
    """
    try:
        contenedor = driver.find_element(By.ID, f"{campo_id}-errors")
        return contenedor.text
    except NoSuchElementException:
        raise NoSuchElementException(
            f"No se encontro el contenedor de errores '{campo_id}-errors'."
        )


def hay_alerta_js(driver):
    """
    Comprueba si existe un alert nativo de JavaScript activo.

    Returns:
        True si hay un alert JS, False en caso contrario.
    """
    try:
        driver.switch_to.alert
        return True
    except NoAlertPresentException:
        return False


def descartar_alerta_js(driver):
    """Descarta el alert nativo de JS si existe (sin fallar si no hay)."""
    try:
        driver.switch_to.alert.dismiss()
    except NoAlertPresentException:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# 4. ASSERTIONS PERSONALIZADAS
# ─────────────────────────────────────────────────────────────────────────────

def verificar_texto_en_alerta(driver, fragmento, timeout=TIMEOUT_DEFECTO):
    """
    Afirma que el #alert-box contiene el fragmento de texto dado.

    Args:
        driver:    WebDriver.
        fragmento: Subcadena esperada en el texto del alert-box.
        timeout:   Segundos de espera para que aparezca el alert.

    Raises:
        AssertionError: Si el fragmento no esta en el texto del alert-box.
    """
    texto = obtener_alerta(driver, timeout)
    assert fragmento.lower() in texto.lower(), (
        f"Se esperaba '{fragmento}' en el alert-box, pero se obtuvo: '{texto}'"
    )


def verificar_error_en_campo(driver, campo_id, fragmento):
    """
    Afirma que el contenedor de errores de un campo contiene el fragmento dado.

    Args:
        driver:    WebDriver.
        campo_id:  ID base del campo.
        fragmento: Subcadena esperada en el mensaje de error.

    Raises:
        AssertionError: Si el fragmento no esta en el texto de error.
    """
    texto_error = obtener_errores_campo(driver, campo_id)
    assert fragmento.lower() in texto_error.lower(), (
        f"Se esperaba '{fragmento}' en errores de '{campo_id}', "
        f"pero se obtuvo: '{texto_error}'"
    )


def verificar_campo_vacio_errores(driver, campo_id):
    """
    Afirma que el contenedor de errores de un campo NO esta vacio
    (es decir, hay al menos un mensaje de error visible).

    Raises:
        AssertionError: Si no hay errores en el campo.
    """
    texto_error = obtener_errores_campo(driver, campo_id)
    assert texto_error.strip() != "", (
        f"Se esperaba algun error en '{campo_id}', pero el contenedor esta vacio."
    )


def verificar_sin_alerta_js(driver):
    """
    Afirma que NO hay un alert nativo de JavaScript activo.

    Raises:
        AssertionError: Si se detecta un alert JS (posible XSS ejecutado).
    """
    assert not hay_alerta_js(driver), (
        "Se detecto un alert nativo de JavaScript — posible ejecucion de XSS."
    )


# ─────────────────────────────────────────────────────────────────────────────
# 5. UTILIDADES GENERALES
# ─────────────────────────────────────────────────────────────────────────────

def recargar_pagina(driver):
    """Recarga la pagina para obtener un formulario limpio entre sub-pruebas."""
    driver.refresh()
    esperar_elemento(driver, By.ID, "submitBtn")


def esperar_boton_habilitado(driver, timeout=TIMEOUT_DEFECTO):
    """
    Espera hasta que el boton submitBtn no este deshabilitado.
    Util tras el timeout de 1.4 s del registro exitoso.

    Raises:
        TimeoutException: Si el boton no se rehabilita.
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: not d.find_element(By.ID, "submitBtn").get_attribute("disabled")
        )
    except TimeoutException:
        raise TimeoutException("El boton submit no se habilito en el tiempo esperado.")
