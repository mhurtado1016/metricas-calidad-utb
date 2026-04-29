"""
Suite de pruebas automatizadas - Formulario de Registro LuxeStay Hotels
Casos de prueba: CP01 al CP07

Requisitos:
    pip install selenium webdriver-manager pytest
Ejecución:
    python test_registro.py
    pytest test_registro.py -v
"""

import time
import pytest
from pathlib import Path
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ── Configuración ──────────────────────────────────────────────────────────────
URL = (Path(__file__).resolve().parent / "registro.html").as_uri()

VELOCIDAD_ESCRITURA = 0.03
PAUSA_ENTRE_PASOS   = 0.8

# Metadatos de cada caso de prueba para el resumen final
METADATA_CP = {
    "test_cp01_registro_exitoso":    {"id": "CP01", "escenario": "Registro exitoso con datos válidos",        "prioridad": "Alta"},
    "test_cp02_campos_vacios":       {"id": "CP02", "escenario": "Registro con campos vacíos",                "prioridad": "Alta"},
    "test_cp03_correo_invalido":     {"id": "CP03", "escenario": "Registro con correo inválido",              "prioridad": "Alta"},
    "test_cp04_contrasena_insegura": {"id": "CP04", "escenario": "Registro con contraseña insegura",          "prioridad": "Media"},
    "test_cp05_correo_ya_existente": {"id": "CP05", "escenario": "Registro con correo ya existente",          "prioridad": "Alta"},
    "test_cp06_confirmacion_registro":{"id": "CP06", "escenario": "Confirmación de registro por correo",      "prioridad": "Baja"},
    "test_cp07_caracteres_maliciosos":{"id": "CP07", "escenario": "Registro con caracteres maliciosos (XSS)", "prioridad": "Alta"},
}


# ── Hook: captura el resultado de cada test ────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def resultados():
    """Lista compartida que acumula el resultado de cada test."""
    return []


@pytest.fixture(scope="session")
def driver(resultados):
    """Instancia única del navegador. Al cerrar muestra el resumen en pantalla."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--start-maximized")
    opciones.add_argument("--disable-notifications")

    d = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opciones
    )
    d.implicitly_wait(3)

    yield d

    # ── Al terminar todos los tests: mostrar resumen en el navegador ───────
    mostrar_resumen(d, resultados)
    time.sleep(30)   # segundos que el navegador permanece abierto con el resumen
    d.quit()


@pytest.fixture(autouse=True)
def abrir_formulario(driver):
    """Recarga el formulario antes de cada test."""
    driver.get(URL)
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "registerForm"))
    )


@pytest.fixture(autouse=True)
def capturar_resultado(request, resultados):
    """Registra automáticamente si cada test pasó o falló."""
    inicio = time.time()
    yield
    duracion = round(time.time() - inicio, 2)

    nombre_test = request.node.name
    meta = METADATA_CP.get(nombre_test, {
        "id": nombre_test, "escenario": nombre_test, "prioridad": "-"
    })

    paso = True
    mensaje_error = ""
    if hasattr(request.node, "rep_call"):
        paso = not request.node.rep_call.failed
        if not paso and request.node.rep_call.longrepr:
            mensaje_error = str(request.node.rep_call.longrepr).strip().split("\n")[-1]

    resultados.append({
        "id":           meta["id"],
        "escenario":    meta["escenario"],
        "prioridad":    meta["prioridad"],
        "paso":         paso,
        "duracion":     duracion,
        "error":        mensaje_error,
    })


# ── Generador del resumen HTML ─────────────────────────────────────────────────

def mostrar_resumen(driver, resultados):
    """Inyecta una página HTML con el resumen de resultados en el navegador."""
    total   = len(resultados)
    pasaron = sum(1 for r in resultados if r["paso"])
    fallaron = total - pasaron
    porcentaje = round((pasaron / total) * 100) if total else 0
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def fila(r):
        estado_cls  = "pass" if r["paso"] else "fail"
        estado_txt  = "✔ PASÓ" if r["paso"] else "✘ FALLÓ"
        prioridad_cls = r["prioridad"].lower()
        error_html  = f'<span class="error-detail">{r["error"]}</span>' if r["error"] else ""
        return f"""
        <tr class="{estado_cls}">
          <td class="id-col">{r['id']}</td>
          <td>{r['escenario']}{error_html}</td>
          <td><span class="badge pri-{prioridad_cls}">{r['prioridad']}</span></td>
          <td>{r['duracion']} s</td>
          <td><span class="estado {estado_cls}">{estado_txt}</span></td>
        </tr>"""

    filas_html = "".join(fila(r) for r in resultados)

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Resumen de Pruebas — LuxeStay Hotels</title>
      <style>
        *, *::before, *::after {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
          font-family: 'Segoe UI', sans-serif;
          background: #f0f4f8;
          min-height: 100vh;
          padding: 40px 24px;
          color: #1a202c;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}

        /* Header */
        .header {{
          background: linear-gradient(135deg, #0f1e3c, #1a3260);
          border-radius: 16px;
          padding: 32px 36px;
          margin-bottom: 28px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 16px;
        }}
        .header-left h1 {{ color: #fff; font-size: 1.5rem; font-weight: 800; margin-bottom: 4px; }}
        .header-left h1 span {{ color: #c9a84c; }}
        .header-left p {{ color: rgba(255,255,255,0.55); font-size: 0.82rem; }}
        .fecha {{ color: rgba(255,255,255,0.4); font-size: 0.78rem; margin-top: 6px; }}

        /* Tarjetas de resumen */
        .cards {{
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 14px;
          margin-bottom: 28px;
        }}
        .card {{
          background: #fff;
          border-radius: 12px;
          padding: 20px;
          text-align: center;
          box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }}
        .card .num {{ font-size: 2rem; font-weight: 800; line-height: 1; margin-bottom: 6px; }}
        .card .lbl {{ font-size: 0.78rem; color: #6b7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .card.total .num  {{ color: #1a3260; }}
        .card.pass  .num  {{ color: #059669; }}
        .card.fail  .num  {{ color: #dc2626; }}
        .card.pct   .num  {{ color: #c9a84c; }}

        /* Barra de progreso */
        .progress-wrap {{
          background: #fff;
          border-radius: 12px;
          padding: 20px 24px;
          margin-bottom: 28px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }}
        .progress-wrap .prog-label {{
          display: flex;
          justify-content: space-between;
          font-size: 0.82rem;
          font-weight: 600;
          color: #4b5563;
          margin-bottom: 8px;
        }}
        .progress-bar {{
          width: 100%;
          height: 10px;
          background: #fee2e2;
          border-radius: 50px;
          overflow: hidden;
        }}
        .progress-fill {{
          height: 100%;
          width: {porcentaje}%;
          background: linear-gradient(90deg, #059669, #34d399);
          border-radius: 50px;
          transition: width 1s ease;
        }}

        /* Tabla */
        .table-wrap {{
          background: #fff;
          border-radius: 12px;
          overflow: hidden;
          box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead tr {{ background: #0f1e3c; }}
        thead th {{
          color: rgba(255,255,255,0.85);
          font-size: 0.75rem;
          font-weight: 700;
          letter-spacing: 0.8px;
          text-transform: uppercase;
          padding: 14px 16px;
          text-align: left;
        }}
        tbody tr {{ border-bottom: 1px solid #f1f5f9; transition: background 0.15s; }}
        tbody tr:hover {{ background: #f8fafc; }}
        tbody tr.fail {{ background: #fff8f8; }}
        tbody tr.fail:hover {{ background: #fff0f0; }}
        td {{ padding: 13px 16px; font-size: 0.875rem; vertical-align: middle; }}
        .id-col {{ font-weight: 700; color: #1a3260; }}

        .estado {{ font-weight: 700; font-size: 0.82rem; padding: 4px 10px; border-radius: 50px; }}
        .estado.pass {{ background: #d1fae5; color: #065f46; }}
        .estado.fail {{ background: #fee2e2; color: #991b1b; }}

        .badge {{ font-size: 0.72rem; font-weight: 700; padding: 3px 9px; border-radius: 50px; }}
        .pri-alta  {{ background: #fee2e2; color: #991b1b; }}
        .pri-media {{ background: #fef3c7; color: #92400e; }}
        .pri-baja  {{ background: #dbeafe; color: #1e40af; }}

        .error-detail {{
          display: block;
          font-size: 0.75rem;
          color: #dc2626;
          margin-top: 4px;
          font-style: italic;
        }}

        .footer {{
          text-align: center;
          margin-top: 24px;
          font-size: 0.78rem;
          color: #9ca3af;
        }}
      </style>
    </head>
    <body>
    <div class="container">

      <div class="header">
        <div class="header-left">
          <h1>Luxe<span>Stay</span> Hotels — Resumen de Pruebas</h1>
          <p>Formulario de Registro · Suite automatizada Selenium</p>
          <p class="fecha">Ejecutado el {ahora}</p>
        </div>
      </div>

      <div class="cards">
        <div class="card total"><div class="num">{total}</div><div class="lbl">Total</div></div>
        <div class="card pass"> <div class="num">{pasaron}</div><div class="lbl">Pasaron</div></div>
        <div class="card fail"> <div class="num">{fallaron}</div><div class="lbl">Fallaron</div></div>
        <div class="card pct">  <div class="num">{porcentaje}%</div><div class="lbl">Éxito</div></div>
      </div>

      <div class="progress-wrap">
        <div class="prog-label">
          <span>Progreso de la suite</span>
          <span>{pasaron} de {total} casos exitosos</span>
        </div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
      </div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Escenario</th>
              <th>Prioridad</th>
              <th>Duración</th>
              <th>Resultado</th>
            </tr>
          </thead>
          <tbody>
            {filas_html}
          </tbody>
        </table>
      </div>

      <p class="footer">LuxeStay Hotels · Pruebas automatizadas con Selenium + pytest</p>
    </div>
    </body>
    </html>
    """

    # Navegar a una página en blanco e inyectar el HTML del resumen
    driver.get("about:blank")
    driver.execute_script("document.open(); document.write(arguments[0]); document.close();", html)


# ══════════════════════════════════════════════════════════════════════════════
# CP01 — Registro exitoso con todos los datos válidos
# Prioridad: Alta
# ══════════════════════════════════════════════════════════════════════════════
def test_cp01_registro_exitoso(driver):
    """
    Precondición : Usuario accede al formulario con un correo no registrado.
    Entrada      : Nombre: José García | Correo: jose@eko.com | Contraseña: Fjkig546*
    Resultado    : Mensaje de confirmación visible y usuario guardado en memoria.
    """
    llenar_formulario(driver, "José García", "jose@eko.com", "Fjkig546*")
    enviar_formulario(driver)

    alert = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "alert-box"))
    )
    time.sleep(2)

    assert "Bienvenido" in alert.text, \
        f"CP01 FALLO — Se esperaba mensaje de bienvenida, se obtuvo: '{alert.text}'"

    registrados = usuarios_en_memoria(driver)
    correos = [u["correo"] for u in registrados]
    assert "jose@eko.com" in correos, \
        "CP01 FALLO — El usuario no quedó guardado en memoria"


# ══════════════════════════════════════════════════════════════════════════════
# CP02 — Registro con campos vacíos
# Prioridad: Alta
# ══════════════════════════════════════════════════════════════════════════════
def test_cp02_campos_vacios(driver):
    """
    Precondición : Ninguna.
    Entrada      : Nombre: "" | Correo: "" | Contraseña: ""
    Resultado    : Mensajes de error en los 3 campos, no permite el registro.
    """
    enviar_formulario(driver)
    time.sleep(PAUSA_ENTRE_PASOS)

    assert "error" in obtener_clase_campo(driver, "nombre"), \
        "CP02 FALLO — Campo 'nombre' debería marcarse como error"
    assert "error" in obtener_clase_campo(driver, "correo"), \
        "CP02 FALLO — Campo 'correo' debería marcarse como error"
    assert "error" in obtener_clase_campo(driver, "contrasena"), \
        "CP02 FALLO — Campo 'contrasena' debería marcarse como error"

    assert len(usuarios_en_memoria(driver)) == 0, \
        "CP02 FALLO — No debería haberse registrado ningún usuario"


# ══════════════════════════════════════════════════════════════════════════════
# CP03 — Registro con correo inválido
# Prioridad: Alta
# ══════════════════════════════════════════════════════════════════════════════
def test_cp03_correo_invalido(driver):
    """
    Precondición : Ninguna.
    Entrada      : Nombre: María Gómez | Correo: mgomez.com | Contraseña: Tplig572*
    Resultado    : Error indicando que el formato del correo es inválido.
    """
    llenar_formulario(driver, "María Gómez", "mgomez.com", "Tplig572*")
    enviar_formulario(driver)
    time.sleep(PAUSA_ENTRE_PASOS)

    assert "error" in obtener_clase_campo(driver, "correo"), \
        "CP03 FALLO — Campo 'correo' debería marcarse como error"

    errores = obtener_errores_campo(driver, "correo")
    assert "válido" in errores, \
        f"CP03 FALLO — Mensaje de error esperado sobre formato, se obtuvo: '{errores}'"

    assert "success" in obtener_clase_campo(driver, "nombre"), \
        "CP03 FALLO — Campo 'nombre' debería ser válido"
    assert "success" in obtener_clase_campo(driver, "contrasena"), \
        "CP03 FALLO — Campo 'contrasena' debería ser válido"


# ══════════════════════════════════════════════════════════════════════════════
# CP04 — Registro con contraseña insegura
# Prioridad: Media
# ══════════════════════════════════════════════════════════════════════════════
def test_cp04_contrasena_insegura(driver):
    """
    Precondición : Ninguna.
    Entrada      : Nombre: Juan Gómez | Correo: juan@mail.com | Contraseña: 123
    Resultado    : Error indicando que la contraseña no cumple la longitud mínima.
    """
    llenar_formulario(driver, "Juan Gómez", "juan@mail.com", "123")
    enviar_formulario(driver)
    time.sleep(PAUSA_ENTRE_PASOS)

    assert "error" in obtener_clase_campo(driver, "contrasena"), \
        "CP04 FALLO — Campo 'contrasena' debería marcarse como error"

    errores = obtener_errores_campo(driver, "contrasena")
    assert "8 caracteres" in errores, \
        f"CP04 FALLO — Mensaje esperado sobre longitud mínima, se obtuvo: '{errores}'"


# ══════════════════════════════════════════════════════════════════════════════
# CP05 — Registro con correo ya existente
# Prioridad: Alta
# ══════════════════════════════════════════════════════════════════════════════
def limpiar_formulario(driver):
    """Limpia el formulario SIN recargar la página para conservar la memoria JS."""
    for field_id in ["nombre", "correo", "contrasena"]:
        campo = esperar_campo(driver, field_id)
        campo.clear()
        driver.execute_script("arguments[0].classList.remove('error', 'success');", campo)
    driver.execute_script("""
        document.getElementById('nombre-errors').innerHTML     = '';
        document.getElementById('correo-errors').innerHTML     = '';
        document.getElementById('contrasena-errors').innerHTML = '';
        document.getElementById('alert-box').style.display    = 'none';
        document.getElementById('password-strength').style.display = 'none';
    """)
    time.sleep(PAUSA_ENTRE_PASOS)


def test_cp05_correo_ya_existente(driver):
    """
    Precondición : El correo existe@eko.com ya debe estar registrado en memoria.
    Entrada      : Nombre: José García | Correo: existe@eko.com | Contraseña: Fjkig546*
    Resultado    : Error indicando que el correo ya está registrado.
    """
    registrar_usuario_completo(driver, "José García", "existe@eko.com", "Fjkig546*")

    registrados = usuarios_en_memoria(driver)
    assert any(u["correo"] == "existe@eko.com" for u in registrados), \
        "CP05 FALLO — Precondición no cumplida: el usuario no se registró en memoria"

    limpiar_formulario(driver)

    llenar_formulario(driver, "José García", "existe@eko.com", "Fjkig546*")
    enviar_formulario(driver)
    time.sleep(PAUSA_ENTRE_PASOS)

    assert "error" in obtener_clase_campo(driver, "correo"), \
        "CP05 FALLO — Campo 'correo' debería marcarse como error"

    alert = obtener_alert(driver)
    assert "ya tiene una cuenta" in alert, \
        f"CP05 FALLO — Se esperaba mensaje de correo duplicado, se obtuvo: '{alert}'"


# ══════════════════════════════════════════════════════════════════════════════
# CP06 — Envío de correo de confirmación tras registro exitoso
# Prioridad: Baja
# ══════════════════════════════════════════════════════════════════════════════
def test_cp06_confirmacion_registro(driver):
    """
    Precondición : Usuario previamente registrado con datos válidos.
    Entrada      : Usuario registrado con datos válidos.
    Resultado    : Mensaje de éxito que menciona confirmación por correo.
    """
    llenar_formulario(driver, "Pedro Ramírez", "pedro@mail.com", "Confirm99*")
    enviar_formulario(driver)
    time.sleep(2)

    alert = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "alert-box"))
    )

    assert "Bienvenido" in alert.text, \
        "CP06 FALLO — Se esperaba mensaje de registro exitoso"
    assert "correo" in alert.text.lower(), \
        f"CP06 FALLO — El mensaje debería mencionar confirmación por correo, se obtuvo: '{alert.text}'"


# ══════════════════════════════════════════════════════════════════════════════
# CP07 — Registro con caracteres maliciosos (XSS)
# Prioridad: Alta
# ══════════════════════════════════════════════════════════════════════════════
def test_cp07_caracteres_maliciosos(driver):
    """
    Precondición : Ninguna.
    Entrada      : Nombre: <script>alert('123')</script>
                   Correo: test@mail.com | Contraseña: Abc123*
    Resultado    : El sistema rechaza el input y no ejecuta el script.
    """
    payload_xss = "<script>alert('123')</script>"

    llenar_formulario(driver, payload_xss, "test@mail.com", "Abc123*")
    enviar_formulario(driver)
    time.sleep(PAUSA_ENTRE_PASOS)

    try:
        alert_nativo = driver.switch_to.alert
        alert_nativo.dismiss()
        pytest.fail("CP07 FALLO — Se ejecutó el script XSS (alert nativo detectado)")
    except Exception:
        pass

    assert "error" in obtener_clase_campo(driver, "nombre"), \
        "CP07 FALLO — El campo 'nombre' debería rechazar el payload XSS"

    errores = obtener_errores_campo(driver, "nombre")
    assert len(errores) > 0, \
        "CP07 FALLO — Debería mostrarse un mensaje de error de validación"

    scripts_activos = driver.execute_script(
        "return document.querySelectorAll('script').length;"
    )
    assert scripts_activos <= 3, \
        f"CP07 FALLO — Se detectaron scripts inyectados en el DOM ({scripts_activos})"


# ── Helpers (definidos después de los fixtures para claridad) ──────────────────

def esperar_campo(driver, field_id, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.ID, field_id))
    )


def escribir_lento(driver, field_id, texto):
    campo = esperar_campo(driver, field_id)
    driver.execute_script("arguments[0].scrollIntoView(true);", campo)
    campo.click()
    campo.clear()
    time.sleep(0.2)
    for caracter in texto:
        campo.send_keys(caracter)
        time.sleep(VELOCIDAD_ESCRITURA)


def llenar_formulario(driver, nombre="", correo="", password=""):
    if nombre:
        escribir_lento(driver, "nombre", nombre)
        time.sleep(PAUSA_ENTRE_PASOS)
    if correo:
        escribir_lento(driver, "correo", correo)
        time.sleep(PAUSA_ENTRE_PASOS)
    if password:
        escribir_lento(driver, "contrasena", password)
        time.sleep(PAUSA_ENTRE_PASOS)


def enviar_formulario(driver):
    time.sleep(PAUSA_ENTRE_PASOS)
    btn = esperar_campo(driver, "submitBtn")
    btn.click()


def obtener_clase_campo(driver, field_id):
    return driver.find_element(By.ID, field_id).get_attribute("class")


def obtener_errores_campo(driver, field_id):
    return driver.find_element(By.ID, f"{field_id}-errors").text.strip()


def obtener_alert(driver, timeout=5):
    alert = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "alert-box"))
    )
    return alert.text.strip()


def usuarios_en_memoria(driver):
    return driver.execute_script("return window.__usuariosRegistrados;") or []


def registrar_usuario_completo(driver, nombre, correo, password):
    llenar_formulario(driver, nombre, correo, password)
    enviar_formulario(driver)
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "alert-box"), "Bienvenido")
    )


# ── Punto de entrada ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
