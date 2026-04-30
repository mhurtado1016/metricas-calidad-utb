# metricas-calidad-utb

## Actividad semana 3 - Grupo 7

Suite de pruebas automatizadas con Python + Selenium + pytest para el formulario de registro de **LuxeStay Hotels**.

---

## Pre-requisitos

### 1. Python 3.9 o superior

Verificar que Python esta instalado:

```
python --version
```

Descargar desde [https://www.python.org/downloads/](https://www.python.org/downloads/) si no esta disponible. Asegurarse de marcar **"Add Python to PATH"** durante la instalacion.

### 2. Google Chrome

El framework usa ChromeDriver para controlar el navegador. Debe tener Chrome instalado en su maquina. Descargar desde [https://www.google.com/chrome/](https://www.google.com/chrome/).

### 3. Dependencias de Python

Instalar todas las dependencias con un solo comando desde la raiz del proyecto:

```
pip install pytest selenium webdriver-manager
```

| Paquete | Version minima | Uso |
|---|---|---|
| `pytest` | 8.0+ | Framework de ejecucion de pruebas |
| `selenium` | 4.0+ | Automatizacion del navegador |
| `webdriver-manager` | 4.0+ | Descarga automatica de ChromeDriver |

---

## Estructura del proyecto

```
metricas-calidad-utb/
├── conftest.py                       # Fixtures compartidos (driver, URL base)
├── utils/
│   └── helpers.py                    # Funciones auxiliares reutilizables
├── test_cp01_registro_exitoso.py     # CP01 - Registro exitoso con datos validos
├── test_cp02_campos_vacios.py        # CP02 - Validacion de campos obligatorios vacios
├── test_cp03_validacion_correo.py    # CP03 - Rechazo de correo con formato invalido
├── test_cp04_validacion_password.py  # CP04 - Rechazo de contrasena insegura
├── test_cp05_seguridad_xss.py        # CP05 - Proteccion contra inyeccion XSS
├── test_cp06_correo_duplicado.py     # CP06 - Rechazo de correo ya registrado
├── test_cp07_validacion_nombre.py    # CP07 - Rechazo de nombre con longitud insuficiente
└── evidencia_pruebas.md              # Informe de ejecucion con logs y resultados
```

---

## Ejecucion de pruebas

Abrir una terminal (cmd, PowerShell o terminal de VS Code) y navegar hasta la carpeta donde se descargo el proyecto:

```
cd ruta/hacia/metricas-calidad-utb
```

### Correr todos los casos de prueba

```
pytest -v
```

El orden de ejecucion es automatico: `conftest.py` aplica la matriz de riesgos del proyecto y corre los tests de mayor a menor criticidad.

| Orden | Caso de Prueba | Nivel | Riesgo (P x I) |
|---|---|---|---|
| 1 | Registro exitoso con datos validos | Critico | 25 |
| 2 | Campos obligatorios vacios | Critico | 25 |
| 3 | Correo con formato invalido | Alto | 20 |
| 4 | Correo ya existente (duplicado) | Alto | 20 |
| 5 | Registro con caracteres maliciosos (XSS) | Alto | 15 |
| 6 | Contrasena insegura | Medio | 12 |
| 7 | Nombre con longitud insuficiente | Bajo | 6 |

### Correr un caso de prueba especifico

```
pytest test_cp01_registro_exitoso.py -v
pytest test_cp06_correo_duplicado.py -v
```

### Opciones utiles de pytest

| Opcion | Descripcion |
|---|---|
| `-v` | Modo verbose: muestra el nombre de cada test y su resultado |
| `--tb=short` | Muestra un traceback reducido en caso de fallo |
| `--tb=long` | Muestra el traceback completo en caso de fallo |
| `-s` | Muestra la salida de `print()` durante la ejecucion |
| `-x` | Detiene la ejecucion al primer fallo |

---

## Notas

- Cada prueba abre una ventana de Chrome que permanece visible **4 segundos** tras finalizar para que el resultado sea legible antes de cerrarse. Este comportamiento esta configurado en `conftest.py` mediante la variable `PAUSA_CIERRE`.
- Las pruebas se ejecutan contra la URL: `http://metricas-calidad-utb-main.s3-website.us-east-2.amazonaws.com`
- No se requiere levantar ningun servidor local; el sistema bajo prueba esta desplegado en AWS S3.
