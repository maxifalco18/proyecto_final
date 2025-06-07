
# 🧱 Proyecto Integrador – Avance 1

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
