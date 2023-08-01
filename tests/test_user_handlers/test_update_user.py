"""Test handlers for update user."""
import json
import uuid
import pytest
from .details_of_errors import (detail_for_empty_fields, detail_for_wrong_email,
                                detail_for_wrong_email_from_update, detail_string_too_short,
                                detail_update_invalid_user_id, detail_for_empty_fields_update)


async def test_update_user(client, create_user_in_database, get_user_from_database):
    """Test 'update user' handler."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_for_update = {
        "name": "Ivan",
        "surname": "Drago",
        "email": "Smith@mail.com",
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response_after_update = client.patch(f"/user/?user_id={user_data['user_id']}",
                                         content=json.dumps(user_data_for_update))
    assert response_after_update.status_code == 200
    response_data = response_after_update.json()
    assert response_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_for_update["name"]
    assert user_from_db["surname"] == user_data_for_update["surname"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_update_user_one_is_updated_other_not(client, create_user_in_database,
                                                    get_user_from_database):
    """Testing 'update user' handler. Check that when we update a user
    other stands not updated."""
    user_data_1 = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_2 = {
        "user_id": uuid.uuid4(),
        "name": "Richard",
        "surname": "Henderson",
        "email": "Henderson@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_3 = {
        "user_id": uuid.uuid4(),
        "name": "Adam",
        "surname": "Pack",
        "email": "Packman@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_for_update = {
        "name": "newname",
        "surname": "newsurname",
        "email": "newemail@mail.com",
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    response_after_update = client.patch(f"/user/?user_id={user_data_1['user_id']}",
                                         content=json.dumps(user_data_for_update))
    assert response_after_update.status_code == 200
    response_data = response_after_update.json()
    assert response_data["updated_user_id"] == str(user_data_1["user_id"])

    # Check that user_data_1 were changed on user_data_for_update.
    user_from_db = await get_user_from_database(user_data_1["user_id"])
    user_from_db = dict(user_from_db[0])
    assert user_from_db["name"] == user_data_for_update["name"]
    assert user_from_db["surname"] == user_data_for_update["surname"]
    assert user_from_db["email"] == user_data_for_update["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data_1["user_id"]

    # Check that user_data_2 not changed.
    user_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(user_from_db[0])
    assert user_from_db["name"] == user_data_2["name"]
    assert user_from_db["surname"] == user_data_2["surname"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]

    # Check that user_data_3 not changed.
    user_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(user_from_db[0])
    assert user_from_db["name"] == user_data_3["name"]
    assert user_from_db["surname"] == user_data_3["surname"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]


@pytest.mark.parametrize("user_data_for_update, expected_status_code, expected_detail",
                         [
                             ({}, 422, detail_for_empty_fields_update),
                             (
                                     {"name": "John1"},
                                     422,
                                     {"detail": "Name should contains only letters"}
                             ),
                             (
                                     {"surname": "McClane2"},
                                     422,
                                     {"detail": "Surname should contains only letters"}
                             ),
                             (
                                 {"email": "John"},
                                 422,
                                 detail_for_wrong_email_from_update
                              ),
                             (
                                     {"email": ""}, 422,
                                     {'detail': [{'type': 'missing', 'loc': ['body', 'name'], 'msg': 'Field required', 'input': {'email': ''}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'}, {'type': 'missing', 'loc': ['body', 'surname'], 'msg': 'Field required', 'input': {'email': ''}, 'url': 'https://errors.pydantic.dev/2.1.2/v/missing'}, {'type': 'value_error', 'loc': ['body', 'email'], 'msg': 'value is not a valid email address: The email address is not valid. It must have exactly one @-sign.', 'input': '', 'ctx': {'reason': 'The email address is not valid. It must have exactly one @-sign.'}}]}

                             )
                         ])
async def test_update_user_validation_error(client, create_user_in_database,
                                            user_data_for_update, expected_status_code, expected_detail):
    """Test 'create user' handler. TestCase when user inputs wrong data."""
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True,
        "password": "password"
    }
    await create_user_in_database(**user_data)
    response = client.patch(f"/user/?user_id={user_data['user_id']}",
                            content=json.dumps(user_data_for_update))
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    print(data_from_response)
    print('##################################################')
    print(expected_detail)
    assert data_from_response == expected_detail


async def test_update_user_invalid_user_id(client, create_user_in_database, get_user_from_database):
    """Test 'update user' handler, try to update with invalid user_id."""
    user_data_for_update = {
        "name": "Ivan",
        "surname": "Drago",
        "email": "Ivan@mail.com",
        "password": "password"
    }
    response_after_update = client.patch(f"/user/?user_id=123",
                                         content=json.dumps(user_data_for_update))
    assert response_after_update.status_code == 422
    response_data = response_after_update.json()
    assert response_data == detail_update_invalid_user_id


async def test_update_user_duplicate_email(client, create_user_in_database, get_user_from_database):
    """Test 'update user' handler, try to update with email,
    that already used in database."""
    user_data_1 = {
        "user_id": uuid.uuid4(),
        "name": "Ivan",
        "surname": "Drago",
        "email": "Ivan@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_2 = {
        "user_id": uuid.uuid4(),
        "name": "Boris",
        "surname": "Blade",
        "email": "BorisB@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_3 = {
        "user_id": uuid.uuid4(),
        "name": "Vladimir",
        "surname": "Tran",
        "email": "TranB@mail.com",
        "is_active": True,
        "password": "password"
    }
    user_data_for_update = {
        "email": user_data_2["email"],
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    response_after_update = client.patch(f"/user/?user_id={user_data_1['user_id']}",
                                         content=json.dumps(user_data_for_update))
    assert response_after_update.status_code == 422
    response_data = response_after_update.json()
