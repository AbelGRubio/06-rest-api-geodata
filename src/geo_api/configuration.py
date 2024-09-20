import os

from dotenv import load_dotenv
from peewee import SqliteDatabase

from .logger_api import LoggerApi

__version__ = '0.0.10'

load_dotenv()

LOGGER = LoggerApi()

API_IP = os.getenv("API_IP", '0.0.0.0')
API_PORT = int(os.getenv("API_PORT", 5005))
API_GEO_URL = os.getenv("API_GEO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "my_database.db")
API_KEY = 'token'

DATABASE = SqliteDatabase(DATABASE_NAME)
