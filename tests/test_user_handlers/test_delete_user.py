"""Test handler fo delete user."""
import json
import uuid
from .details_of_errors import detail_incorrect_user_id


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    """Test 'delete user' handler."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert response.status_code == 200
    assert response.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_by_wrong_user_id(client):
    """Try to delete user by nonexistent user_id."""
    user_id = uuid.uuid4()
    response = client.delete(f"/user/?user_id={user_id}")
    assert response.status_code == 404
    assert response.json() == {'detail': f'User with id {user_id} not found.'}


async def test_delete_user_validation_error(client):
    """Try to delete user by incorrect user_id."""
    response = client.delete(f"/user/?user_id=not_valid_user_id")
    assert response.status_code == 422
    data_from_response = response.json()
    assert data_from_response == detail_incorrect_user_id


