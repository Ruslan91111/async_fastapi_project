"""Routes for interaction with user model"""
from typing import Optional
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from myapplication.database.database import get_db
from .models_api import CreateUserRequest, ShowUser, DeleteUserResponse, \
    UpdateUserResponse, UpdateUserRequest
from ..database.data_access_layer import UserDataAccessLayer


user_router = APIRouter()


async def _create_new_user(body: CreateUserRequest, db) -> ShowUser:
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


async def _get_user(user_id, db) -> Optional[ShowUser]:
    """Get user from DB by user_id. Should use in handler get."""
    async with db as session:
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            user_from_database = await user_dal.get_user(user_id=user_id)
            if user_from_database is not None:
                return ShowUser(
                    user_id=user_from_database.user_id,
                    name=user_from_database.name,
                    surname=user_from_database.surname,
                    email=user_from_database.email,
                    is_active=user_from_database.is_active,
                )


async def _update_user(parameters_for_update_user: dict, user_id: UUID, db) -> Optional[UUID]:
    """Update user."""
    async with db as session:
        async with session.begin():
            user_dal = UserDataAccessLayer(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id,

                **parameters_for_update_user,
            )
            return updated_user_id


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUserRequest, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Create user"""
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    """Delete user handler."""
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    """Get user handler."""
    user_from_database = await _get_user(user_id, db)
    if user_from_database is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    return user_from_database


@user_router.patch("/", response_model=UpdateUserResponse)
async def update_user(
        user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
) -> UpdateUserResponse:
    """Update user handler."""
    parameters_for_update_user = body.model_dump(exclude_none=True)
    if parameters_for_update_user == {}:
        raise HTTPException(
            status_code=422, detail="You didn't specify any parameters.")
    user_from_db_for_update = await _get_user(user_id, db)
    if user_from_db_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found.")
    updated_user_id = await _update_user(parameters_for_update_user=parameters_for_update_user,
                                         db=db, user_id=user_id)
    return UpdateUserResponse(updated_user_id=updated_user_id)
