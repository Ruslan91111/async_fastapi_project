"""Test handler fo delete user."""
import json
import uuid
from .details_of_errors import detail_incorrect_user_id
from ..conftest import create_test_auth_headers_for_user


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    """Test 'delete user' handler with everything fine."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response = client.delete(f"/user/?user_id={user_data['user_id']}",
                             headers=create_test_auth_headers_for_user(user_data["email"]))
    assert response.status_code == 200
    assert response.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_by_wrong_user_id(client, create_user_in_database):
    """Try to delete user by nonexistent user_id."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    user_id = uuid.uuid4()
    response = client.delete(f"/user/?user_id={user_id}",
                             headers=create_test_auth_headers_for_user(user_data["email"]))
    assert response.status_code == 404
    assert response.json() == {'detail': f'User with id {user_id} not found.'}


async def test_delete_user_validation_error(client, create_user_in_database):
    """Try to delete user by incorrect user_id (validation error."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response = client.delete(f"/user/?user_id=not_valid_user_id",
                             headers=create_test_auth_headers_for_user(user_data["email"]))
    assert response.status_code == 422
    data_from_response = response.json()
    assert data_from_response == detail_incorrect_user_id


async def test_delete_user_with_invalid_token_by_wrong_email(
        client, create_user_in_database):
    """Try to delete user using a invalid access token.
    Create jwt using not the same email. """
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response = client.delete(f"/user/?user_id=not_valid_user_id",
                             headers=create_test_auth_headers_for_user(
                                 user_data["email"] + "some_string"
                             ))
    assert response.status_code == 401
    data_from_response = response.json()
    assert data_from_response == {"detail": "Could not validate your credentials"}


async def test_delete_user_with_invalid_broken_token(
        client, create_user_in_database):
    """Try to delete user using a invalid access token -
    token with some extra symbols."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    auth_headers_broken_token = create_test_auth_headers_for_user(user_data["email"])
    auth_headers_broken_token["Authorization"] += "Something that should not be in token"
    response = client.delete(f"/user/?user_id=not_valid_user_id",
                             headers=auth_headers_broken_token)
    assert response.status_code == 401
    data_from_response = response.json()
    assert data_from_response == {"detail": "Could not validate your credentials"}


async def test_delete_user_no_jwt(client, create_user_in_database):
    """Try to delete user using no access token."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response = client.delete(f"/user/?user_id=not_valid_user_id")
    assert response.status_code == 401
    data_from_response = response.json()
    assert data_from_response == {"detail": "Not authenticated"}
