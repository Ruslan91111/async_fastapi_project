"""Test handlers of interaction with user."""
import json
import uuid
from .details_of_errors import detail_incorrect_user_id


async def test_get_user(client, create_user_in_database):
    """Test 'get user' handler."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    response = client.get(f"/user/?user_id={user_data['user_id']}")
    assert response.status_code == 200
    user_from_response = response.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] == user_data["is_active"]


async def test_get_user_by_wrong_user_id(client, create_user_in_database,
                                         get_user_from_database):
    """Try to delete user by nonexistent user_id."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    fake_user_id = uuid.uuid4()
    response = client.get(f"/user/?user_id={fake_user_id}")
    assert response.status_code == 404
    assert response.json() == {'detail': f'User with id {fake_user_id} not found.'}


async def test_get_user_validation_error(client, create_user_in_database,
                                         get_user_from_database):
    """Try to delete user by incorrect user_id."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    response = client.get(f"/user/?user_id=not_valid_user_id")
    assert response.status_code == 422
    data_from_response = response.json()
    assert data_from_response == detail_incorrect_user_id
