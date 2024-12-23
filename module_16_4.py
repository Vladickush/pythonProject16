# Тема "Модели данных Pydantic"
# Задача "Модель пользователя"


from fastapi import FastAPI,  HTTPException
from pydantic import BaseModel
from typing import List

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
async def add_user(user: User, username: str, age: int):
    user_id = max((t.id for t in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

# 3.put запрос по маршруту '/user/{user_id}/{username}/{age} Обновляет username и age пользователя '
@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: int, username: str, age: int):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# 4. delete запрос по маршруту '/user/{user_id}' Удаляет пользователя
@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")