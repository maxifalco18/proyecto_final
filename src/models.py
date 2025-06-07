# src/models.py

from datetime import datetime, date

class Category:
    """
    Representa la tabla 'categories'.
    Cada producto pertenece a una categoría.
    """
    def __init__(self, CategoryID: int, CategoryName: str):
        self.CategoryID = CategoryID
        self.CategoryName = CategoryName

    def __repr__(self):
        return f"Category(ID={self.CategoryID}, Name='{self.CategoryName}')"

class Country:
    """
    Representa la tabla 'countries'.
    Contiene metadatos relacionados con los países.
    """
    def __init__(self, CountryID: int, CountryName: str, CountryCode: str):
        self.CountryID = CountryID
        self.CountryName = CountryName
        self.CountryCode = CountryCode

    def __repr__(self):
        return f"Country(ID={self.CountryID}, Name='{self.CountryName}')"

class City:
    """
    Representa la tabla 'cities'.
    Contiene datos geográficos a nivel de ciudad.
    Las ciudades están en un país.
    """
    def __init__(self, CityID: int, CityName: str, Zipcode: str, CountryID: int):
        self.CityID = CityID
        self.CityName = CityName
        self.Zipcode = Zipcode
        self.CountryID = CountryID # FK a countries.CountryID

    def __repr__(self):
        return f"City(ID={self.CityID}, Name='{self.CityName}')"

class Customer:
    """
    Representa la tabla 'customers'.
    Incluye información sobre los clientes que realizan compras.
    Un cliente vive en una ciudad y país.
    """
    def __init__(self, CustomerID: int, FirstName: str, LastName: str, CityID: int, CountryID: int, MiddleInitial: str = None, Address: str = None):
        self.CustomerID = CustomerID
        self.FirstName = FirstName
        self.MiddleInitial = MiddleInitial
        self.LastName = LastName
        self.Address = Address
        self.CityID = CityID # FK a cities.CityID
        self.CountryID = CountryID # FK a countries.CountryID

    @property
    def full_name(self) -> str:
        """
        Método personalizado para devolver el nombre completo del cliente.
        """
        if self.MiddleInitial:
            return f"{self.FirstName} {self.MiddleInitial}. {self.LastName}"
        return f"{self.FirstName} {self.LastName}"

    def __repr__(self):
        return f"Customer(ID={self.CustomerID}, Name='{self.full_name}')"

class Employee:
    """
    Representa la tabla 'employees'.
    Contiene detalles de los empleados que gestionan las ventas.
    Un empleado está asignado a una ciudad.
    """
    def __init__(self, EmployeeID: int, FirstName: str, LastName: str, CityID: int, HireDate: date, BirthDate: date, Gender: str = None, MiddleInitial: str = None):
        self.EmployeeID = EmployeeID
        self.FirstName = FirstName
        self.MiddleInitial = MiddleInitial
        self.LastName = LastName
        self.BirthDate = BirthDate
        self.Gender = Gender
        self.CityID = CityID # FK a cities.CityID
        self.HireDate = HireDate

    @property
    def full_name(self) -> str:
        """
        Método personalizado para devolver el nombre completo del empleado.
        """
        if self.MiddleInitial:
            return f"{self.FirstName} {self.MiddleInitial}. {self.LastName}"
        return f"{self.FirstName} {self.LastName}"

    def __repr__(self):
        return f"Employee(ID={self.EmployeeID}, Name='{self.full_name}')"

class Product:
    """
    Representa la tabla 'products'.
    Contiene información sobre los productos disponibles.
    """
    def __init__(self, ProductID: int, ProductName: str, Price: float, CategoryID: int, ModifyDate: date, Class: str = None, Resistant: str = None, IsAllergic: str = None, VitalityDays: int = None):
        self.ProductID = ProductID
        self.ProductName = ProductName
        self.Price = Price
        self.CategoryID = CategoryID # FK a categories.CategoryID
        self.Class = Class
        self.ModifyDate = ModifyDate
        self.Resistant = Resistant
        self.IsAllergic = IsAllergic
        self.VitalityDays = VitalityDays

    def __repr__(self):
        return f"Product(ID={self.ProductID}, Name='{self.ProductName}', Price={self.Price})"

class Sale:
    """
    Representa la tabla 'sales' (ventas).
    Almacena los datos transaccionales de cada venta.
    Una venta une un producto, un cliente y un vendedor.
    """
    def __init__(self, SalesID: int, SalesPersonID: int, CustomerID: int, ProductID: int, Quantity: int, Discount: float, TotalPrice: float, SalesDate: datetime, TransactionNumber: str):
        self.SalesID = SalesID
        self.SalesPersonID = SalesPersonID # FK a employees.EmployeeID
        self.CustomerID = CustomerID # FK a customers.CustomerID
        self.ProductID = ProductID # FK a products.ProductID
        self.Quantity = Quantity
        self.Discount = Discount
        self.TotalPrice = TotalPrice
        self.SalesDate = SalesDate
        self.TransactionNumber = TransactionNumber

    def __repr__(self):
        return f"Sale(ID={self.SalesID}, Transaction='{self.TransactionNumber}', Total=${self.TotalPrice})"