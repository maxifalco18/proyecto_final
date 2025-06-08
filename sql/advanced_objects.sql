-- ====================================================================
-- FASE 3: OBJETOS AVANZADOS DE LA BASE DE DATOS
-- ====================================================================

-- 1. VISTA PARA SIMPLIFICAR CONSULTAS (v_ventas_detalladas)
-- Propósito: Crear una tabla virtual que pre-una todas las tablas
-- relacionadas con las ventas. Esto simplifica enormemente las
-- consultas futuras, ya que evita la necesidad de escribir JOINs
-- complejos repetidamente.

CREATE OR REPLACE VIEW v_ventas_detalladas AS
SELECT
    s.SalesID,
    -- Usamos CASE para manejar fechas inválidas.
    -- La expresión regular '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}' verifica el formato YYYY-MM-DD HH:MI:SS.
    -- Si el formato es correcto, lo convierte. Si no, lo deja como NULL.
    CASE
        WHEN s.SalesDate ~ '^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
        THEN TO_TIMESTAMP(s.SalesDate, 'YYYY-MM-DD HH24:MI:SS.US')
        ELSE NULL
    END AS SalesDate,
    s.Quantity,
    s.Discount,
    s.TotalPrice,
    p.ProductName,
    p.Price AS ProductPrice,
    c.CategoryName,
    cust.FirstName AS CustomerFirstName,
    cust.LastName AS CustomerLastName,
    ci.CityName,
    co.CountryName
FROM
    sales s
JOIN products p ON s.ProductID = p.ProductID
JOIN categories c ON p.CategoryID = c.CategoryID
JOIN customers cust ON s.CustomerID = cust.CustomerID
JOIN cities ci ON cust.CityID = ci.CityID
JOIN countries co ON ci.CountryID = co.CountryID;

-- Ejemplo de uso de la vista:
-- SELECT * FROM v_ventas_detalladas WHERE CountryName = 'United States' LIMIT 10;


-- 2. PROCEDIMIENTO ALMACENADO PARA LÓGICA REUTILIZABLE (sp_reporte_cliente)
-- Propósito: Encapsular una lógica de negocio compleja y reutilizable.
-- Este procedimiento toma un ID de cliente y devuelve un informe completo
-- de su actividad, optimizando la consulta en el servidor.

DROP FUNCTION IF EXISTS sp_reporte_cliente(integer);

CREATE FUNCTION sp_reporte_cliente(p_customer_id INT)
RETURNS TABLE(
    nombre_completo VARCHAR,
    ciudad VARCHAR,
    total_gastado NUMERIC,
    total_compras BIGINT,
    fecha_ultima_compra TIMESTAMP,
    categoria_favorita VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_nombre_completo VARCHAR;
    v_ciudad VARCHAR;
BEGIN
    SELECT
        c.FirstName || ' ' || c.LastName,
        ci.CityName
    INTO
        v_nombre_completo,
        v_ciudad
    FROM
        customers c
    JOIN
        cities ci ON c.CityID = ci.CityID
    WHERE
        c.CustomerID = p_customer_id;

    RETURN QUERY
    WITH CustomerSales AS (
        SELECT
            v.TotalPrice,
            v.SalesDate,
            v.CategoryName
        FROM
            v_ventas_detalladas v
        JOIN customers c ON v.CustomerFirstName = c.FirstName AND v.CustomerLastName = c.LastName
        WHERE
            c.CustomerID = p_customer_id
    )
    SELECT
        v_nombre_completo,
        v_ciudad,
        SUM(cs.TotalPrice) AS total_gastado,
        COUNT(*) AS total_compras,
        MAX(cs.SalesDate)::TIMESTAMP AS fecha_ultima_compra,
        (SELECT CategoryName
         FROM CustomerSales
         GROUP BY CategoryName
         ORDER BY COUNT(*) DESC
         LIMIT 1) AS categoria_favorita
    FROM
        CustomerSales cs;
END;
$$;

-- Ejemplo de uso del procedimiento:
-- SELECT * FROM sp_reporte_cliente(1);