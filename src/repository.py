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
        Esto es un ejemplo de Inyección de Dependencias.
        """
        self.db_connection = DatabaseConnection()
        self.engine = self.db_connection.get_engine()

    def get_sales_summary_by_country(self) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL simple para obtener un resumen de ventas por país
        y devuelve el resultado como un DataFrame de pandas.
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
            return pd.DataFrame() # Devuelve un DataFrame vacío en caso de error