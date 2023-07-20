"""Routes for interaction with user model"""
from typing import Optional
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .models_api import CreateUser, ShowUser, DeleteUserResponse
from myapplication.database.database import get_db
from ..database.data_access_layer import UserDataAccessLayer


user_router = APIRouter()


async def _create_new_user(body: CreateUser, db) -> ShowUser:
    """Create user. Should use in handler post('/')"""
    async with db as session:
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
            )
            return ShowUser(
              user_id=user.user_id,
              name=user.name,
              surname=user.surname,
              email=user.email,
              is_active=user.is_active,
            )


async def _delete_user(user_id, db) -> Optional[UUID]:
    """Delete user. Should use in handler delete."""
    async with db as session:
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            deleted_user_id = await user_dal.delete_user(user_id=user_id)
            return deleted_user_id


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Create user"""
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)