from dash import dcc, Input, Output, State, callback, ctx
from .layouts.login_layout import Layout
from .components import PHONE_FORM, EMAIL_FORM
from app.db import get_db
from app.models.users import Users
from werkzeug.security import check_password_hash



def login_layout():
    return Layout()()


# переключатель
@callback(
    Output('form-store', 'data'),
    Output('email-type', 'data-state'),
    Output('phone-type', 'data-state'),
    Input('email-type', 'n_clicks'),
    Input('phone-type', 'n_clicks'),
    prevent_initial_call=True
)
def switch(n1, n2):
    triggered = ctx.triggered_id
    if triggered == 'email-type':
        return 'email-type', 'active', 'inactive'
    return 'phone-type', 'inactive', 'active'


#модуль входа
@callback(
    Output('form', 'children'),
    Input('form-store', 'data')
)
def render_form(active_tab):

    if active_tab == 'email-type':
        return EMAIL_FORM
    return PHONE_FORM


@callback(
    Output("phone_output", "children"),
    Input("phone_submit", "n_clicks"),
    State("phone_log", "value"),
    State("phone_password", "value"),
    State('form-store', 'data'),  # текущая вкладка: 'phone-type' или 'email-type'
    prevent_initial_call=True
)
def handle_phone_log(phone_clicks, phone, phone_pass, active_tab):
    db = get_db()

    triggered = ctx.triggered_id

    if triggered == "phone_submit":
        if not all([phone, phone_pass]):
            return "⚠️ Заполните все обязательные поля."

        try:
            user = db.query(Users).filter(Users.email == phone).first()

            if not user:
                return '⚠️ Пользователь с таким номером телефона не найден'

            if not check_password_hash(user.user_password, phone_pass):
                return '⚠️ Неверный пароль'

            user_id = user.user_id
            email = user.email

            return dcc.Location(id="redirect", href=f"/auth/set-token?user_id={user_id}&email={email}", refresh=True)

        except Exception as e:
            print(e)


@callback(
    Output("email_output", "children"),
    Input("email_submit", "n_clicks"),
    State("email_log", "value"),
    State("email_password", "value"),
    State('form-store', 'data'),  # текущая вкладка: 'phone-type' или 'email-type'
    prevent_initial_call=True
)
def handle_email_log(email_clicks, email, email_pass, active_tab):
    db = get_db()

    triggered = ctx.triggered_id

    if triggered == "email_submit":
        if not all([email, email_pass]):
            return "⚠️ Заполните все обязательные поля."

        try:
            user = db.query(Users).filter(Users.email == email).first()

            if not user:
                return '⚠️ Пользователь с таким email не найден'


            if not check_password_hash(user.user_password, email_pass):
                return '⚠️ Неверный пароль'

            user_id = user.user_id
            return dcc.Location(id="redirect", href=f"/auth/set-token?user_id={user_id}&email={email}", refresh=True)

        except Exception as e:
            print(e)