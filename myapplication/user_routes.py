"""Routes for interaction with user model"""
from fastapi.routing import APIRouter
from .models_api import CreateUser, ShowUser
from .database import async_session
from .models_db import UserDataAccessLayer


user_router = APIRouter()


async def _create_new_user(body: CreateUser) -> ShowUser:
    async with async_session() as session:
        async with session.begin():
            user_data = UserDataAccessLayer(session)
            user = await user_data.create_user(
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


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUser) -> ShowUser:
    """Create user"""
    return await _create_new_user(body)
