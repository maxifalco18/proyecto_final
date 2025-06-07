import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Product, Customer

def test_product_creation():
    """
    Prueba que un objeto Producto se inicializa correctamente.
    """
    p = Product(
        ProductID=101,
        ProductName="Manzana",
        Price=1.50,
        CategoryID=5,
        ModifyDate=None  # Campo obligatorio en tu clase actual
    )
    assert p.ProductID == 101
    assert p.ProductName == "Manzana"
    assert p.Price == 1.50
    assert p.CategoryID == 5

def test_customer_full_name():
    """
    Prueba el método personalizado 'full_name' de la clase Customer.
    """
    c = Customer(
        CustomerID=1,
        FirstName="Juan",
        MiddleInitial=None,
        LastName="Perez",
        Address=None,
        CityID=10,
        CountryID=20
    )
    assert c.full_name == "Juan Perez"
