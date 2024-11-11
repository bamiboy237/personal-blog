import os
import secrets 
basedir = os.path.abspath(os.path.dirname(__file__))
from datetime import timedelta

class Config:
   SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
   REMEMBER_COOKIE_DURATION = timedelta(hours=1)

