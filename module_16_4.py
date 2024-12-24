# Тема "Модели данных Pydantic"
# Задача "Модель пользователя"


from fastapi import FastAPI,  Path, HTTPException
from pydantic import BaseModel
from typing import Annotated, List

# uvicorn module_16_4:app --reload - команда запуска FastAPI через терминал
app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None

# 1. get запрос по маршруту '/users' теперь возвращает список users
@app.get('/users')
async def get_all_users() -> List[User]:
    return users

# 2. id нового user будет на 1 больше, чем у последнего в списке users.
@app.post('/user/{username}/{age}')
async def add_user(
    username: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    user_id = max((t.id for t in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# 3.put запрос по маршруту '/user/{user_id}/{username}/{age} Обновляет username и age пользователя '
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100, description='Enter user ID', example=1)],
    username: Annotated[str, Path(min_length=5, max_length=20,
                                  description='Enter user name', example='UrbanUser')],
    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# 4. delete запрос по маршруту '/user/{user_id}' Удаляет пользователя
@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter user ID', example=1)]):
    for i, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")
