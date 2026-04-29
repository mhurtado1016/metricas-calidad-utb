"""
Suite de pruebas automatizadas - Formulario de Registro LuxeStay Hotels
Requisitos:
    pip install selenium webdriver-manager pytest
"""

import time
import pytest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ── Configuración ──────────────────────────────────────────────────────────────
# Path.as_uri() genera file:///ruta/correcta en cualquier PC, Windows o Linux
URL = (Path(__file__).resolve().parent / "registro.html").as_uri()

# Velocidad de escritura en los campos (segundos entre cada carácter)
# 0 = instantáneo | 0.05 = lento y visible | 0.1 = muy lento
VELOCIDAD_ESCRITURA = 0.06

# Pausa visual entre pasos dentro de un test (segundos)
PAUSA_ENTRE_PASOS = 0.8

# Datos de prueba
USUARIO_VALIDO = {
    "nombre":    "María García",
    "correo":    "maria@luxestay.com",
    "password":  "Segura123"
}


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def driver():
    """Instancia única del navegador para toda la sesión de pruebas."""
    opciones = webdriver.ChromeOptions()
    # opciones.add_argument("--headless")   # descomentar para correr sin ventana
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-notifications")

    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones
    )
    d.implicitly_wait(3)
    yield d
    d.quit()


@pytest.fixture(autouse=True)
def abrir_formulario(driver):
    """Recarga el formulario antes de cada test para empezar desde cero."""
    driver.get(URL)
    # Esperar a que el formulario esté listo
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "registerForm"))
    )


# ── Helpers ────────────────────────────────────────────────────────────────────

def escribir_lento(elemento, texto):
    """Escribe carácter a carácter para que sea visible durante la ejecución."""
    for caracter in texto:
        elemento.send_keys(caracter)
        time.sleep(VELOCIDAD_ESCRITURA)


def llenar_formulario(driver, nombre="", correo="", password=""):
    if nombre:
        campo = driver.find_element(By.ID, "nombre")
        campo.click()
        escribir_lento(campo, nombre)
        time.sleep(PAUSA_ENTRE_PASOS)
    if correo:
        campo = driver.find_element(By.ID, "correo")
        campo.click()
        escribir_lento(campo, correo)
        time.sleep(PAUSA_ENTRE_PASOS)
    if password:
        campo = driver.find_element(By.ID, "contrasena")
        campo.click()
        escribir_lento(campo, password)
        time.sleep(PAUSA_ENTRE_PASOS)


def enviar_formulario(driver):
    time.sleep(PAUSA_ENTRE_PASOS)
    driver.find_element(By.ID, "submitBtn").click()


def obtener_clase_campo(driver, field_id):
    return driver.find_element(By.ID, field_id).get_attribute("class")


def obtener_errores_campo(driver, field_id):
    return driver.find_element(By.ID, f"{field_id}-errors").text.strip()


def obtener_alert(driver):
    wait = WebDriverWait(driver, 5)
    alert = wait.until(EC.visibility_of_element_located((By.ID, "alert-box")))
    return alert.text.strip()


def usuarios_en_memoria(driver):
    return driver.execute_script("return window.__usuariosRegistrados;") or []


def registrar_y_esperar(driver, nombre, correo, password):
    """Registra un usuario y espera a que el proceso termine (1.4 s de setTimeout)."""
    llenar_formulario(driver, nombre, correo, password)
    enviar_formulario(driver)
    time.sleep(1.8)


# ══════════════════════════════════════════════════════════════════════════════
# CASOS DE PRUEBA
# ══════════════════════════════════════════════════════════════════════════════

class TestCamposVacios:
    """CP-01 a CP-03 — Validación de campos obligatorios vacíos."""

    def test_cp01_todos_los_campos_vacios(self, driver):
        """CP-01: Enviar el formulario completamente vacío muestra errores en los 3 campos."""
        enviar_formulario(driver)

        assert "error" in obtener_clase_campo(driver, "nombre"),    "Nombre debería marcarse como error"
        assert "error" in obtener_clase_campo(driver, "correo"),    "Correo debería marcarse como error"
        assert "error" in obtener_clase_campo(driver, "contrasena"),"Contraseña debería marcarse como error"

    def test_cp02_solo_nombre_vacio(self, driver):
        """CP-02: Enviar sin nombre muestra error únicamente en ese campo."""
        llenar_formulario(driver, correo="test@correo.com", password="Segura123")
        enviar_formulario(driver)

        assert "error"   in obtener_clase_campo(driver, "nombre")
        assert "success" in obtener_clase_campo(driver, "correo")
        assert "success" in obtener_clase_campo(driver, "contrasena")

    def test_cp03_solo_correo_vacio(self, driver):
        """CP-03: Enviar sin correo muestra error únicamente en ese campo."""
        llenar_formulario(driver, nombre="Juan Pérez", password="Segura123")
        enviar_formulario(driver)

        assert "success" in obtener_clase_campo(driver, "nombre")
        assert "error"   in obtener_clase_campo(driver, "correo")
        assert "success" in obtener_clase_campo(driver, "contrasena")


class TestValidacionNombre:
    """CP-04 a CP-06 — Reglas de validación del campo Nombre."""

    def test_cp04_nombre_muy_corto(self, driver):
        """CP-04: Nombre con menos de 3 caracteres genera error."""
        llenar_formulario(driver, nombre="Jo")
        driver.find_element(By.ID, "nombre").send_keys("\t")  # trigger blur

        assert "error" in obtener_clase_campo(driver, "nombre")
        assert "3 caracteres" in obtener_errores_campo(driver, "nombre")

    def test_cp05_nombre_con_numeros(self, driver):
        """CP-05: Nombre que contiene números genera error."""
        llenar_formulario(driver, nombre="Juan123")
        driver.find_element(By.ID, "nombre").send_keys("\t")

        assert "error" in obtener_clase_campo(driver, "nombre")

    def test_cp06_nombre_valido(self, driver):
        """CP-06: Nombre válido marca el campo como éxito."""
        llenar_formulario(driver, nombre="Ana Martínez")
        driver.find_element(By.ID, "nombre").send_keys("\t")

        assert "success" in obtener_clase_campo(driver, "nombre")


class TestValidacionCorreo:
    """CP-07 a CP-09 — Reglas de validación del campo Correo."""

    def test_cp07_correo_sin_arroba(self, driver):
        """CP-07: Correo sin @ genera error de formato."""
        llenar_formulario(driver, correo="correosinArroba.com")
        driver.find_element(By.ID, "correo").send_keys("\t")

        assert "error" in obtener_clase_campo(driver, "correo")
        assert "válido" in obtener_errores_campo(driver, "correo")

    def test_cp08_correo_sin_dominio(self, driver):
        """CP-08: Correo sin dominio genera error de formato."""
        llenar_formulario(driver, correo="usuario@")
        driver.find_element(By.ID, "correo").send_keys("\t")

        assert "error" in obtener_clase_campo(driver, "correo")

    def test_cp09_correo_valido(self, driver):
        """CP-09: Correo con formato correcto marca el campo como éxito."""
        llenar_formulario(driver, correo="usuario@dominio.com")
        driver.find_element(By.ID, "correo").send_keys("\t")

        assert "success" in obtener_clase_campo(driver, "correo")


class TestValidacionPassword:
    """CP-10 a CP-12 — Reglas de validación del campo Contraseña."""

    def test_cp10_password_muy_corta(self, driver):
        """CP-10: Contraseña con menos de 8 caracteres genera error."""
        llenar_formulario(driver, password="Abc1")
        driver.find_element(By.ID, "contrasena").send_keys("\t")

        assert "error" in obtener_clase_campo(driver, "contrasena")
        assert "8 caracteres" in obtener_errores_campo(driver, "contrasena")

    def test_cp11_password_sin_mayuscula(self, driver):
        """CP-11: Contraseña sin mayúscula genera error."""
        llenar_formulario(driver, password="segura123")
        driver.find_element(By.ID, "contrasena").send_keys("\t")

        assert "error" in obtener_clase_campo(driver, "contrasena")
        assert "mayúscula" in obtener_errores_campo(driver, "contrasena")

    def test_cp12_password_sin_numero(self, driver):
        """CP-12: Contraseña sin número genera error."""
        llenar_formulario(driver, password="SeguraSinNum")
        driver.find_element(By.ID, "contrasena").send_keys("\t")

        assert "error" in obtener_clase_campo(driver, "contrasena")
        assert "número" in obtener_errores_campo(driver, "contrasena")


class TestRegistroCompleto:
    """CP-13 y CP-14 — Flujo de registro exitoso y usuario duplicado."""

    def test_cp13_registro_exitoso(self, driver):
        """CP-13: Datos válidos completan el registro y guardan el usuario en memoria."""
        registrar_y_esperar(
            driver,
            USUARIO_VALIDO["nombre"],
            USUARIO_VALIDO["correo"],
            USUARIO_VALIDO["password"]
        )

        # Mensaje de bienvenida visible
        alert = obtener_alert(driver)
        assert "Bienvenido" in alert, f"Se esperaba mensaje de bienvenida, se obtuvo: '{alert}'"

        # Usuario guardado en memoria del navegador
        registrados = usuarios_en_memoria(driver)
        correos = [u["correo"] for u in registrados]
        assert USUARIO_VALIDO["correo"] in correos, "El correo no quedó guardado en memoria"

    def test_cp14_usuario_ya_existente(self, driver):
        """CP-14: Intentar registrar un correo ya existente muestra error apropiado."""
        # Primero registrar el usuario
        registrar_y_esperar(
            driver,
            USUARIO_VALIDO["nombre"],
            USUARIO_VALIDO["correo"],
            USUARIO_VALIDO["password"]
        )

        # Recargar y volver a intentar con el mismo correo
        # (el fixture autouse recarga la página, así que navegamos de nuevo
        #  pero el estado en memoria persiste porque es la misma sesión del driver)
        driver.get(URL)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "registerForm"))
        )

        llenar_formulario(driver, "Otro Usuario", USUARIO_VALIDO["correo"], "OtraPass9")
        enviar_formulario(driver)

        # El campo correo debe marcarse como error
        assert "error" in obtener_clase_campo(driver, "correo"), \
            "El campo correo debería marcarse como error para usuario duplicado"

        # El alert debe indicar que el correo ya está registrado
        alert = obtener_alert(driver)
        assert "ya tiene una cuenta" in alert, \
            f"Se esperaba mensaje de duplicado, se obtuvo: '{alert}'"


# ── Punto de entrada para ejecutar con: python test_registro.py ────────────────
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
