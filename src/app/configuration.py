import configparser
import os

import openai
from keycloak import KeycloakOpenID
from peewee import SqliteDatabase

from app.utils.services.connection_manager import ConnectionManager
from app.utils.services.keycloak_admin import CustomKeycloakAdmin
from app.utils.logger_api import LoggerApi

__version__ = '0.1.0'

LOGGER = LoggerApi("geodata")

conf_file = os.getenv('CONF_FILE', './conf/config.cfg')

config = configparser.ConfigParser()
config.read(conf_file)

API_IP = config.get('conf', "api_ip", fallback='0.0.0.0')
API_PORT = config.getint('conf', "api_port", fallback=5005)
API_GEO_URL = config.get('conf', "api_geo_url", fallback=None)
DATABASE_NAME = config.get('conf', "DATABASE_NAME", fallback="my_database.db")
API_KEY = os.getenv('API_KEY', 'token')
SAVE_FOLDER = config.get('conf', 'SAVE_FOLDER', fallback='./save')
MINUTES_REFRESH_CONF = config.getint('conf', "minutes_refresh_conf", fallback=5)
cors_ = config.get('conf', "cors_origins", fallback='').split(',')
CORS_ORIGINS = [c_ for c_ in cors_ if c_ != '']

KEYCLOAK_URL = config.get('keycloak', 'keycloak_url', fallback=None)
KEYCLOAK_SEC_URL = config.get('keycloak', 'keycloak_sec_url', fallback=None)
CLIENT_NAME = config.get('keycloak', 'client_name', fallback=None)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', None)
REALM = config.get('keycloak', 'realm', fallback=None)

KEYCLOAK_OPENID = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=CLIENT_NAME,
    realm_name=REALM,
)

KEYCLOAK_ADMIN = CustomKeycloakAdmin(
    server_url=KEYCLOAK_SEC_URL,
    username=os.getenv('USER_ADMIN', None),
    password=os.getenv('PSSWRD_ADMIN', None),
    realm_name=REALM,
    client_secret_key=CLIENT_SECRET,
    verify=False
)

DATABASE = SqliteDatabase(DATABASE_NAME)

MANAGER = ConnectionManager()

openai.api_key = os.getenv("GPT_KEY", None)

