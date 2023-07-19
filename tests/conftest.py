"""Test configuration"""
import asyncio
import os
from typing import Generator, Any

import asyncpg
import pytest
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import text

from myapplication.database.database import get_db
from myapplication.settings import TEST_POSTGRES_URL, TEST_POSTGRES_URL_FOR_POOL
from myapplication.main import app


test_engine = create_async_engine(TEST_POSTGRES_URL, future=True, echo=True)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)


TABLES_FOR_CLEANING = [
    "users",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_test_migrations():
    """Run alembic migrations to test database."""
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_test_session():
    """ Create session for the interation with test database. """
    engine = create_async_engine(TEST_POSTGRES_URL, future=True, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_test_tables(async_test_session):
    """Clean tables before test function."""
    async with async_test_session() as session:
        async with session.begin():
            for table in TABLES_FOR_CLEANING:
                await session.execute(text(f"TRUNCATE TABLE {table};"))


async def _get_test_db():
    try:
        # create async engine for interaction with database
        engine = create_async_engine(
            TEST_POSTGRES_URL, future=True, echo=True
        )

        # create session for the interaction with database
        async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """ Create a TestClient."""

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    """Async pool"""
    pool = await asyncpg.create_pool(TEST_POSTGRES_URL_FOR_POOL)
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):
    """Get the user from database by id."""

    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            return await connection.fetch("SELECT * FROM users WHERE user_id = $1;", user_id)

    return get_user_from_database_by_uuid
