# test_cp06_correo_duplicado.py
# CP05 - Registro con correo ya existente (correo duplicado).

import time
import pytest
from selenium.common.exceptions import TimeoutException

from utils.helpers import (
    enviar_formulario,
    llenar_campo,
    hacer_submit,
    verificar_texto_en_alerta,
)

ESPERA_REGISTRO_JS = 3


def test_cp06_correo_duplicado(driver):
    """
    DADO que el correo repetido.cp06@test.com ya fue registrado,
    CUANDO se intenta registrar el mismo correo por segunda vez,
    ENTONCES el alert-box debe indicar que el correo ya tiene una cuenta.
    """
    correo = "repetido.cp06@test.com"
    try:
        enviar_formulario(driver, nombre="Usuario Primero", correo=correo, contrasena="Fuerte2024!")
        time.sleep(ESPERA_REGISTRO_JS)

        llenar_campo(driver, "nombre",     "Usuario Segundo")
        llenar_campo(driver, "correo",     correo)
        llenar_campo(driver, "contrasena", "Fuerte2024!")
        hacer_submit(driver)

        verificar_texto_en_alerta(driver, "ya tiene una cuenta", timeout=10)

    except TimeoutException as exc:
        pytest.fail(f"CP06 fallo por timeout: {exc}")
    except AssertionError:
        raise
    except Exception as exc:
        pytest.fail(f"CP06 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
