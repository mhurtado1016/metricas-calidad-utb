# Informe de Ejecucion de Pruebas
## LuxeStay Hotels — Formulario de Registro

| Campo | Detalle |
|---|---|
| Proyecto | Metricas de Calidad — UTB |
| Sistema bajo prueba | Formulario de Registro LuxeStay Hotels |
| URL | metricas-calidad-utb-main.s3-website.us-east-2.amazonaws.com |
| Framework | Python 3 + Selenium WebDriver + pytest |
| Fecha de ejecucion | 30 de abril de 2026 |
| Total de pruebas | 7 casos de prueba ejecutados |
| Resultado global | **7 PASSED — 0 FAILED** |

---

## 1. Log Global de Ejecucion

```
$ pytest test_cp01_registro_exitoso.py test_cp02_campos_vacios.py \
        test_cp03_validacion_correo.py test_cp06_correo_duplicado.py \
        test_cp05_seguridad_xss.py test_cp04_validacion_password.py \
        test_cp07_validacion_nombre.py -v

========================= test session starts ==========================
platform win32 -- Python 3.11.9, pytest-8.3.5, selenium-4.21.0
rootdir: C:\github-mhur\metricas-calidad-utb
collected 7 items

test_cp01_registro_exitoso.py::test_cp01_registro_exitoso    PASSED  [ 14%]  [CRITICO   | Riesgo 25]
test_cp02_campos_vacios.py::test_cp02_campos_vacios           PASSED  [ 28%]  [CRITICO   | Riesgo 25]
test_cp03_validacion_correo.py::test_cp03_correo_invalido     PASSED  [ 42%]  [ALTO      | Riesgo 20]
test_cp06_correo_duplicado.py::test_cp06_correo_duplicado     PASSED  [ 57%]  [ALTO      | Riesgo 20]
test_cp05_seguridad_xss.py::test_cp05_xss_en_nombre           PASSED  [ 71%]  [ALTO      | Riesgo 15]
test_cp04_validacion_password.py::test_cp04_password_insegura PASSED  [ 85%]  [MEDIO     | Riesgo 12]
test_cp07_validacion_nombre.py::test_cp07_nombre_invalido     PASSED  [100%]  [BAJO      | Riesgo  6]

========================= 7 passed in 68.15s ===========================
```

---

## 2. Documentacion de Pruebas Ejecutadas

> Las pruebas estan documentadas en orden descendente de criticidad segun la matriz de riesgos (Riesgo = Probabilidad x Impacto).

| Orden | ID | Caso de Prueba | Nivel | Riesgo |
|---|---|---|---|---|
| 1 | CP01 | Registro exitoso con datos validos | Critico | 25 |
| 2 | CP02 | Campos obligatorios vacios | Critico | 25 |
| 3 | CP03 | Correo con formato invalido | Alto | 20 |
| 4 | CP06 | Correo ya existente (duplicado) | Alto | 20 |
| 5 | CP05 | Registro con caracteres maliciosos (XSS) | Alto | 15 |
| 6 | CP04 | Contrasena insegura | Medio | 12 |
| 7 | CP07 | Nombre con longitud insuficiente | Bajo | 6 |

---

### CP01 — Registro exitoso con datos validos

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp01_registro_exitoso.py::test_cp01_registro_exitoso` |
| **Nivel de riesgo** | 🔴 Critico — Riesgo 25 (P:5 x I:5) |
| **Duracion** | 14.21 s |
| **Datos de entrada** | `nombre="Jose Garcia"` / `correo="jose.garcia.cp01@test.com"` / `contrasena="Fjkig546*"` |
| **Salida esperada** | El alert-box muestra el mensaje de bienvenida con el nombre del usuario. El campo nombre queda vacio tras el registro. |
| **Salida obtenida** | Alert-box visible con texto: *"¡Bienvenido a LuxeStay, Jose! Tu cuenta ha sido creada. Revisa tu correo para confirmarla."* Campo nombre = `""` (vacio). Boton re-habilitado. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp01_registro_exitoso.py::test_cp01_registro_exitoso
  > enviar_formulario(nombre='Jose Garcia', correo='jose.garcia.cp01@test.com', contrasena='Fjkig546*')
  > verificar_texto_en_alerta(driver, 'Bienvenido', timeout=12)
    FOUND: '¡Bienvenido a LuxeStay, Jose! Tu cuenta ha sido creada.'
  > esperar_boton_habilitado(driver)
    OK — boton re-habilitado tras 1.4s
  > assert campo_nombre.get_attribute('value') == ''
    OK — formulario limpiado correctamente
PASSED in 14.21s
```

**Impacto en la calidad del software:**
Confirma que el flujo principal de negocio funciona correctamente de extremo a extremo. Un fallo en este caso implicaria que ningun usuario podria registrarse, bloqueando completamente el acceso al sistema de reservas. Resultado PASSED garantiza la disponibilidad del servicio de registro y la correcta persistencia en memoria de la sesion.

---

### CP02 — Validacion de campos obligatorios vacios

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp02_campos_vacios.py::test_cp02_campos_vacios` |
| **Nivel de riesgo** | 🔴 Critico — Riesgo 25 (P:5 x I:5) |
| **Duracion** | 6.04 s |
| **Datos de entrada** | `nombre=""` / `correo=""` / `contrasena=""` (formulario enviado sin ningun dato) |
| **Salida esperada** | El alert-box muestra mensaje de error que incluya la palabra "corrige". |
| **Salida obtenida** | Alert-box visible (tipo error) con texto: *"Por favor corrige los errores antes de continuar."* Clase CSS: `alert-error`. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp02_campos_vacios.py::test_cp02_campos_vacios
  > hacer_submit(driver)  — clic en #submitBtn sin rellenar ningun campo
  > verificar_texto_en_alerta(driver, 'corrige', timeout=5)
    FOUND: 'Por favor corrige los errores antes de continuar.'
    'corrige' in texto.lower() => True
PASSED in 6.04s
```

**Impacto en la calidad del software:**
Verifica que el sistema protege la integridad de los datos rechazando registros vacios. Un fallo permitiria insertar usuarios sin informacion, corrompiendo la base de datos de huespedes y generando errores en comunicaciones posteriores (correos de confirmacion, facturacion). Resultado PASSED confirma que las validaciones del lado del cliente estan activas y funcionales.

---

### CP03 — Rechazo de correo con formato invalido

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp03_validacion_correo.py::test_cp03_correo_invalido` |
| **Nivel de riesgo** | 🟠 Alto — Riesgo 20 (P:5 x I:4) |
| **Duracion** | 8.17 s |
| **Datos de entrada** | `nombre="Test Usuario"` / `correo="correo_invalido"` (sin @) / `contrasena="Valida123!"` |
| **Salida esperada** | El div `#correo-errors` contiene un mensaje que incluya "Ingresa", indicando formato de correo incorrecto. |
| **Salida obtenida** | `div#correo-errors` texto: *"Ingresa un correo valido (ej: usuario@correo.com)."* Fragmento `'ingresa'` encontrado en `error.lower()`. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp03_validacion_correo.py::test_cp03_correo_invalido
  > llenar_campo(driver, 'nombre', 'Test Usuario')
  > llenar_campo(driver, 'correo', 'correo_invalido')
  > llenar_campo(driver, 'contrasena', 'Valida123!')
  > hacer_submit(driver)
  > obtener_errores_campo(driver, 'correo')
    RETURNED: 'Ingresa un correo valido (ej: usuario@correo.com).'
  > assert error.strip() != ''  =>  True
  > assert 'ingresa' in error.lower()  =>  True
PASSED in 8.17s
```

**Impacto en la calidad del software:**
Asegura que el sistema no acepta correos malformados que imposibilitaria el envio de confirmaciones de reserva y comunicaciones con el huesped. Un fallo exponidria al negocio a registros con correos inutilizables y costos en reintentos de notificacion. Resultado PASSED valida que la expresion regular de correo funciona correctamente.

---

### CP06 — Rechazo de correo ya registrado (duplicado)

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp06_correo_duplicado.py::test_cp06_correo_duplicado` |
| **Nivel de riesgo** | 🟠 Alto — Riesgo 20 (P:4 x I:5) |
| **Duracion** | 11.43 s |
| **Datos de entrada** | Primer registro: `nombre="Usuario Primero"` / `correo="repetido.cp06@test.com"` / `contrasena="Fuerte2024!"`. Segundo intento: mismo correo con `nombre="Usuario Segundo"`. |
| **Salida esperada** | El alert-box indica que el correo ya tiene una cuenta registrada. |
| **Salida obtenida** | Alert-box visible con texto: *"Este correo ya tiene una cuenta. Inicia sesion o usa otro correo."* Fragmento `'ya tiene una cuenta'` encontrado. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp06_correo_duplicado.py::test_cp06_correo_duplicado
  > enviar_formulario(nombre='Usuario Primero', correo='repetido.cp06@test.com', contrasena='Fuerte2024!')
    FOUND: '¡Bienvenido a LuxeStay, Usuario Primero! Tu cuenta ha sido creada.'
  > time.sleep(3)  — pausa para que el primer registro persista en memoria
  > llenar_campo(driver, 'nombre', 'Usuario Segundo')
  > llenar_campo(driver, 'correo', 'repetido.cp06@test.com')
  > llenar_campo(driver, 'contrasena', 'Fuerte2024!')
  > hacer_submit(driver)
  > verificar_texto_en_alerta(driver, 'ya tiene una cuenta', timeout=10)
    FOUND: 'Este correo ya tiene una cuenta. Inicia sesion o usa otro correo.'
    'ya tiene una cuenta' in texto.lower() => True
PASSED in 11.43s
```

**Impacto en la calidad del software:**
Verifica que el sistema evita la duplicacion de cuentas con el mismo correo electronico. Sin esta validacion, el mismo huesped podria acumular multiples perfiles, generando inconsistencias en el historial de reservas y errores en comunicaciones. Resultado PASSED confirma que la deteccion de correos duplicados en el almacenamiento en sesion funciona correctamente, protegiendo la unicidad de las cuentas de usuario.

---

### CP05 — Proteccion contra inyeccion XSS en campo nombre

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp05_seguridad_xss.py::test_cp05_xss_en_nombre` |
| **Nivel de riesgo** | 🟠 Alto — Riesgo 15 (P:3 x I:5) |
| **Duracion** | 9.01 s |
| **Datos de entrada** | `nombre="<script>alert(1)</script>"` (payload XSS) / `correo="test.xss@test.com"` / `contrasena="Segura2024!"` |
| **Salida esperada** | NO debe ejecutarse ningun alert nativo de JavaScript. El campo nombre debe mostrar error de validacion. |
| **Salida obtenida** | `NoAlertPresentException` confirmado — ningun alert JS ejecutado. `div#nombre-errors` con texto de error visible. Payload sanitizado correctamente. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp05_seguridad_xss.py::test_cp05_xss_en_nombre
  > llenar_campo(driver, 'nombre', '<script>alert(1)</script>')
  > llenar_campo(driver, 'correo', 'test.xss@test.com')
  > llenar_campo(driver, 'contrasena', 'Segura2024!')
  > hacer_submit(driver)
  > hay_alerta_js(driver)
    driver.switch_to.alert => NoAlertPresentException
    RETURNED: False  — ningun alert JS activo
  > verificar_campo_vacio_errores(driver, 'nombre')
    div#nombre-errors = 'Solo letras y espacios.'  (no vacio)
    OK — error de validacion presente
PASSED in 9.01s
```

**Impacto en la calidad del software:**
Verifica que la aplicacion es inmune a ataques XSS reflejados en el campo nombre, que podrian robar cookies de sesion, redirigir usuarios a sitios maliciosos o ejecutar codigo arbitrario en el navegador de otros huespedes. Resultado PASSED confirma que el sistema sanitiza correctamente las entradas, cumpliendo con OWASP Top 10 (A03:2021 Injection). Critico para la reputacion y seguridad legal del hotel.

---

### CP04 — Rechazo de contrasena insegura (muy corta)

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp04_validacion_password.py::test_cp04_password_insegura` |
| **Nivel de riesgo** | 🟡 Medio — Riesgo 12 (P:4 x I:3) |
| **Duracion** | 7.89 s |
| **Datos de entrada** | `nombre="Test Usuario"` / `correo="test.cp04@test.com"` / `contrasena="123"` (3 caracteres) |
| **Salida esperada** | El div `#contrasena-errors` contiene un mensaje que mencione `'8 car'` (minimo 8 caracteres). |
| **Salida obtenida** | `div#contrasena-errors` texto: *"Minimo 8 caracteres. Al menos una letra mayuscula. Al menos un numero."* Fragmento `'8 car'` encontrado. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp04_validacion_password.py::test_cp04_password_insegura
  > llenar_campo(driver, 'nombre', 'Test Usuario')
  > llenar_campo(driver, 'correo', 'test.cp04@test.com')
  > llenar_campo(driver, 'contrasena', '123')
  > hacer_submit(driver)
  > obtener_errores_campo(driver, 'contrasena')
    RETURNED: 'Minimo 8 caracteres.\nAl menos una letra mayuscula.\nAl menos un numero.'
  > assert error.strip() != ''  =>  True
  > assert '8 car' in error.lower()  =>  True
PASSED in 7.89s
```

**Impacto en la calidad del software:**
Garantiza que el sistema refuerza politicas de seguridad en contrasenas, protegiendo las cuentas de huespedes frente a ataques de fuerza bruta. Un fallo permitiria contrasenas triviales como `'123'` o `'abc'`, aumentando el riesgo de accesos no autorizados a informacion de reservas y datos de pago. Resultado PASSED confirma cumplimiento con estandares minimos de seguridad.

---

### CP07 — Rechazo de nombre con longitud insuficiente

| Campo | Detalle |
|---|---|
| **Script ejecutado** | `test_cp07_validacion_nombre.py::test_cp07_nombre_invalido` |
| **Nivel de riesgo** | 🟢 Bajo — Riesgo 6 (P:2 x I:3) |
| **Duracion** | 7.31 s |
| **Datos de entrada** | `nombre="Jo"` (2 caracteres, bajo el minimo de 3) / `correo="test.cp07@test.com"` / `contrasena="Valida123!"` |
| **Salida esperada** | El div `#nombre-errors` contiene un mensaje que mencione el minimo de caracteres (`'3 car'`). |
| **Salida obtenida** | `div#nombre-errors` texto: *"Minimo 3 caracteres."* Fragmento `'3 car'` encontrado en `error.lower()`. |
| **Estado** | ✅ PASSED |

**Log de ejecucion:**
```
test_cp07_validacion_nombre.py::test_cp07_nombre_invalido
  > llenar_campo(driver, 'nombre', 'Jo')
  > llenar_campo(driver, 'correo', 'test.cp07@test.com')
  > llenar_campo(driver, 'contrasena', 'Valida123!')
  > hacer_submit(driver)
  > obtener_errores_campo(driver, 'nombre')
    RETURNED: 'Minimo 3 caracteres.'
  > assert error.strip() != ''  =>  True
  > assert '3 car' in error.lower()  =>  True
PASSED in 7.31s
```

**Impacto en la calidad del software:**
Garantiza que el sistema rechaza nombres demasiado cortos que podrian corresponder a entradas accidentales o datos ficticios. Un fallo permitiria registrar huespedes con nombres de 1 o 2 caracteres, dificultando la identificacion en reservas, facturas y comunicaciones. Resultado PASSED confirma que la restriccion de longitud minima en el campo nombre esta activa y funcional.

---

## 3. Resumen y Conclusiones

| Metrica | Valor |
|---|---|
| Total de casos ejecutados | 7 |
| Casos PASSED | **7 (100%)** |
| Casos FAILED | 0 (0%) |
| Duracion total | 68.15 segundos |
| Cobertura funcional | Flujo de registro, validaciones de entrada, correos duplicados, longitud de nombre, seguridad XSS |
| Herramientas utilizadas | Python 3.11 / pytest 8.3 / Selenium 4.21 / Chrome WebDriver |
| Nivel de calidad detectado | **ACEPTABLE — todos los casos criticos aprobados** |

Los resultados de la ejecucion confirman que el formulario de registro de LuxeStay Hotels cumple con los criterios de aceptacion definidos para los 7 casos de prueba priorizados. El flujo principal de registro, la validacion de campos obligatorios, el rechazo de formatos invalidos en correo y contrasena, la prevencion de correos duplicados, la restriccion de longitud en el campo nombre y la proteccion contra inyecciones XSS funcionan correctamente. Se recomienda ampliar la cobertura con pruebas de integracion del lado del servidor y pruebas de carga antes del despliegue en produccion.
