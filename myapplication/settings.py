"""File with settings and configs of project."""
import os
from dotenv import load_dotenv


env = load_dotenv()  # take environment variables from .env.

# For main DB postgresql
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = fastapi = os.getenv("POSTGRES_DB")

# For TEST DB postgresql
POSTGRES_USER_TEST = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD_TEST = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_TEST = os.getenv("POSTGRES_DB")

# URLS
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@0.0.0.0:5433/{POSTGRES_DB}"
TEST_POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}@0.0.0.0:5433/{POSTGRES_DB_TEST}"
TEST_POSTGRES_URL_FOR_POOL = f"postgresql://{POSTGRES_USER_TEST}:{POSTGRES_PASSWORD_TEST}@0.0.0.0:5433/{POSTGRES_DB_TEST}"

# For JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES"))
