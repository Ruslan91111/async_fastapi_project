"""Configuration of interaction with database."""
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from myapplication.settings import POSTGRES_URL


# create async engine
engine = create_async_engine(POSTGRES_URL, echo=True)

# create session for the interation with database
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session_db() -> Generator:
    """Get async session_db."""
    try:
        session_db: AsyncSession = async_session()
        yield session_db
    finally:
        await session_db.close()
