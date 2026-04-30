# test_cp01_registro_exitoso.py
# CP01 - Registro exitoso con datos validos.

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from utils.helpers import (
    enviar_formulario,
    verificar_texto_en_alerta,
    esperar_boton_habilitado,
)


def test_cp01_registro_exitoso(driver):
    """
    DADO un formulario vacio,
    CUANDO se ingresan nombre, correo y contrasena validos y se hace submit,
    ENTONCES el alert-box debe contener 'Bienvenido' y el formulario se limpia.
    """
    try:
        enviar_formulario(
            driver,
            nombre="Jose Garcia",
            correo="jose.garcia.cp01@test.com",
            contrasena="Fjkig546*",
        )

        verificar_texto_en_alerta(driver, "Bienvenido", timeout=12)

        esperar_boton_habilitado(driver)
        campo_nombre = driver.find_element(By.ID, "nombre")
        assert campo_nombre.get_attribute("value") == "", (
            "El campo nombre deberia estar vacio tras el registro exitoso."
        )

    except TimeoutException as exc:
        pytest.fail(f"CP01 fallo por timeout: {exc}")
    except AssertionError:
        raise
    except Exception as exc:
        pytest.fail(f"CP01 fallo con error inesperado: {exc}")


if __name__ == "__main__":
    pytest.main(["-v", __file__])
