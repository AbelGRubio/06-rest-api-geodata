import os

import openai
from dotenv import load_dotenv
from peewee import SqliteDatabase

from .connection_manager import ConnectionManager
from .logger_api import LoggerApi

__version__ = '0.1.0'

load_dotenv()

LOGGER = LoggerApi()

API_IP = os.getenv("API_IP", '0.0.0.0')
API_PORT = int(os.getenv("API_PORT", 5005))
API_GEO_URL = os.getenv("API_GEO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "my_database.db")
API_KEY = 'token'
SAVE_FOLDER = os.getenv('SAVE_FOLDER', './save')


DATABASE = SqliteDatabase(DATABASE_NAME)

MANAGER = ConnectionManager()

openai.api_key = os.getenv("GPT_KEY", None)

