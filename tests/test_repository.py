import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.repository import DataRepository

@patch('src.repository.DatabaseConnection')
def test_get_sales_summary_with_mock_db(MockDatabaseConnection):
    """
    Prueba el método del repositorio sin conectar a una base de datos real.
    Utiliza un 'mock' para simular la conexión y la ejecución de la consulta.
    """
    # 1. Arrange (Preparar el escenario)
    # Crear un DataFrame falso que simula el resultado de la consulta
    fake_data = {
        'countryname': ['USA', 'Canada'],
        'totaltransactions': [100, 50],
        'totalrevenue': [5000.00, 2500.00]
    }
    fake_df = pd.DataFrame(fake_data)

    # Configurar el mock para que, cuando se use pd.read_sql, devuelva nuestro DataFrame falso
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection
    
    # Esta es la línea clave: interceptamos la llamada a `pd.read_sql`
    with patch('pandas.read_sql', return_value=fake_df) as mock_read_sql:
        
        # 2. Act (Ejecutar la acción a probar)
        repo = DataRepository()
        result_df = repo.get_sales_summary_by_country()

        # 3. Assert (Verificar el resultado)
        # Verificar que el método devolvió el DataFrame que esperábamos
        pd.testing.assert_frame_equal(result_df, fake_df)
        
        # Verificar que se llamó a la función `read_sql` con una consulta (un string)
        mock_read_sql.assert_called_once()
        assert isinstance(mock_read_sql.call_args[0][0], str) # El primer argumento debe ser un string (la query)