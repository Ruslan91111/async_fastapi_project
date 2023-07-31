"""Handlers for authentication of user."""
from datetime import timedelta
from fastapi.routing import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from myapplication.database.database import get_db
from myapplication.api.models_api import Token
from myapplication.api.handler_utils.login_handler_utils \
    import authenticate_user_by_email_and_password
from myapplication.settings import ACCESS_TOKEN_EXPIRES_MINUTES
from myapplication.token_maker import create_access_token

login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_user_to_get_access_token(form_data_to_login: OAuth2PasswordRequestForm = Depends(),
                                         db: AsyncSession = Depends(get_db)):
    """Handler for authentication."""
    user = await authenticate_user_by_email_and_password(form_data_to_login.username,
                                                         form_data_to_login.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You entered incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
