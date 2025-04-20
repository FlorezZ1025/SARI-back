from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Configuración base del proyecto con parámetros comunes, como clave secreta, puerto, y base de datos.
    Sirve como clase base para configuraciones específicas de entornos como desarrollo, producción y pruebas.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Reducir uso de memoria de SQLAlchemy
    DEBUG = True  
    PORT = 5000  
    JWT_TOKEN_LOCATION = 'headers'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=60*60*24)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')


class ProductionConfig(Config):
    """Configuración específica para el entorno de producción.
    Desactiva el modo debug y asegura las cookies. Permite configurar una URI de base de datos específica para producción.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL'),

    DEBUG = False  
    # SQLBD = {
    #     'SQLALCHEMY_DATABASE_URI': os.getenv('DATABASE_URL'),
    #     'SQLALCHEMY_TRACK_MODIFICATIONS': False
    # }

class DevelopmentConfig(Config):
    """Configuración específica para el entorno de desarrollo.
    Habilita el modo debug para facilitar la depuración durante el desarrollo.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL'),
    DEBUG = True  # Activar modo debug en desarrollo


class PURE:
    PURE_URL = os.getenv('PURE_URL')