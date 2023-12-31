"""Handlers for interact with user's routes."""
from uuid import UUID

from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from logging import getLogger

from myapplication.api.handler_utils.login_handler_utils import get_current_user_from_token
from myapplication.api.handler_utils.user_handler_utils import _create_new_user, \
    _delete_user, _get_user_by_id, _update_user
from myapplication.database.database import get_session_db
from myapplication.api.models_api import CreateUserRequest, ShowUser, DeleteUserResponse, \
    UpdateUserResponse, UpdateUserRequest
from myapplication.database.models_db import User

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUserRequest,
                      session_db: AsyncSession = Depends(get_session_db)) -> ShowUser:
    """Create user"""
    try:
        return await _create_new_user(body, session_db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=409,
                            detail="The email address you entered is already registered.")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID,
                      session_db: AsyncSession = Depends(get_session_db),
                      current_user: User = Depends(get_current_user_from_token)
                      ) -> DeleteUserResponse:
    """Delete user handler."""
    deleted_user_id = await _delete_user(user_id, session_db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user(user_id: UUID,
                   session_db: AsyncSession = Depends(get_session_db),
                   current_user: User = Depends(get_current_user_from_token)
                   ) -> ShowUser:
    """Get user handler."""
    user_from_database = await _get_user_by_id(user_id, session_db)
    if user_from_database is None:
        raise HTTPException(status_code=404,
                            detail=f"User with id {user_id} not found.")
    return user_from_database


@user_router.patch("/", response_model=UpdateUserResponse)
async def update_user(user_id: UUID,
                      body: UpdateUserRequest,
                      session_db: AsyncSession = Depends(get_session_db),
                      current_user: User = Depends(get_current_user_from_token)
                      ) -> UpdateUserResponse:
    """Update user handler."""
    parameters_for_update_user = body.model_dump(exclude_none=True)
    if parameters_for_update_user == {}:
        raise HTTPException(
            status_code=422, detail="You didn't specify any parameters.")
    user_from_db_for_update = await _get_user_by_id(user_id, session_db)
    if user_from_db_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found.")

    try:
        updated_user_id = await _update_user(parameters_for_update_user=parameters_for_update_user,
                                             session_db=session_db, user_id=user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=409,
                            detail="The email address you entered is already registered.")
    return UpdateUserResponse(updated_user_id=updated_user_id)
