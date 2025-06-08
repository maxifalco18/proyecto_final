import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, engine

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class DatabaseConnection:
    """
    Clase Singleton para gestionar la conexión a la base de datos.
    
    Asegura que solo exista una instancia del motor de SQLAlchemy en toda la aplicación,
    optimizando el uso de recursos y la gestión de la conexión.
    """
    _instance = None
    _engine = None

    def __new__(cls):
        """
        Sobrescribe el método __new__ para implementar el patrón Singleton.
        """
        if cls._instance is None:
            print("Creando una nueva instancia de DatabaseConnection...")
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            
            # Obtener credenciales de la base de datos desde .env
            db_user = os.getenv("POSTGRES_USER")
            db_password = os.getenv("POSTGRES_PASSWORD")
            db_host = os.getenv("POSTGRES_HOST", "localhost") # Default a localhost si no está
            db_port = os.getenv("POSTGRES_PORT", "5432")
            db_name = os.getenv("POSTGRES_DB")

            if not all([db_user, db_password, db_host, db_port, db_name]):
                raise ValueError("Faltan variables de entorno para la conexión a la base de datos.")

            # Crear el motor de SQLAlchemy
            db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            cls._engine = create_engine(db_url)
        
        return cls._instance

    def get_engine(self) -> engine.Engine:
        """
        Devuelve el motor de SQLAlchemy para ser utilizado por otras partes de la aplicación.
        """
        return self._engine