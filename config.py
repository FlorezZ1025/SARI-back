from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=60*60*24)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')
    JWT_TOKEN_LOCATION = 'headers'
    # JWT_TOKEN_LOCATION = 'cookies'
    # JWT_COOKIE_HTTPOONLY = True
