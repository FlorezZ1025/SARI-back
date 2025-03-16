from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=60*60*1)
    # JWT_TOKEN_LOCATION = 'cookies'
    # JWT_COOKIE_HTTPOONLY = True
