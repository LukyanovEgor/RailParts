from dash import html, dcc, Input, Output, State, callback
from app.db import get_db
from app.models.users import Users
from werkzeug.security import generate_password_hash


def register_layout():
    form_style = {
        'maxWidth': '400px',
        'margin': '20px auto',
        'padding': '20px',
        'border': '1px solid #ddd',
        'borderRadius': '8px',
        'fontFamily': 'Arial, sans-serif'
    }
    input_style = {'padding': '8px', 'margin': '5px 0 10px', 'width': '100%', 'boxSizing': 'border-box'}
    label_style = {'fontWeight': 'bold', 'marginTop': '10px', 'display': 'block'}

    return html.Div([
    html.H2("Регистрация", style={'textAlign': 'center'}),

    html.Label("Имя *", style=label_style),
    dcc.Input(id="firstname", type="text", placeholder="Иван", style=input_style),

    html.Label("Фамилия *", style=label_style),
    dcc.Input(id="lastname", type="text", placeholder="Иванов", style=input_style),

    html.Label("Отчество", style=label_style),
    dcc.Input(id="patronymic", type="text", placeholder="Иванович", style=input_style),

    html.Label("Email *", style=label_style),
    dcc.Input(id="email", type="email", placeholder="user@example.com", style=input_style),

    html.Label("Телефон *", style=label_style),
    dcc.Input(id="phone", type="tel", placeholder="+7 (999) 999-99-99", style=input_style),

    html.Label("Возраст *", style=label_style),
    dcc.Input(id="age", type="number", placeholder="25", min=1, max=120, style=input_style),

    html.Label("Пароль *", style=label_style),
    dcc.Input(id="password", type="password", placeholder="Минимум 6 символов", style=input_style),

    html.Button("Зарегистрироваться", id="submit-btn", className='btn_style', n_clicks=0),
    html.Div(id="output-message", style={'marginTop': '15px', 'textAlign': 'center', 'fontWeight': 'bold'}),
        dcc.Location(id="redirect", refresh=False)  # <-- для редиректов
], style=form_style)


@callback(
    Output("output-message", "children"),
    Input("submit-btn", "n_clicks"),
    State("firstname", "value"),
    State("lastname", "value"),
    State("patronymic", "value"),
    State("email", "value"),
    State("phone", "value"),
    State("age", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def register_user(n_clicks, firstname, lastname, patronymic, email, phone, age, password):
    # Базовая валидация
    if not all([firstname, lastname, email, phone, age, password]):
        return "⚠️ Заполните все обязательные поля."
    if len(password) < 6:
        return "⚠️ Пароль должен содержать минимум 6 символов."

    if age < 1 or age > 120:
        return "⚠️ Укажите корректный возраст (1-120)."

    db = get_db()

    # Проверка на существующего пользователя
    if db.query(Users).filter(Users.email == email).first():
        db.close()
        return "⚠️ Пользователь с таким email уже существует."

    # Хеширование пароля и создание пользователя
    new_user = Users(
        user_password=generate_password_hash(password),
        email=email,
        phone=phone,
        age=int(age),
        firstname=firstname,
        lastname=lastname,
        patronymic=patronymic or ""
    )
    db.add(new_user)
    db.commit()
    user_id = new_user.user_id
    db.close()

    return dcc.Location(id="redirect", href=f"/auth/set-token?user_id={user_id}&email={email}", refresh=True)