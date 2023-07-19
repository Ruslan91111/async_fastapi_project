"""Configuration of interaction with database."""
from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from myapplication.settings import POSTGRES_URL


# create async engine
engine = create_async_engine(POSTGRES_URL, echo=True)

# create session for the interation with database
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Get async session."""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
