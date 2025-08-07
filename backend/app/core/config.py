import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings
# Carga las variables de entorno
load_dotenv()

# BaseSettings establece automáticamente los valores para las variables de entorno
# y permite acceder a ellas de forma segura.
class Settings(BaseSettings):
    # Extraemos cada parte de la URL de forma segura
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Construimos la URL completa para SQLAlchemy
    # @property permite acceder a DATABASE_URL como un atributo
    @property
    def DATABASE_URL(self) -> str:
        # Codificamos la contraseña para evitar errores con caracteres especiales
        encoded_password = quote_plus(self.DB_PASSWORD)
        return f"mysql+pymysql://{self.DB_USER}:{encoded_password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Crea una instancia de la clase Settings
settings = Settings()