# test_cp03_validacion_correo.py
# CP03 - Validacion de formato de correo electronico invalido.

import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.helpers import (
    llenar_campo,
    hacer_submit,
    obtener_errores_campo,
)

# El mensaje JS dice: "Ingresa un correo valido (ej: usuario@correo.com)."
FRAGMENTO_ERROR_CORREO = "ingresa"


def test_cp03_correo_invalido(driver):
    """
    DADO un correo sin el simbolo @ (ej. correo_invalido),
    CUANDO se hace submit con nombre y contrasena validos,
    ENTONCES debe mostrarse un error de formato en el campo correo.
    """
    try:
        llenar_campo(driver, "nombre",     "Test Usuario")
        llenar_campo(driver, "correo",     "correo_invalido")
        llenar_campo(driver, "contrasena", "Valida123!")
        hacer_submit(driver)

        error = obtener_errores_campo(driver, "correo")
        assert error.strip() != "", "Se esperaba un error en correo pero el campo esta limpio."
        assert FRAGMENTO_ERROR_CORREO in error.lower(), (
            f"Error esperado '{FRAGMENTO_ERROR_CORREO}' no encontrado. Obtenido: '{error}'"
        )

    except TimeoutException as exc:
        pytest.fail(f"CP03 fallo por timeout: {exc}")
    except (AssertionError, NoSuchElementException):
        raise
    except Exception as exc:
        pytest.fail(f"CP03 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
