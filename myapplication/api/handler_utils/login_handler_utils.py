from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from myapplication.database.data_access_layer import UserDataAccessLayer
from myapplication.database.database import get_session_db
from myapplication.database.models_db import User
from myapplication.hasher import Hasher
from myapplication.settings import SECRET_KEY, ALGORITHM


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_by_email_for_authentication(email: str, session_db):
    """Get user from DB by email for authentication."""
    async with session_db.begin():
        user_dal = UserDataAccessLayer(session_db)

        return await user_dal.get_user_from_db_by_email(email=email,)


async def authenticate_user_by_email_and_password(email: str,
                                                  password_from_user: str,
                                                  session_db: AsyncSession) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = await _get_user_by_email_for_authentication(email=email, session_db=session_db)
    if user is None:
        return None
    if not Hasher.verify_password(password_from_user, user.password):
        return None

    return user


async def get_current_user_from_token(token: str = Depends(oauth2_schema),
                                      session_db: AsyncSession = Depends(get_session_db)):
    """Get current user from access token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate your credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("sub")
        print("username/email extracted is ", email)
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email_for_authentication(email=email, session_db=session_db)
    if user is None:
        raise credentials_exception
    return user
