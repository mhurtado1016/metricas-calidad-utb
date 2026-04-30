# test_cp04_validacion_password.py
# CP04 - Validacion de seguridad de contrasena.

import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.helpers import (
    llenar_campo,
    hacer_submit,
    obtener_errores_campo,
)


def test_cp04_password_insegura(driver):
    """
    DADO una contrasena de solo 3 caracteres (123),
    CUANDO se hace submit con nombre y correo validos,
    ENTONCES debe mostrarse error que mencione el minimo de caracteres.
    El mensaje JS dice: "Minimo 8 caracteres." — se busca "8 car" para evitar tildes.
    """
    try:
        llenar_campo(driver, "nombre",     "Test Usuario")
        llenar_campo(driver, "correo",     "test.cp04@test.com")
        llenar_campo(driver, "contrasena", "123")
        hacer_submit(driver)

        error = obtener_errores_campo(driver, "contrasena")
        assert error.strip() != "", "Se esperaba error en contrasena pero el campo esta limpio."
        assert "8 car" in error.lower(), (
            f"Se esperaba '8 car' en el error de contrasena. Obtenido: '{error}'"
        )

    except TimeoutException as exc:
        pytest.fail(f"CP04 fallo por timeout: {exc}")
    except (AssertionError, NoSuchElementException):
        raise
    except Exception as exc:
        pytest.fail(f"CP04 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
