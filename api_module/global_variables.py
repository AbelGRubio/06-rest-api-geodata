import os

from dotenv import load_dotenv
from fastapi import FastAPI

from .functions import check_all_vars, check_exist_database, LOGGER

load_dotenv()

APP = FastAPI()

vars_to_check = [
    "API_IP", "API_PORT", "API_GEO_URL",
    "DATABASE_NAME", "EXIST_USER_MSG",
    "ADDED_USER_MSG"
]

if not check_all_vars(vars_to_check):
    LOGGER.error("There are not all variables")
    exit(0)

API_IP = os.getenv("API_IP")
API_PORT = int(os.getenv("API_PORT"))
API_GEO_URL = os.getenv("API_GEO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
EXIST_USER_MSG = os.getenv("EXIST_USER_MSG")
ADDED_USER_MSG = os.getenv("ADDED_USER_MSG")

check_exist_database(database=DATABASE_NAME)

from .routes import *
