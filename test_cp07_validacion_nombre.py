# test_cp07_validacion_nombre.py
# CP06 - Validacion del campo nombre: longitud y caracteres permitidos.

import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.helpers import (
    llenar_campo,
    hacer_submit,
    obtener_errores_campo,
)


def test_cp07_nombre_invalido(driver):
    """
    DADO un nombre de solo 2 caracteres (Jo), bajo el minimo de 3,
    CUANDO se hace submit con correo y contrasena validos,
    ENTONCES debe mostrarse error que mencione el minimo de caracteres.
    El mensaje JS dice: "Minimo 3 caracteres." — se busca "3 car" para evitar tildes.
    """
    try:
        llenar_campo(driver, "nombre",     "Jo")
        llenar_campo(driver, "correo",     "test.cp07@test.com")
        llenar_campo(driver, "contrasena", "Valida123!")
        hacer_submit(driver)

        error = obtener_errores_campo(driver, "nombre")
        assert error.strip() != "", "Se esperaba error en nombre con 2 caracteres."
        assert "3 car" in error.lower(), (
            f"Se esperaba '3 car' en el error de nombre. Obtenido: '{error}'"
        )

    except TimeoutException as exc:
        pytest.fail(f"CP07 fallo por timeout: {exc}")
    except (AssertionError, NoSuchElementException):
        raise
    except Exception as exc:
        pytest.fail(f"CP07 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
