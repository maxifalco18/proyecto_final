# 🚀 Proyecto Integrador – Sistema de Análisis de Ventas
---

# 🧱 Proyecto Integrador – Avance 1: Estructura y Carga de Datos

Este repositorio corresponde al **Avance 1** del Proyecto Integrador de Henry. El objetivo de esta fase inicial fue establecer los cimientos de un sistema de análisis de ventas, aplicando conceptos fundamentales de bases de datos, programación orientada a objetos (POO) y buenas prácticas de ingeniería de software.

El trabajo realizado en esta etapa es la base sobre la cual se construirán las funcionalidades más complejas en fases posteriores.

---

## ✅ Objetivos Cumplidos en esta Fase

-   **Estructurar el proyecto** con una organización de carpetas lógica y escalable.
-   **Modelar las entidades del negocio** (`Product`, `Customer`, etc.) como clases en Python, aplicando principios de POO.
-   **Crear un esquema de base de datos relacional** en PostgreSQL, garantizando la integridad de los datos con claves primarias y foráneas.
-   **Cargar un conjunto de datos** desde archivos `.csv` a la base de datos de manera eficiente.
-   **Validar la carga de datos** para asegurar que la ingesta fue exitosa.
-   **Implementar pruebas unitarias** simples con `pytest` para verificar la correcta instanciación de los modelos.

---

## 🗂️ Estructura del Proyecto

Se implementó una estructura de directorios estándar en la industria para garantizar la **modularidad y la separación de conceptos (Separation of Concerns)**.

```
proyecto_integrador/
├── data/                     # Contiene los archivos CSV de entrada.
├── notebooks/
│   ├── 1_analisis_exploratorio.ipynb # <-- Notebook inicial para la exploración y validación de datos.
│                   
├── src/                      # Código fuente principal de la aplicación.
│   ├── __init__.py           # Permite que 'src' sea tratado como un paquete de Python.
│   └── models.py             # Define las clases POO que representan las tablas.
├── sql/                      # Almacena todos los scripts SQL.
│   └── load_data.sql         # Script para la creación de tablas y carga de datos.
├── tests/                    # Contiene las pruebas unitarias del proyecto.
│   └── test_models.py        # Pruebas para las clases definidas en models.py.
├── .env                      # Archivo para almacenar variables de entorno (no versionado).
├── .gitignore                # Especifica los archivos a ignorar por Git.
├── requirements.txt          # Lista de dependencias de Python del proyecto.
└── README.md                 # Este archivo de documentación.
```

---

## 🏛️ Decisiones de Diseño y Arquitectura (Fase 1)

#### 1. Elección de la Base de Datos: PostgreSQL en Docker
-   **Decisión:** Se optó por **PostgreSQL** por ser una base de datos relacional de código abierto, robusta y muy potente, ideal para análisis de datos.
-   **Justificación:** Utilizar **Docker** para ejecutar la base de datos garantiza un entorno de desarrollo **100% reproducible y aislado**. Cualquier persona que clone el repositorio puede levantar una instancia idéntica de la base de datos con un solo comando, eliminando problemas de configuración local.

#### 2. Carga de Datos: Comando `COPY`
-   **Decisión:** Para cargar los datos desde los archivos `.csv` a las tablas de PostgreSQL, se utilizó el comando `COPY` nativo de PostgreSQL en lugar de múltiples sentencias `INSERT`.
-   **Justificación:** `COPY` es órdenes de magnitud **más rápido y eficiente** para cargas masivas, ya que está optimizado para leer un flujo de datos directamente desde un archivo. Esto es una práctica estándar en la ingeniería de datos para la ingesta inicial.

#### 3. Modelado de Datos: Programación Orientada a Objetos (POO)
-   **Decisión:** Cada tabla del esquema relacional (`countries`, `products`, `sales`, etc.) fue modelada como una clase en Python dentro del archivo `src/models.py`.
-   **Justificación:** Este enfoque permite trabajar con los datos de una manera más intuitiva y alineada con el negocio. En lugar de manejar filas como tuplas o diccionarios genéricos, operamos con objetos (`Product`, `Customer`) que tienen atributos y métodos propios. Esto mejora la legibilidad, el mantenimiento y la reutilización del código. Se implementaron métodos `__repr__` para facilitar la depuración y métodos de negocio como `full_name`.

#### 4. Pruebas Unitarias con `pytest`
-   **Decisión:** Se implementaron pruebas básicas para validar la correcta creación de los objetos de nuestras clases.
-   **Justificación:** Introducir pruebas desde la primera fase establece una cultura de calidad y robustez. Asegura que los componentes básicos del sistema funcionan como se espera y proporciona una red de seguridad para futuros cambios.

---

## ▶️ Cómo Ejecutar y Validar el Avance 1

### 1. Prerrequisitos
-   Tener `git`, `Python 3.8+` y `Docker` instalados.

### 2. Configuración del Entorno
```bash
# 1. Clona el repositorio
git clone https://github.com/maxifalco18/proyecto_final
cd proyecto_integrador

# 2. Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt
```

### 3. Levantar la Base de Datos y Cargar los Datos
```bash
# 1. Levanta el contenedor de PostgreSQL con Docker
docker run --name pg-integrador -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=admin123 -e POSTGRES_DB=proyecto_integrador -p 5432:5432 -d postgres:15

# 2. Copia los archivos CSV al contenedor
docker cp ./data/. pg-integrador:/data

# 3. Ejecuta el script SQL
# Abre tu cliente de base de datos preferido (DBeaver, DataGrip, etc.),
# conéctate a la base de datos en Docker y ejecuta el contenido completo
# del archivo 'sql/load_data.sql'.
```

### 4. Correr las Pruebas Unitarias
Para verificar que los modelos POO funcionan correctamente:
```bash
pytest -v tests/test_models.py
```
**Resultado Esperado:** Todas las pruebas deben pasar (`PASSED`), confirmando que los objetos se instancian con los atributos correctos.

---

## 📌 Desafíos y Notas Finales

-   **Calidad de Datos:** Durante la carga, se identificaron problemas de formato en las columnas de fecha (`SalesDate`, `ModifyDate`), que contenían valores inválidos.
-   **Solución Temporal:** Para permitir la carga inicial, estas columnas se definieron como de tipo `TEXT` en la base de datos. Se documentó que este es un punto de "deuda técnica" a resolver en fases posteriores mediante un proceso de limpieza de datos (ETL).
-   **Integridad Referencial:** Se establecieron relaciones con claves foráneas (`FOREIGN KEY`) en el script de creación de tablas para garantizar la consistencia y la integridad de los datos a nivel de base de datos.
-   **Validación de Carga:** El script `load_data.sql` incluye sentencias `SELECT COUNT(*)` para cada tabla, permitiendo una validación rápida y directa de que todos los registros de los CSVs fueron cargados correctamente.

¡Por supuesto! Aquí tienes un `README.md` súper completo y descriptivo, enfocado exclusivamente en el **Avance 2**.

Este documento está diseñado para que un evaluador pueda entender en profundidad las decisiones de arquitectura y diseño que tomaste en esta fase, demostrando tu capacidad para construir software modular, mantenible y profesional.

---

# 🚀 Proyecto Integrador – Avance 2: Modularización y Patrones de Diseño

Este documento detalla los avances correspondientes a la **Fase 2** del Proyecto Integrador. El foco de esta etapa fue transformar la base estática del proyecto en una **aplicación Python dinámica, modular y robusta**. Se aplicaron patrones de diseño de software para construir una solución escalable y desacoplada, siguiendo las mejores prácticas de la industria.

---

## ✅ Objetivos Cumplidos en esta Fase

-   **Modularizar el sistema** para desacoplar la lógica de negocio del acceso a los datos.
-   Implementar una **clase de conexión** a la base de datos aplicando el patrón de diseño **Singleton** para una gestión eficiente de recursos.
-   Crear una **capa de acceso a datos** con el patrón **Repository** para centralizar todas las consultas SQL.
-   Ejecutar consultas desde Python y **formatear los resultados como DataFrames de Pandas** para facilitar el análisis.
-   **Proteger las credenciales** de la base de datos de forma segura utilizando un archivo `.env`.
-   **Integrar la arquitectura completa** en un Jupyter Notebook funcional que demuestre el flujo de datos.
-   Añadir **pruebas unitarias avanzadas** para los patrones implementados, utilizando **mocks** para garantizar pruebas aisladas y rápidas.

---

## 🗂️ Arquitectura de la Aplicación (Fase 2)

La estructura del proyecto fue extendida para soportar la nueva lógica de la aplicación. Los archivos clave de esta fase son:

```
proyecto_integrador/
├── data/
│   └── ...
├── notebooks/
|   ├── 1_analisis_exploratorio.ipynb # <-- Notebook inicial para la exploración y validación de datos.
│   └── 2_analisis_de_ventas.ipynb   # <-- NUEVO: Notebook de integración que usa el Repository.
├── src/
│   ├── __init__.py
│   ├── database.py                # <-- NUEVO: Gestor de conexión (Implementa Singleton).
│   ├── models.py
│   └── repository.py              # <-- NUEVO: Capa de acceso a datos (Implementa Repository).
├── sql/
│   └── load_data.sql
├── tests/
│   ├── __init__.py
│   ├── test_database.py           # <-- NUEVO: Prueba unitaria para el patrón Singleton.
│   ├── test_models.py
│   └── test_repository.py         # <-- NUEVO: Prueba unitaria para el Repository (con Mocks).
├── .env
├── requirements.txt               # (Actualizado con sqlalchemy, etc.)
└── README.md
```

---

## 🏛️ Decisiones de Ingeniería y Diseño (Fase 2)

En esta fase, se tomaron decisiones de arquitectura clave para elevar la calidad del software.

#### 1. Patrón Singleton para la Conexión (`src/database.py`)
-   **Problema a Resolver:** Crear una conexión a la base de datos es una operación costosa en términos de tiempo y recursos. Si cada componente de la aplicación (o cada llamada) creara su propia conexión, el rendimiento se degradaría rápidamente y se podrían agotar los recursos del servidor.
-   **Solución Implementada:** Se implementó el patrón **Singleton** en la clase `DatabaseConnection`. Este patrón garantiza que, sin importar cuántas veces se solicite una conexión en la aplicación, solo se cree **una única instancia** del motor de SQLAlchemy. Este motor gestiona un *pool* de conexiones que se reutilizan de manera eficiente.
-   **Justificación Técnica:** Esta decisión optimiza el rendimiento, reduce la latencia y asegura una gestión de recursos predecible y centralizada.

#### 2. Patrón Repository para el Acceso a Datos (`src/repository.py`)
-   **Problema a Resolver:** Mezclar consultas SQL directamente en la lógica de negocio (por ejemplo, dentro de un notebook) crea un código fuertemente acoplado. Esto lo hace difícil de leer, mantener y, sobre todo, probar.
-   **Solución Implementada:** Se creó la clase `DataRepository`, que actúa como una **capa de abstracción** entre la aplicación y la base de datos. Esta clase es la única responsable de construir y ejecutar consultas SQL. Expone métodos con nombres claros y relacionados con el negocio (ej. `get_sales_summary_by_country()`).
-   **Justificación Técnica:** Este patrón **desacopla** la lógica de la aplicación de la tecnología de la base de datos. Si en el futuro la base de datos cambiara (ej. de PostgreSQL a MySQL) o los datos vinieran de una API, solo tendríamos que modificar el `DataRepository`. El resto de la aplicación seguiría funcionando sin cambios, lo que demuestra una arquitectura flexible y mantenible.

#### 3. Pruebas Unitarias con Mocks (`tests/test_repository.py`)
-   **Problema a Resolver:** Las pruebas unitarias deben ser rápidas, fiables y no depender de sistemas externos como una base de datos. Probar el `DataRepository` contra una base de datos real sería una prueba de integración, no unitaria, y sería lenta y frágil.
-   **Solución Implementada:** Se utilizó la librería `unittest.mock` de Python para **simular (mockear)** la conexión a la base de datos. Creamos un objeto falso que imita el comportamiento de la conexión y le indicamos qué datos falsos debe devolver.
-   **Justificación Técnica:** Esto nos permite probar la lógica del `DataRepository` (si construye bien las consultas, si procesa los resultados, etc.) en **total aislamiento**, sin necesidad de tener Docker corriendo o una conexión de red activa. Las pruebas son rápidas, deterministas y se centran en validar una única unidad de código.

---

## ▶️ Cómo Ejecutar y Validar el Avance 2

Esta guía asume que la configuración de la **Fase 1** (base de datos en Docker creada y cargada) ha sido completada.

1.  **Actualizar Dependencias:** `pip install -r requirements.txt`
2.  **Configurar `.env`:** Asegurarse de que el archivo `.env` exista en la raíz del proyecto con las credenciales correctas.

#### Ejecutar el Análisis de Integración:
-   **Acción:** Abrir y ejecutar todas las celdas del notebook `notebooks/2_analisis_de_ventas.ipynb`.
-   **Resultado Esperado:** El notebook debe ejecutarse de principio a fin sin errores, mostrando mensajes de inicialización, un **DataFrame de Pandas** con el resumen de ventas y una **visualización gráfica** de los resultados. Esto demuestra que todas las capas de la arquitectura se comunican correctamente.

#### Ejecutar las Pruebas Unitarias:
-   **Acción:** Correr el siguiente comando en la terminal: `pytest -v tests/`
-   **Resultado Esperado:** Todas las pruebas deben pasar (`PASSED`), confirmando que los patrones Singleton y Repository, así como su lógica interna, funcionan como se esperaba de forma aislada.

---

## ✔️ Checklist de Requisitos (Fase 2)

| Requisito                            | Estado    | Verificación                                     |
| ------------------------------------ | --------- | ------------------------------------------------ |
| Modularización y Patrones de Diseño  | ✅ Cumplido | Revisión de `src/database.py` y `src/repository.py`. |
| Clase de conexión con Singleton      | ✅ Cumplido | `pytest tests/test_database.py` pasa.            |
| Ejecución de consultas desde Python  | ✅ Cumplido | El notebook `2_analisis...` muestra resultados. |
| Resultados como DataFrame de Pandas  | ✅ Cumplido | El notebook muestra un DataFrame.                |
| Notebook de integración funcional    | ✅ Cumplido | Ejecución completa del notebook sin errores.     |
| Pruebas unitarias para patrones      | ✅ Cumplido | `pytest tests/test_repository.py` pasa.          |
| Seguridad de credenciales con `.env` | ✅ Cumplido | La conexión funciona leyendo desde `.env`.       |

¡Absolutamente! Aquí tienes un `README.md` súper completo y descriptivo, enfocado exclusivamente en el **Avance 3**.

Este documento está diseñado para que un evaluador pueda entender en profundidad las decisiones de ingeniería, los desafíos y los logros de esta etapa final de optimización, demostrando tu dominio de técnicas avanzadas de SQL y arquitectura de datos.

---

# 🚀 Proyecto Integrador – Avance 3: SQL Avanzado y Optimización

Este documento detalla los avances correspondientes a la **Fase 3 y final** del Proyecto Integrador. El objetivo de esta etapa fue refinar y optimizar el sistema, moviendo la lógica de análisis compleja desde la aplicación Python hacia la base de datos PostgreSQL.

El principio rector de esta fase fue **"mover el cómputo a los datos, no los datos al cómputo"**. Se implementaron técnicas avanzadas de SQL para mejorar significativamente el rendimiento, la mantenibilidad y la eficiencia del sistema de análisis.

---

## ✅ Objetivos Cumplidos en esta Fase

-   **Crear y ejecutar consultas SQL analíticas avanzadas** utilizando **CTEs (Common Table Expressions)** y **Funciones de Ventana** (`ROW_NUMBER()`, `LAG()`).
-   **Diseñar y crear dos objetos programables en SQL** para encapsular lógica y simplificar el acceso a los datos. Se implementaron una **Vista** y un **Procedimiento Almacenado**.
-   **Integrar la ejecución** de estas nuevas consultas y objetos desde la capa de datos de Python (`DataRepository`).
-   **Documentar y presentar los resultados** en el Jupyter Notebook final, explicando las técnicas utilizadas y los insights obtenidos.
-   **Resolver desafíos de calidad de datos** identificados en fases anteriores, específicamente con las columnas de fecha.
-   **Actualizar la documentación final** del proyecto (`README.md`) para reflejar una arquitectura completa y profesional.

---

## 🗂️ Arquitectura y Ficheros Clave (Fase 3)

La arquitectura de tres capas se mantuvo, pero la **capa de datos (PostgreSQL)** fue significativamente enriquecida.

```
proyecto_integrador/
├── data/
│   ├── products_cleaned.csv       # <-- NUEVO: Archivo generado por el proceso de limpieza.
│   └── ...
├── notebooks/
|   ├── 1_analisis_exploratorio.ipynb # <-- Notebook inicial para la exploración y validación de datos.
│   └── 2_analisis_de_ventas.ipynb   # <-- NUEVO: Notebook de integración que 
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   └── repository.py              # (Actualizado con métodos para llamar a las queries avanzadas).
├── sql/
│   ├── load_data.sql
│   ├── 3_advanced_objects.sql     # <-- NUEVO: Script para crear Vistas y Procedimientos Almacenados.
│   └── 4_update_products_from_cleaned_csv.sql # <-- NUEVO: Script para el experimento de actualización.
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_models.py
│   └── test_repository.py
├── .env
├── requirements.txt
└── README.md
```
### Justificación de esta Estructura

-   **`notebooks/`**: La carpeta ahora muestra una progresión lógica.
    -   `1_analisis_exploratorio.ipynb`: Representa el trabajo de la **Fase 1**, donde se realiza un primer contacto con los datos, se validan las cargas y se realizan pruebas iniciales de conexión. Es un entregable que demuestra el proceso de descubrimiento.
    -   `2_analisis_de_ventas.ipynb`: Es el **informe final y la demostración principal** del proyecto. No contiene lógica de conexión ni SQL complejo; su único propósito es consumir la aplicación a través del `DataRepository` y presentar los análisis avanzados de la **Fase 2 y 3**.
---

## 🏛️ Decisiones de Ingeniería y Diseño (Fase 3)

En esta fase, se delegó la responsabilidad del análisis complejo a la base de datos, que está diseñada para manejar estas operaciones de manera óptima.

#### 1. Consultas Analíticas Avanzadas

Para responder preguntas de negocio que van más allá de simples agregaciones, se implementaron dos consultas analíticas clave:

-   **Ranking de Productos por Categoría:**
    -   **Problema:** Identificar los productos "estrella" dentro de cada categoría. Un simple `GROUP BY` no puede rankear resultados dentro de un grupo.
    -   **Solución:** Se utilizó una **CTE** para pre-calcular las ventas por producto y luego la función de ventana **`ROW_NUMBER() OVER (PARTITION BY ...)`** para asignar un ranking a cada producto *dentro* de su categoría. Esto permite un filtrado trivial de los "Top N" productos.
    -   **Justificación:** Esta técnica es estándar para problemas de ranking y es extremadamente eficiente, ya que evita múltiples consultas o un procesamiento complejo en Python.

-   **Análisis de Crecimiento Mensual:**
    -   **Problema:** Calcular la tasa de crecimiento de ingresos mes a mes, lo que requiere comparar la fila de un mes con la del mes anterior.
    -   **Solución:** Se usó la función de ventana **`LAG()`** para acceder a los ingresos del mes anterior en la misma fila del mes actual, permitiendo el cálculo del crecimiento porcentual directamente en la sentencia `SELECT`.
    -   **Justificación:** `LAG()` es la herramienta nativa de SQL para este tipo de análisis de series temporales. Es mucho más performante que traer toda la serie de datos a Pandas para luego hacer un `shift()` y calcular la diferencia.

#### 2. Vista para Simplificación de Datos (`v_ventas_detalladas`)

-   **Problema:** Las consultas de análisis a menudo requerían unir 5 o 6 tablas (`sales`, `customers`, `products`, etc.), lo que resultaba en código SQL repetitivo, propenso a errores y difícil de mantener.
-   **Solución:** Se creó una **VISTA** llamada `v_ventas_detalladas`. Una vista es una tabla virtual almacenada como una consulta `SELECT` que contiene todos los `JOINs` pre-configurados.
-   **Justificación:** La vista **abstrae la complejidad**. Ahora, en lugar de escribir `JOINs` complejos, cualquier consulta puede simplemente hacer un `SELECT` a esta vista como si fuera una tabla normal. Esto reduce errores, asegura consistencia y simplifica radicalmente el desarrollo de nuevas consultas.

#### 3. Procedimiento Almacenado para Lógica de Negocio (`sp_reporte_cliente`)

-   **Problema:** Ciertas operaciones, como generar un reporte completo para un cliente específico, representan una lógica de negocio común que es reutilizable y requiere un parámetro de entrada.
-   **Solución:** Se creó un **PROCEDIMIENTO ALMACENADO** (implementado como una `FUNCTION` en PostgreSQL) que acepta un `CustomerID` como parámetro. Toda la lógica para calcular el total gastado, la categoría favorita y otros KPIs del cliente está encapsulada dentro de este procedimiento en el servidor.
-   **Justificación:**
    -   **Rendimiento:** Reduce el tráfico de red, ya que la aplicación solo envía un ID y recibe un pequeño resultado final.
    -   **Mantenibilidad:** La lógica de negocio del "reporte de cliente" está en un solo lugar. Si necesita cambiar, se modifica el procedimiento sin tocar la aplicación Python.
    -   **Seguridad y Reutilización:** Expone una funcionalidad de negocio clara y segura que puede ser utilizada por diferentes partes de la aplicación o incluso por otros sistemas.

---

## 📌 Desafío Clave: Calidad de Datos de Origen

-   **El Problema:** Se confirmó que las columnas de fecha (`SalesDate`, `ModifyDate`) contenían datos de texto con formatos inválidos (ej. `"31:24.2"`), lo que impedía su tratamiento como un tipo `TIMESTAMP` nativo.
-   **La Solución Implementada:** Se abordó este problema de "deuda técnica" directamente en la capa de SQL.
    1.  **En la Vista:** Se implementó una expresión `CASE WHEN ...` que utiliza expresiones regulares para validar el formato de la fecha en cada fila. Si el formato es válido, lo convierte a `TIMESTAMP`; si es inválido, lo convierte a `NULL`, evitando que las consultas fallen.
    2.  **En el Script de Actualización (Experimento):** Se diseñó un script (`4_update_products_from_cleaned_csv.sql`) que utiliza un patrón de "staging table" para actualizar los datos desde un CSV limpio. Este script contiene la lógica SQL para parsear y reconstruir las fechas a partir de los deltas de tiempo (ej. `HH:MM.f`), demostrando una solución completa al problema.

---

## ▶️ Cómo Verificar el Avance 3

1.  **Ejecutar los Objetos SQL:** En un cliente SQL, ejecutar el script `sql/3_advanced_objects.sql` para crear la Vista y el Procedimiento Almacenado.
2.  **Ejecutar el Notebook de Análisis:** Abrir y ejecutar todas las celdas de `notebooks/2_analisis_de_ventas.ipynb`. Las nuevas secciones al final del notebook demostrarán:
    -   La ejecución de las consultas de ranking y crecimiento mensual.
    -   La llamada al procedimiento almacenado para generar un reporte de cliente dinámico.
    -   El uso implícito de la vista en las nuevas consultas, que ahora se ejecutan sin errores de fecha.

---

## ✔️ Checklist de Requisitos (Fase 3)

| Requisito                               | Estado    | Verificación                                     |
| --------------------------------------- | --------- | ------------------------------------------------ |
| Consultas con CTEs y Funciones Ventana  | ✅ Cumplido | Métodos en `repository.py` y resultados en notebook. |
| Creación de Vista                       | ✅ Cumplido | `sql/3_advanced_objects.sql` y su uso en consultas. |
| Creación de Procedimiento Almacenado    | ✅ Cumplido | `sql/3_advanced_objects.sql` y su uso desde Python. |
| Integración de todo desde Python        | ✅ Cumplido | El notebook se ejecuta y llama a todos los métodos. |
| Documentación en Notebook               | ✅ Cumplido | Celdas de Markdown explican cada paso del análisis. |
| Documentación Final en `README.md`      | ✅ Cumplido | Este mismo documento.                            |