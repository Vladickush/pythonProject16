# Тема "Основы Fast Api и маршрутизация"
# Задача "Начало пути"

from fastapi import FastAPI

app = FastAPI()
# uvicorn main:app --reload - запуск FastAPI

# "/" - главная страница
@app.get("/")
async def main() -> str:
    return "Главная страница"


# "/user/admin" - страница администратора
@app.get("/user/admin")
async def admin() -> str:
    return "Вы вошли как администратор"


# "/user/{user_id}" - страница пользователя с номером "/user/{123}".
@app.get("/user/{user_id}")
async def user(user_id) -> str:
    return f"Вы вошли как пользователь № {user_id}"


# "/user?username='Name'&age=int" - страница с параметрами (username,age)
@app.get("/user")
async def user_data(username: str, age: int) -> str:
    return f"Информация о пользователе. Имя: {username}, Возраст: {age}"
