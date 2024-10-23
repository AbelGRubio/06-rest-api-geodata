import os

import openai
from dotenv import load_dotenv
from keycloak import KeycloakOpenID
from peewee import SqliteDatabase

from .connection_manager import ConnectionManager
from .keycloak_admin import CustomKeycloakAdmin
from .logger_api import LoggerApi

__version__ = '0.1.0'

load_dotenv()

LOGGER = LoggerApi("geodata")

API_IP = os.getenv("API_IP", '0.0.0.0')
API_PORT = int(os.getenv("API_PORT", 5005))
API_GEO_URL = os.getenv("API_GEO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "my_database.db")
API_KEY = 'token'
SAVE_FOLDER = os.getenv('SAVE_FOLDER', './save')

KEYCLOAK_URL = 'http://10.0.0.12:8888/'
KEYCLOAK_SEC_URL = 'https://10.0.0.12:8843/'
CLIENT_NAME = 'angular-app'
CLIENT_SECRET = '38504b38-8426-44af-bd5b-84807e02ed33'
REALM = 'chat'

KEYCLOAK_OPENID = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=CLIENT_NAME,
    realm_name=REALM,
    # client_secret_key=CLIENT_SECRET
)

KEYCLOAK_ADMIN = CustomKeycloakAdmin(
    server_url=KEYCLOAK_SEC_URL,
    username='admin',
    password='admin',
    realm_name=REALM,
    client_id=CLIENT_NAME,
    client_secret_key=CLIENT_SECRET,
    verify=False
)

DATABASE = SqliteDatabase(DATABASE_NAME)

MANAGER = ConnectionManager()

openai.api_key = os.getenv("GPT_KEY", None)

