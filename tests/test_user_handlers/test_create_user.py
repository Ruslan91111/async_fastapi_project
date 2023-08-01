"""Test handler of create user."""
import json
import uuid
import pytest

from .details_of_errors import detail_for_empty_fields, detail_for_wrong_email


async def test_create_user(client, get_user_from_database):
    """Test 'create user' handler."""
    user_data = {
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "password": "password"
    }
    response = client.post("/user/", content=json.dumps(user_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response["name"] == user_data["name"]
    assert data_from_response["surname"] == user_data["surname"]
    assert data_from_response["email"] == user_data["email"]
    assert data_from_response["is_active"] is True
    users_from_db = await get_user_from_database(data_from_response["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_response["user_id"]


async def test_create_user_try_input_same_email(client, get_user_from_database):
    """Test the "create user" handler when a user tries
    to use an email that is already in the database"""
    user_data = {
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "password": "password"
    }
    user_data_with_same_email = {
        "name": "Michael",
        "surname": "Thorn",
        "email": "Smith@mail.com",
        "password": "password"
    }
    response = client.post("/user/", content=json.dumps(user_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response["name"] == user_data["name"]
    assert data_from_response["surname"] == user_data["surname"]
    assert data_from_response["email"] == user_data["email"]
    assert data_from_response["is_active"] is True
    users_from_db = await get_user_from_database(data_from_response["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_response["user_id"]
    response = client.post("/user/", content=json.dumps(user_data_with_same_email))
    assert response.status_code == 409
    assert response.json()["detail"] == "The email address you entered is already registered."


@pytest.mark.parametrize("user_data, expected_status_code, expected_detail",
                         [
                             ({}, 422, detail_for_empty_fields),
                             (
                                     {"name": "John1", "surname": "McClane", "email": "John@mail.com",
                                      "password": "password"}, 422,
                                     {"detail": "Name should contains only letters"}
                             ),
                             (
                                     {"name": "John", "surname": "McClane2", "email": "John@mail.com",
                                      "password": "password"}, 422,
                                     {"detail": "Surname should contains only letters"}
                             ),
                             (
                                 {"name": "John", "surname": "McClane", "email": "John",
                                  "password": "password"}, 422, detail_for_wrong_email
                              ),
                             (
                                     {"name": "", "surname": "McClane", "email": "John@mail.com",
                                      "password": "password"}, 422,
                                     {"detail": "Name should contains only letters"}
                             ),
                         ])
async def test_create_user_validation_error(client, user_data, expected_status_code, expected_detail):
    """Test 'create user' handler. TestCase when user inputs wrong data."""
    response = client.post("/user/", content=json.dumps(user_data))
    data_from_response = response.json()
    print('#################################################')
    print(data_from_response)
    print('#################################################')
    print(expected_detail)
    print('#################################################')
    assert response.status_code == expected_status_code
    assert data_from_response == expected_detail


