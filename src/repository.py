# src/repository.py

import pandas as pd
from src.database import DatabaseConnection

class DataRepository:
    """
    Capa de acceso a datos que centraliza todas las consultas SQL.
    Utiliza el patrón Repository para desacoplar la lógica de negocio
    de la fuente de datos.
    """
    def __init__(self):
        """
        El repositorio obtiene la instancia Singleton de la conexión a la BBDD.
        """
        self.db_connection = DatabaseConnection()
        self.engine = self.db_connection.get_engine()

    def get_sales_summary_by_country(self) -> pd.DataFrame:
        """
        (Fase 2) Ejecuta una consulta SQL simple para obtener un resumen de ventas por país.
        """
        query = """
            SELECT 
                co.CountryName,
                COUNT(s.SalesID) AS TotalTransactions,
                SUM(s.TotalPrice) AS TotalRevenue
            FROM sales s
            JOIN customers c ON s.CustomerID = c.CustomerID
            JOIN cities ci ON c.CityID = ci.CityID
            JOIN countries co ON ci.CountryID = co.CountryID
            GROUP BY co.CountryName
            ORDER BY TotalRevenue DESC;
        """
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(query, connection)
            return df
        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return pd.DataFrame()

    # --- MÉTODOS NUEVOS DE LA FASE 3 ---

    def get_top_products_per_category(self, limit: int = 3) -> pd.DataFrame:
        """
        (Fase 3) Obtiene los N productos más vendidos por categoría usando CTEs y Funciones de Ventana.
        """
        query = """
            WITH ProductSales AS (
                SELECT
                    s.ProductID,
                    SUM(s.Quantity) as TotalQuantitySold
                FROM sales s
                GROUP BY s.ProductID
            ),
            RankedProducts AS (
                SELECT
                    c.CategoryName,
                    p.ProductName,
                    ps.TotalQuantitySold,
                    ROW_NUMBER() OVER(PARTITION BY c.CategoryID ORDER BY ps.TotalQuantitySold DESC) as Rank
                FROM products p
                JOIN categories c ON p.CategoryID = c.CategoryID
                JOIN ProductSales ps ON p.ProductID = ps.ProductID
            )
            SELECT
                rp.CategoryName,
                rp.ProductName,
                rp.TotalQuantitySold
            FROM RankedProducts rp
            WHERE rp.Rank <= %(limit)s
            ORDER BY rp.CategoryName, rp.TotalQuantitySold DESC;
        """
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(query, connection, params={'limit': limit})
            return df
        except Exception as e:
            print(f"Error al obtener el top de productos: {e}")
            return pd.DataFrame()

    def get_monthly_sales_growth(self) -> pd.DataFrame:
        """
        (Fase 3) Calcula el crecimiento de ventas mensual usando CTEs y la función de ventana LAG().
        """
        query = """
            WITH MonthlySales AS (
                SELECT
                    DATE_TRUNC('month', SalesDate) AS SaleMonth,
                    SUM(TotalPrice) AS MonthlyRevenue
                FROM v_ventas_detalladas -- Usamos nuestra nueva VISTA para simplificar
                WHERE SalesDate IS NOT NULL
                GROUP BY SaleMonth
                ORDER BY SaleMonth
            )
            SELECT
                to_char(ms.SaleMonth, 'YYYY-MM') AS SaleMonth,
                ms.MonthlyRevenue,
                LAG(ms.MonthlyRevenue, 1, 0) OVER (ORDER BY ms.SaleMonth) AS PreviousMonthRevenue,
                (ms.MonthlyRevenue - LAG(ms.MonthlyRevenue, 1, 0) OVER (ORDER BY ms.SaleMonth)) / NULLIF(LAG(ms.MonthlyRevenue, 1, 0) OVER (ORDER BY ms.SaleMonth), 0) * 100 AS GrowthPercentage
            FROM MonthlySales ms;
        """
        try:
            with self.engine.connect() as connection:
                df = pd.read_sql(query, connection)
            return df
        except Exception as e:
            print(f"Error al calcular el crecimiento mensual: {e}")
            return pd.DataFrame()

    def get_customer_report(self, customer_id: int) -> pd.DataFrame:
        """
        (Fase 3) Ejecuta el Procedimiento Almacenado 'sp_reporte_cliente' para obtener
        un informe de actividad de un cliente específico.
        """
        try:
            with self.engine.connect() as connection:
                # Este método no contiene SQL complejo, solo llama al procedimiento.
                # Usamos f-string de forma segura porque customer_id es un entero.
                query = f"SELECT * FROM sp_reporte_cliente({customer_id});"
                df = pd.read_sql_query(query, connection)
            return df
        except Exception as e:
            print(f"Error al generar el reporte de cliente: {e}")
            return pd.DataFrame()