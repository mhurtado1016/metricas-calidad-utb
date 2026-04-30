# test_cp05_seguridad_xss.py
# CP07 - Pruebas de seguridad: inyeccion XSS (Cross-Site Scripting).

import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.helpers import (
    llenar_campo,
    hacer_submit,
    verificar_campo_vacio_errores,
    hay_alerta_js,
    descartar_alerta_js,
)

XSS_SCRIPT_BASICO = "<script>alert(1)</script>"


def test_cp05_xss_en_nombre(driver):
    """
    DADO el payload '<script>alert(1)</script>' en el campo nombre,
    CUANDO se hace submit,
    ENTONCES NO debe ejecutarse ningun alert JS y debe aparecer error en nombre.
    """
    try:
        llenar_campo(driver, "nombre",     XSS_SCRIPT_BASICO)
        llenar_campo(driver, "correo",     "test.xss@test.com")
        llenar_campo(driver, "contrasena", "Segura2024!")
        hacer_submit(driver)

        if hay_alerta_js(driver):
            descartar_alerta_js(driver)
            pytest.fail(
                "XSS ejecutado: se detecto un alert nativo de JavaScript. "
                "El payload no fue sanitizado correctamente."
            )

        verificar_campo_vacio_errores(driver, "nombre")

    except TimeoutException as exc:
        pytest.fail(f"CP05 fallo por timeout: {exc}")
    except (AssertionError, NoSuchElementException):
        raise
    except Exception as exc:
        pytest.fail(f"CP05 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
