from datetime import timedelta, datetime
from typing import Optional
from jose import JWTError, jwt
from .settings import ACCESS_TOKEN_EXPIRES_MINUTES, SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create and return to user a access token."""
    data_for_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    data_for_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_for_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
