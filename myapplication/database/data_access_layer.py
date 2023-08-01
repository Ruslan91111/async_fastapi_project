"""Data access layer"""
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select

from .models_db import User


class UserDataAccessLayer:
    """Business logic for interaction with DB."""
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, surname: str, email: str, password: str) -> User:
        """Create user"""
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        """Delete user."""
        query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).returning(User.user_id)
        result = await self.db_session.execute(query)
        deleted_user_id_row = result.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_from_db_by_id(self, user_id: UUID) -> Optional[UUID]:
        """Get a user from database by id."""
        query = select(User).where(User.user_id == user_id)
        result = await self.db_session.execute(query)
        user_from_table = result.fetchone()
        if user_from_table is not None:
            return user_from_table[0]

    async def get_user_from_db_by_email(self, email: str) -> Optional[UUID]:
        """Get a user from database by email."""
        query = select(User).where(User.email == email)
        result = await self.db_session.execute(query)
        user_from_table = result.fetchone()
        if user_from_table is not None:
            return user_from_table[0]

    async def update_user(self, user_id: UUID, **parameters_for_update_user) -> Optional[UUID]:
        """Update a user."""
        query = update(User).where(and_(User.user_id == user_id, User.is_active == True)).\
            values(parameters_for_update_user).returning(User.user_id)
        result = await self.db_session.execute(query)
        updated_user = result.fetchone()
        if updated_user is not None:
            return updated_user[0]
