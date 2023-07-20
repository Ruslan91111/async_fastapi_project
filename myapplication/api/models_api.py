"""Pydantic models"""
import re
import uuid

from pydantic import BaseModel, EmailStr, field_validator
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


class CreateUser(BaseModel):
    """Get data from client."""
    name: str
    surname: str
    email: EmailStr

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
