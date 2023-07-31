"""Pydantic models"""
import re
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, constr
from fastapi import HTTPException


LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class BaseModelForAPI(BaseModel):
    """Everything convert to JSON"""
    class ConfigDict:
        from_attributes = True


class ShowUser(BaseModelForAPI):
    """Show user to client."""
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class CreateUserRequest(BaseModel):
    """Get data from client for creation user."""
    name: str
    surname: str
    email: EmailStr
    password: str

    @field_validator("name")
    def validate_name(cls, value):
        """Validate name before create user"""
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        """Validate surname before create user"""
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    """Response after delete user."""
    deleted_user_id: uuid.UUID


class UpdateUserResponse(BaseModel):
    """Response after update user by patch."""
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    """Get data from client to update user."""
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @field_validator("name")
    def validate_name(cls, value):
        """Validate name before create user"""
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @field_validator("surname")
    def validate_surname(cls, value):
        """Validate surname before create user"""
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class Token(BaseModel):
    """Token model."""
    access_token: str
    token_type: str
