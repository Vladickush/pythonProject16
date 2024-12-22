# Тема "CRUD Запросы: Get, Post, Put Delete."
# Задача "Имитация работы с БД"

from fastapi import FastAPI, Path
from typing import Annotated

# uvicorn module_16_3:app --reload - команда запуска FastAPI через терминал
app = FastAPI()

# Словарь users
users = {'1': 'Имя: Example, возраст: 18'}


# 1. get запрос по маршруту '/users', который возвращает словарь users.
@app.get("/users")
async def get_all_users() -> dict:
    return users


# 2. post запрос по маршруту '/user/{username}/{age}',
@app.post("/user/{username}/{age}")
async def add_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Urban User")],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='22')]) -> str:
    new_id = str(int(max(users, key=int)) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_id} is registered"


# 3. put запрос по маршруту '/user/{user_id}/{username}/{age}'
@app.put("/user/{user_id}/{username}/{age}")
async def update_message(
        user_id: Annotated[str, Path(description='Enter user ID', example='1')],
        username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Urban User")],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='22')]) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f"The user {user_id} is updated"


# 4. delete запрос по маршруту '/user/{user_id}',
# который удаляет из словаря users пару по ключу user_id.
@app.delete('/user/{user_id}')
async def delete_user_id(user_id: Annotated[str, Path(description='Enter user ID', example='1')]) -> str:
    del users[user_id]
    return f'User {user_id} has been deleted'
