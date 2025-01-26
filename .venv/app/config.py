import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of config.py
    DATABASE_PATH = os.path.join(BASE_DIR, '..', 'database.db')  # Go one level up to the .venv folder
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
