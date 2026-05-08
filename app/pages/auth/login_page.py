from dash import dcc, Input, Output, State, callback
from .layouts.login_layout import Layout

def login_layout():
    return Layout()()



@callback(
    Output("output-msg", "children"),
    Input("submit-btn", "n_clicks"),
    State("email_log", "value"),
    State("phone_log", "value"),
    State("password_log", "value"),
    prevent_initial_call=True
)
def login_user(n_clicks, firstname, lastname, patronymic, email, phone, age, password):
    # Базовая валидация
    # if not all([firstname, lastname, email, phone, age, password]):
    #     return "⚠️ Заполните все обязательные поля."
    # if len(password) < 6:
    #     return "⚠️ Пароль должен содержать минимум 6 символов."
    #
    # if age < 1 or age > 120:
    #     return "⚠️ Укажите корректный возраст (1-120)."
    #
    #     # Сохранение в БД (пример с SQLAlchemy)
    # from app.db import get_db
    # from app.models.users import Users
    # from werkzeug.security import generate_password_hash
    #
    # db = get_db()
    #
    # # Проверка на существующего пользователя
    # if db.query(Users).filter(Users.email == email).first():
    #     db.close()
    #     return "⚠️ Пользователь с таким email уже существует."
    #
    # # Хеширование пароля и создание пользователя
    # new_user = Users(
    #     user_password=generate_password_hash(password),
    #     email=email,
    #     phone=phone,
    #     age=int(age),
    #     firstname=firstname,
    #     lastname=lastname,
    #     patronymic=patronymic or ""
    # )
    # db.add(new_user)
    # db.commit()
    # user_id = new_user.user_id
    # db.close()

    return dcc.Location(id="redirect", href=f"/auth/set-token?user_id={user_id}&email={email}", refresh=True)