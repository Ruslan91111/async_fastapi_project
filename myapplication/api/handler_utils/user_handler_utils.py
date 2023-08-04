"""Utils for act in handllers."""
from typing import Optional
from uuid import UUID

from myapplication.api.models_api import CreateUserRequest, ShowUser
from myapplication.database.data_access_layer import UserDataAccessLayer
from myapplication.hasher import Hasher


async def _create_new_user(body: CreateUserRequest, session_db) -> ShowUser:
    """Create user. Should use in handler post('/')"""
    async with session_db.begin():
        user_dal = UserDataAccessLayer(session_db)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            password=Hasher.get_hash_of_password(body.password)
        )
        return ShowUser(
          user_id=user.user_id,
          name=user.name,
          surname=user.surname,
          email=user.email,
          is_active=user.is_active,
        )


async def _delete_user(user_id, session_db) -> Optional[UUID]:
    """Delete user. Should use in handler delete."""
    async with session_db.begin():
        user_dal = UserDataAccessLayer(session_db)
        deleted_user_id = await user_dal.delete_user(user_id=user_id)
        return deleted_user_id


async def _get_user_by_id(user_id, session_db) -> Optional[ShowUser]:
    """Get user from DB by user_id. Should use in handler get."""
    async with session_db.begin():
        user_dal = UserDataAccessLayer(session_db)
        user_from_database = await user_dal.get_user_from_db_by_id(user_id=user_id)
        if user_from_database is not None:
            return ShowUser(
                user_id=user_from_database.user_id,
                name=user_from_database.name,
                surname=user_from_database.surname,
                email=user_from_database.email,
                is_active=user_from_database.is_active,
            )


async def _update_user(parameters_for_update_user: dict, user_id: UUID,
                       session_db) -> Optional[UUID]:
    """Update user."""
    async with session_db.begin():
        user_dal = UserDataAccessLayer(session_db)
        updated_user_id = await user_dal.update_user(
            user_id=user_id,
            **parameters_for_update_user,
        )
        return updated_user_id
