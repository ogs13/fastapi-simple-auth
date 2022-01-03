import os

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = Config(f'{BASE_DIR}/.env')

DATABASE_URL = f'sqlite:///{BASE_DIR}/'+config('DB_NAME',cast=str)

SECRET_KEY = config('SECRET_KEY',cast=Secret)