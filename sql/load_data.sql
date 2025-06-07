-- ====================================
-- 1. CREACIÓN DE TABLAS
-- ====================================

CREATE TABLE countries (
    CountryID       INT PRIMARY KEY,
    CountryName     VARCHAR(100),
    CountryCode     VARCHAR(10)
);

CREATE TABLE cities (
    CityID      INT PRIMARY KEY,
    CityName    VARCHAR(100),
    Zipcode     VARCHAR(20),
    CountryID   INT REFERENCES countries(CountryID)
);

CREATE TABLE categories (
    CategoryID      INT PRIMARY KEY,
    CategoryName    VARCHAR(100)
);

CREATE TABLE products (
    ProductID      INT PRIMARY KEY,
    ProductName    VARCHAR(100),
    Price          NUMERIC(10,2),
    CategoryID     INT REFERENCES categories(CategoryID),
    Class          VARCHAR(50),
    ModifyDate     TEXT,          -- Ajustado desde TIME
    Resistant      VARCHAR(20),
    IsAllergic     VARCHAR(20),
    VitalityDays   INT
);

CREATE TABLE customers (
    CustomerID      INT PRIMARY KEY,
    FirstName       VARCHAR(50),
    MiddleInitial   VARCHAR(5),
    LastName        VARCHAR(50),
    CityID          INT REFERENCES cities(CityID),
    Address         TEXT
);

CREATE TABLE employees (
    EmployeeID      INT PRIMARY KEY,
    FirstName       VARCHAR(50),
    MiddleInitial   VARCHAR(5),
    LastName        VARCHAR(50),
    BirthDate       TIMESTAMP,    -- TIMESTAMP para aceptar hora
    Gender          VARCHAR(10),
    CityID          INT REFERENCES cities(CityID),
    HireDate        TIMESTAMP     -- TIMESTAMP para aceptar hora
);

CREATE TABLE sales (
    SalesID           INT PRIMARY KEY,
    SalesPersonID     INT REFERENCES employees(EmployeeID),
    CustomerID        INT REFERENCES customers(CustomerID),
    ProductID         INT REFERENCES products(ProductID),
    Quantity          INT,
    Discount          NUMERIC(5,2),
    TotalPrice        NUMERIC(10,2),
    SalesDate         TEXT,         -- Ajustado desde DATE
    TransactionNumber VARCHAR(50)
);

-- ====================================
-- 2. CARGA DE CSVs DESDE /data
-- ====================================

COPY countries(CountryID, CountryName, CountryCode)
FROM '/data/countries.csv'
DELIMITER ',' CSV HEADER;

COPY cities(CityID, CityName, Zipcode, CountryID)
FROM '/data/cities.csv'
DELIMITER ',' CSV HEADER;

COPY categories(CategoryID, CategoryName)
FROM '/data/categories.csv'
DELIMITER ',' CSV HEADER;

COPY products(ProductID, ProductName, Price, CategoryID, Class, ModifyDate, Resistant, IsAllergic, VitalityDays)
FROM '/data/products.csv'
DELIMITER ',' CSV HEADER;

COPY customers(CustomerID, FirstName, MiddleInitial, LastName, CityID, Address)
FROM '/data/customers.csv'
DELIMITER ',' CSV HEADER;

COPY employees(EmployeeID, FirstName, MiddleInitial, LastName, BirthDate, Gender, CityID, HireDate)
FROM '/data/employees.csv'
DELIMITER ',' CSV HEADER;

COPY sales(SalesID, SalesPersonID, CustomerID, ProductID, Quantity, Discount, TotalPrice, SalesDate, TransactionNumber)
FROM '/data/sales.csv'
DELIMITER ',' CSV HEADER;

-- ====================================
-- 3. VALIDACIÓN: CANTIDAD DE REGISTROS
-- ====================================

SELECT 'countries' AS tabla, COUNT(*) FROM countries
UNION ALL
SELECT 'cities', COUNT(*) FROM cities
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'employees', COUNT(*) FROM employees
UNION ALL
SELECT 'sales', COUNT(*) FROM sales;
