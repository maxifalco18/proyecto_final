-- ====================================================================
-- SCRIPT SEGURO PARA ACTUALIZAR 'products' (VERSIÓN FINAL CON TRANSFORMACIÓN EN SQL)
-- ====================================================================

-- Paso 1: Crear una copia de seguridad/tabla beta de 'products'.
DROP TABLE IF EXISTS products_beta;
CREATE TABLE products_beta AS SELECT * FROM products;

-- Paso 2: Crear la tabla temporal (staging).
DROP TABLE IF EXISTS products_staging;
CREATE TEMP TABLE products_staging (
    ProductID      INT PRIMARY KEY,
    ProductName    VARCHAR(100),
    Price          NUMERIC(10,2),
    CategoryID     INT,
    Class          VARCHAR(50),
    -- IMPORTANTE: Cargamos la fecha como TEXTO para que coincida con el CSV.
    ModifyDate     TEXT,
    Resistant      VARCHAR(20),
    IsAllergic     VARCHAR(20),
    VitalityDays   INT
);

-- Paso 3: Cargar los datos del CSV limpio en la tabla temporal.
-- Este comando ahora funcionará porque estamos copiando TEXTO a una columna de TEXTO.
COPY products_staging(ProductID, ProductName, Price, CategoryID, Class, ModifyDate, Resistant, IsAllergic, VitalityDays)
FROM '/data/products_cleaned.csv'
DELIMITER ',' CSV HEADER;

-- Paso 4: Actualizar la tabla 'products_beta' con la transformación de fecha.
UPDATE products_beta p_beta
SET
    ProductName = s.ProductName,
    Price = s.Price,
    CategoryID = s.CategoryID,
    Class = s.Class,
    -- ¡AQUÍ OCURRE LA MAGIA!
    -- Reconstruimos la fecha completa a partir del texto y luego la formateamos
    -- para guardarla en la columna de texto de la tabla beta.
    ModifyDate = TO_CHAR(
        '2023-01-01'::timestamp + -- Nuestra fecha base
        (split_part(s.ModifyDate, ':', 1) || ' hours')::interval + -- Extrae las horas
        (split_part(split_part(s.ModifyDate, ':', 2), '.', 1) || ' minutes')::interval + -- Extrae los minutos
        ( ('0.' || split_part(split_part(s.ModifyDate, ':', 2), '.', 2))::float * 60 || ' seconds' )::interval, -- Extrae y calcula los segundos
        'YYYY-MM-DD HH24:MI:SS'
    ),
    Resistant = s.Resistant,
    IsAllergic = s.IsAllergic,
    VitalityDays = s.VitalityDays
FROM
    products_staging s
WHERE
    p_beta.ProductID = s.ProductID;

-- Paso 5: ¡Verificar y Comparar!
SELECT
    p.ProductID,
    p.ModifyDate AS Original_ModifyDate,
    p_beta.ModifyDate AS Beta_ModifyDate_Reconstructed
FROM
    products p
JOIN
    products_beta p_beta ON p.ProductID = p_beta.ProductID
WHERE
    p.ProductID IN (1, 2, 3, 4, 5);