"""File with settings and configs of project."""
import os
from dotenv import load_dotenv

env = load_dotenv()  # take environment variables from .env.

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = fastapi = os.getenv("POSTGRES_DB")
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@0.0.0.0:5433/{POSTGRES_DB}"
