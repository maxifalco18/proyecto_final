# 🧱 Proyecto Integrador – Fase 1

Este repositorio corresponde al **Avance 1** del Proyecto Integrador de Henry, enfocado en la construcción de un sistema de análisis de ventas para una empresa distribuida geográficamente. El objetivo es aplicar conceptos de bases de datos, programación orientada a objetos (POO), pruebas unitarias y buenas prácticas de ingeniería de datos.

---

## ✅ Objetivos de esta fase

- Estructurar el proyecto con buenas prácticas.
- Modelar las entidades del negocio como clases en Python.
- Cargar datos desde archivos `.csv` a una base de datos PostgreSQL.
- Validar los datos cargados.
- Implementar pruebas unitarias simples con `pytest`.

---

## 🗂️ Estructura del Proyecto

```
proyecto_integrador/
├── data/                     # Archivos CSV de entrada
├── src/                      # Código fuente del modelo de datos
│   ├── __init__.py           # Define src como módulo de Python
│   └── models.py             # Clases que representan las tablas (POO)
├── sql/                      # Scripts SQL de creación y carga de datos
│   └── load_data.sql
├── tests/                    # Pruebas unitarias
│   └── test_models.py
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
└── .env                      # Variables de entorno (no incluido en git)

---

## ▶️ Cómo correr el proyecto localmente

1. **Clonar el repositorio**:

```bash
git clone <repo-url>
cd proyecto_integrador
```
2. **Crear y activar entorno virtual**:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
3. **Instalar dependencias**:

```bash
pip install -r requirements.txt
```
4. **Verificar que la carpeta `src/` tenga un archivo `__init__.py`**:

```bash
touch src/__init__.py  # o crear manualmente un archivo vacío
```
5. **Configuración de la Base de Datos**:

Se utilizó **PostgreSQL en un contenedor Docker**:

```bash
docker run --name pg-integrador -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=proyecto_integrador -p 5432:5432 -d postgres:15
```

Los archivos `.csv` fueron copiados al contenedor:

```bash
docker cp ./data/. pg-integrador:/data
```
---

## 🧱 Script de Creación y Carga

**Ejecutar script SQL en DBeaver o desde psql**:

El script SQL completo se encuentra en [`sql/load_data.sql`](sql/load_data.sql), e incluye:

- `CREATE TABLE` para cada entidad: `countries`, `cities`, `customers`, `employees`, `sales`, `products`, `categories`.
- `COPY` para cargar los `.csv`.

---

## 🔄 Validación de Carga

Se validaron las filas cargadas en cada tabla:

| Tabla       | Registros |
|-------------|-----------|
| countries   | 206       |
| cities      | 96        |
| categories  | 11        |
| products    | 452       |
| customers   | 98759     |
| employees   | 23        |
| sales       | 50000     |

También se corrigieron errores de formato en campos como `ModifyDate` y `SalesDate`.

---

6. **Correr los tests**:

Se implementaron dos pruebas básicas usando `pytest` en el archivo `tests/test_models.py`:

- Creación de objeto `Product`
- Método personalizado `full_name` en `Customer`

Para correr los tests:

```bash
pytest tests/test_models.py -v
```
---

## ✔️ Estado de Avance

| Requisito                            | Cumplido |
|--------------------------------------|-----------|
| Estructura del proyecto              | ✅       |
| Carga de datos en base PostgreSQL    | ✅       |
| Clases Python con POO                | ✅       |
| Pruebas con pytest                   | ✅       |
| Validación de datos                  | ✅       |
| Documentación (README)               | ✅       |

---
## ✅ Requisitos cumplidos

### 1. Creación de la base de datos y carga de CSV
- Se creó una instancia de PostgreSQL en Docker.
- Se generaron las tablas `countries`, `cities`, `customers`, `employees`, `products`, `sales` y `categories` a partir del modelo lógico.
- Se cargaron datos desde los CSV usando sentencias `COPY` dentro del contenedor.

### 2. Normalización
- Se reemplazaron los campos `CityName` y `CountryName` por `CityID` y `CountryID` en la tabla `customers`.
- Se resolvieron los valores `NULL` en `CountryID` con una sentencia `UPDATE` basada en join entre `customers`, `cities` y `countries`.

### 3. Programación orientada a objetos
- Se modeló cada entidad como clase Python en `src/models.py`, aplicando encapsulamiento, métodos auxiliares (`full_name`) y `__repr__` para facilitar depuración.
- Las clases modeladas fueron: `Category`, `Country`, `City`, `Customer`, `Employee`, `Product` y `Sale`.

### 4. Pruebas unitarias
- Se implementaron pruebas en `tests/test_models.py` para validar el comportamiento de instanciación y métodos personalizados como `full_name`.
- Se usó `pytest`, permitiendo detección automática de tests.

---
## 📌 Notas finales

- Se manejaron correctamente tipos de datos y relaciones con claves foráneas.
- Se corrigieron valores inválidos manualmente (`SalesDate`, `ModifyDate`).
- Se establecieron convenciones de nombres y estilos para facilitar futuras ampliaciones del sistema.
- En la tabla `products`, el campo `ModifyDate` se almacena como `TEXT` por problemas de formato en los datos.
- En la tabla `sales`, el campo `SalesDate` también se almacena como `TEXT`, ya que los valores no respetan un formato de fecha válido (`31:24.2`).
- La integridad referencial fue respetada con claves foráneas (`FOREIGN KEY`) entre tablas relacionadas.
- Los datos cargados desde los `.csv` fueron verificados en cuanto a cantidad de registros y consistencia.

---

# 🧱 Proyecto Integrador – Fase 2 – Modularización, patrones de diseño y consultas en Python

Esta etapa aborda la modularización del sistema, la aplicación de patrones de diseño, la conexión entre Python y MySQL, y la ejecución de consultas SQL desde código, junto con pruebas unitarias y protección de credenciales.

## ✅ Objetivos de esta fase

- Modularizar el proyecto utilizando patrones de diseño.
- Crear una clase de conexión a la base de datos aplicando el patrón Singleton.
- Ejecutar consultas SQL desde Python y devolver resultados como pandas.DataFrame.
- Aplicar buenas prácticas de desacoplamiento, encapsulamiento y separación de responsabilidades.
- Proteger credenciales con python-dotenv.
- Integrar todo en un Jupyter Notebook de presentación.
- Agregar pruebas unitarias enfocadas en la nueva lógica.

## 📁 Estructura del Proyecto

proyecto_integrador/
├── data/
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   └── repository.py
├── sql/
│   └── load_data.sql
├── tests/
│   ├── test_models.py
│   ├── test_database.py
│   └── test_repository.py
├── notebooks/
│   ├── 1_analisis_exploratorio.ipynb
│   └── 2_analisis_de_ventas.ipynb
├── .env
├── .gitignore
├── requirements.txt
└── README.md

## ⚙️ Configuración del entorno

1. Crear entorno virtual:
    python -m venv venv
    source venv/bin/activate (o venv\Scripts\activate en Windows)

2. Instalar dependencias:
    pip install -r requirements.txt

3. Archivo `.env`:

    DB_USER=root
    DB_PASSWORD=tu_password
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=proyecto_integrador

4. `.gitignore` debe incluir:

    .env

## 🧠 Patrón Singleton aplicado

Clase DBConnection:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")
            db = os.getenv("DB_NAME")

            cls._instance = super().__new__(cls)
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
            cls._instance.engine = create_engine(url)
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
        return cls._instance

    def get_session(self):
        return self.Session()

## 🔍 Consulta SQL desde Python

import pandas as pd
from src.db.database import DBConnection

def get_top_products(limit=10):
    session = DBConnection().get_session()
    query = f'''
        SELECT p.ProductName, SUM(s.Quantity) AS TotalSold
        FROM sales s
        JOIN products p ON s.ProductID = p.ProductID
        GROUP BY p.ProductName
        ORDER BY TotalSold DESC
        LIMIT {limit};
    '''
    df = pd.read_sql(query, session.bind)
    session.close()
    return df

## 🧪 Test Unitario

from src.db.database import DBConnection

def test_singleton_instance():
    db1 = DBConnection()
    db2 = DBConnection()
    assert db1 is db2

## 📓 Notebook de integración

Incluye:

- Verificación de conexión
- Ejecución de consultas
- Resultados visualizados
- Justificación de patrones
- Prueba unitaria visible

## ✅ Requisitos cumplidos

| Requisito                                           | Estado |
|-----------------------------------------------------|--------|
| Patrón Singleton implementado                       | ✅     |
| Clase de conexión con SQLAlchemy                    | ✅     |
| Consulta SQL con pandas                             | ✅     |
| Variables de entorno con dotenv                     | ✅     |
| .env ignorado por Git                               | ✅     |
| Test unitario del patrón                            | ✅     |
| Notebook completo con resultados visibles           | ✅     |

# 🧱 Proyecto Integrador – Fase 3: SQL Avanzado y Optimización

Este documento detalla los avances correspondientes a la **Fase 3 y final** del Proyecto Integrador. El objetivo de esta etapa fue refinar el sistema, moviendo la lógica de análisis compleja desde la aplicación Python hacia la base de datos PostgreSQL.

El principio rector de esta fase fue **"mover el cómputo a los datos, no los datos al cómputo"**. Se implementaron técnicas avanzadas de SQL para mejorar el rendimiento, la mantenibilidad y la eficiencia general del sistema de análisis.

---

## ✅ Objetivos de esta Fase

- **Crear y ejecutar consultas SQL avanzadas** utilizando **CTEs (Common Table Expressions)** y **Funciones de Ventana** (`ROW_NUMBER()`, `LAG()`).
- **Diseñar y crear al menos dos objetos programables en SQL** para encapsular lógica y simplificar el acceso a los datos. Se eligieron una **Vista** y un **Procedimiento Almacenado** por su alto impacto en la arquitectura.
- **Integrar la ejecución** de estas consultas y objetos desde la capa de datos de Python (`DataRepository`).
- **Documentar y presentar los resultados** en el Jupyter Notebook final, explicando las técnicas utilizadas y los insights obtenidos.
- **Actualizar la documentación final** del proyecto (`README.md`) para reflejar una arquitectura completa y profesional.

---

## 🏛️ Arquitectura y Decisiones de Ingeniería (Fase 3)

En esta fase, no se modificó la arquitectura de tres capas existente, sino que se **enriqueció la capa de datos (PostgreSQL)**, dándole más responsabilidades de análisis para que la aplicación Python pudiera ser más ligera y declarativa.

### 1. Consultas Analíticas Avanzadas

Para responder preguntas de negocio complejas, se implementaron dos consultas analíticas directamente en el `DataRepository`.

- **Ranking de Productos por Categoría:**
  - **Problema:** Identificar los productos "estrella" dentro de cada categoría. Un simple `GROUP BY` es insuficiente.
  - **Solución:** Se utilizó una **CTE** para pre-calcular las ventas por producto y luego la función de ventana **`ROW_NUMBER() OVER (PARTITION BY ...)`** para asignar un ranking a cada producto *dentro* de su categoría. Esto permite un filtrado trivial de los "Top N" productos.
  - **Beneficio:** El cálculo se realiza enteramente en la base de datos de forma muy eficiente, y Python solo recibe el resultado final ya procesado.

- **Análisis de Crecimiento Mensual:**
  - **Problema:** Calcular la tasa de crecimiento de ingresos mes a mes. Esto requiere comparar la fila de un mes con la del mes anterior.
  - **Solución:** Se usó la función de ventana **`LAG()`** para acceder a los ingresos del mes anterior en la misma fila del mes actual, permitiendo el cálculo del crecimiento porcentual directamente en la sentencia `SELECT`.
  - **Beneficio:** Evita la necesidad de traer toda la serie temporal a Pandas para luego hacer un `shift()` y calcular la diferencia, lo cual sería mucho menos performante.

### 2. Vista para Simplificación de Datos (`v_ventas_detalladas`)

- **Problema:** Las consultas de análisis a menudo requerían unir 5 o 6 tablas (`sales`, `customers`, `products`, `cities`, etc.), lo que resultaba en código SQL repetitivo, propenso a errores y difícil de mantener.
- **Solución:** Se creó una **VISTA** llamada `v_ventas_detalladas`. Una vista es una tabla virtual almacenada como una consulta `SELECT`. Esta vista contiene todos los `JOINs` pre-configurados.
- **Beneficio:** Ahora, en lugar de escribir `JOINs` complejos, cualquier consulta puede simplemente hacer un `SELECT` a esta vista como si fuera una tabla normal. Esto **abstrae la complejidad**, reduce errores y asegura consistencia en el acceso a los datos.

### 3. Procedimiento Almacenado para Lógica de Negocio (`sp_reporte_cliente`)

- **Problema:** Ciertas operaciones, como generar un reporte completo para un cliente específico, son una lógica de negocio común que se quiere reutilizar y que requiere un parámetro de entrada.
- **Solución:** Se creó un **PROCEDIMIENTO ALMACENADO** (implementado como una `FUNCTION` en PostgreSQL) que acepta un `CustomerID` como parámetro. Toda la lógica para calcular el total gastado, la categoría favorita y otros KPIs del cliente está encapsulada dentro de este procedimiento en el servidor.
- **Beneficio:**
  - **Rendimiento:** Reduce el tráfico de red, ya que la aplicación solo envía un ID y recibe un pequeño resultado final.
  - **Mantenibilidad:** La lógica de negocio del "reporte de cliente" está en un solo lugar. Si necesita cambiar, se modifica el procedimiento sin tocar la aplicación Python.
  - **Seguridad:** Limita el tipo de operaciones que la aplicación puede realizar, exponiendo solo la funcionalidad deseada.

---

## 📌 Desafío Clave: Calidad de Datos de Origen

- **El Problema:** Durante la implementación, se confirmó que la columna `sales.SalesDate` contenía datos de texto inválidos (ej. `"31:24.2"`) que impedían su tratamiento como un tipo `TIMESTAMP` nativo.
- **La Solución (Mitigación en la Vista):** Para solucionar esto sin alterar los datos crudos, se implementó una expresión `CASE WHEN ...` dentro de la `CREATE VIEW`. Esta lógica utiliza una expresión regular para validar el formato de la fecha en cada fila. Si el formato es válido, lo convierte a `TIMESTAMP`; si es inválido, lo convierte a `NULL`, evitando así que las consultas fallen.
- **Propuesta de Mejora (Estándar Industrial):** La solución definitiva y más robusta sería implementar un **script de ETL previo a la carga**. Este script, escrito en Python con Pandas, se encargaría de leer el CSV, limpiar y estandarizar la columna de fecha (`pd.to_datetime(..., errors='coerce')`), y guardar un `sales_cleaned.csv`. El proceso de carga en SQL se haría entonces desde este archivo limpio, permitiendo que la columna en la base de datos sea de tipo `TIMESTAMP` nativo, lo que garantizaría la máxima integridad y rendimiento.

---

## ▶️ Cómo Verificar el Avance 3

1. **Ejecutar los Objetos SQL:** En un cliente SQL, ejecutar el script `sql/3_advanced_objects.sql` para crear la Vista y el Procedimiento Almacenado.
2. **Ejecutar el Notebook de Análisis:** Abrir y ejecutar todas las celdas de `notebooks/2_analisis_de_ventas.ipynb`. Las nuevas secciones al final del notebook demostrarán:
   - La ejecución de las consultas de ranking y crecimiento mensual.
   - La llamada al procedimiento almacenado para generar un reporte de cliente dinámico.
   - El uso implícito de la vista en las nuevas consultas.

---

## ✔️ Checklist de Requisitos (Fase 3)

| Requisito                               | Estado      | Verificación                                          |
| --------------------------------------- | ----------- | ----------------------------------------------------- |
| Consultas con CTEs y Funciones Ventana  | ✅ Cumplido | Métodos en `repository.py` y resultados en notebook.  |
| Creación de Vista                       | ✅ Cumplido | `sql/3_advanced_objects.sql` y su uso en consultas.   |
| Creación de Procedimiento Almacenado    | ✅ Cumplido | `sql/3_advanced_objects.sql` y su uso desde Python.   |
| Integración de todo desde Python        | ✅ Cumplido | El notebook se ejecuta y llama a todos los métodos.   |
| Documentación en Notebook               | ✅ Cumplido | Celdas de Markdown explican cada paso del análisis.   |
| Documentación Final en `README.md`      | ✅ Cumplido | Este mismo documento.                                 |
