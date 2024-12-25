# Тема "Шаблонизатор Jinja 2"
# Задача "Список пользователей в шаблоне"

from fastapi import FastAPI, Path, status, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

# uvicorn module_16_5:app --reload - команда запуска FastAPI через терминал
app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


# 1. get запрос по маршруту '/' принимает аргумент request и возвращает TemplateResponse:
@app.get('/', response_class=HTMLResponse)
async def get_main_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, "users": users})


# 2. get запрос по маршруту '/user/{user_id}' теперь возвращается объект TemplateResponse:
@app.get('/user/{user_id}')
async def get_user(request: Request,
                   user_id: Annotated[int, Path(description='Enter user ID', example=1)]):
    if user_id < 0 or user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": users[user_id]})


# 3. id нового user будет на 1 больше, чем у последнего в списке users.
@app.post('/user/{username}/{age}')
async def add_user(
        request: Request,
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example=24)]) -> HTMLResponse:
    user_id = len(users) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "user": users})


# 4.put запрос по маршруту '/user/{user_id}/{username}/{age} Обновляет username и age пользователя '
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


# 5. delete запрос по маршруту '/user/{user_id}' Удаляет пользователя
@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter user ID', example=1)]):
    for i, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User was not found")
