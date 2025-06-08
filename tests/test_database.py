import pytest
from src.database import DatabaseConnection

def test_singleton_instance():
    """Verifica que DatabaseConnection siempre devuelve la misma instancia del motor."""
    conn1 = DatabaseConnection()
    conn2 = DatabaseConnection()

    assert conn1 is conn2
    assert conn1.get_engine() is conn2.get_engine()