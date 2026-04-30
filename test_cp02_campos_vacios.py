# test_cp02_campos_vacios.py
# CP02 - Validacion de campos vacios / obligatoriedad.

import pytest
from selenium.common.exceptions import TimeoutException

from utils.helpers import (
    hacer_submit,
    verificar_texto_en_alerta,
)


def test_cp02_campos_vacios(driver):
    """
    DADO un formulario completamente vacio,
    CUANDO se hace clic en submit,
    ENTONCES el alert-box debe indicar que hay errores que corregir.
    """
    try:
        hacer_submit(driver)
        verificar_texto_en_alerta(driver, "corrige", timeout=5)

    except TimeoutException as exc:
        pytest.fail(f"CP02 fallo por timeout: {exc}")
    except AssertionError:
        raise
    except Exception as exc:
        pytest.fail(f"CP02 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
