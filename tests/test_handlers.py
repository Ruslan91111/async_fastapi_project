import json
import uuid


async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com"
    }
    response = client.post("/user/", content=json.dumps(user_data))
    data_from_response = response.json()
    assert response.status_code == 200
    assert data_from_response["name"] == user_data["name"]
    assert data_from_response["surname"] == user_data["surname"]
    assert data_from_response["email"] == user_data["email"]
    users_from_db = await get_user_from_database(data_from_response["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_response["user_id"]


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid.uuid4(),
        "name": "John",
        "surname": "Smith",
        "email": "Smith@mail.com",
        "is_active": True
    }
    await create_user_in_database(**user_data)
    response = client.delete(f"/user/?user_id={user_data['user_id']}")
    assert response.status_code == 200
    assert response.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    print('reSSPOnse', users_from_db)
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]
