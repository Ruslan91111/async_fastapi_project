from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from myapplication.database.data_access_layer import UserDataAccessLayer
from myapplication.database.models_db import User
from myapplication.hasher import Hasher


async def _get_user_by_email_for_authentication(email: str, session):
    """Get user from DB by email for authentication."""
    async with session.begin():
        user_dal = UserDataAccessLayer(session)

        return await user_dal.get_user_from_db_by_email(email=email,)


async def authenticate_user_by_email_and_password(email: str,
                                                  password_from_user: str,
                                                  session: AsyncSession) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = await _get_user_by_email_for_authentication(email=email, session=session)
    if user is None:
        return None
    if not Hasher.verify_password(password_from_user, user.password):
        return None

    return user
