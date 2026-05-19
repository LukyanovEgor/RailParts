from .layout import Layout
from dash import ctx, callback, callback_context, Output, Input
from .components import AuthBut, UserBut, AuthBar
from app.models import Users
from app.db import get_db
from flask import request
import jwt


layout = Layout()


@callback(
    Output('auth-or-profile', 'children'),
    Input('auth-trigger', 'data'),          # Обязательный Input (срабатывает при инициализации)
    prevent_initial_call=False              # Запускается сразу при загрузке страницы
)
def check_jwt_and_render(_):

    token = request.cookies.get('auth_token')

    try:
        # 2. Декодируем токен (замените на ваш SECRET_KEY)
        try:
            payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        except Exception as e:

            return AuthBut()()

        user_id = payload.get("user_id")

        if user_id:

            db = get_db()

            user = db.query(Users).filter(Users.user_id == user_id).first()

            return UserBut(username=user.firstname)()

        return AuthBut()()

    except Exception as e:
        print(e)
        return AuthBut()()


# Callback для управления видимостью окна авторизации
@callback(
    Output("modal-overlay", "style"),
    Input("show-auth-modal", "n_clicks"),
    Input("close-modal-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(open_clicks, close_clicks):

    ctx = callback_context
    if not ctx.triggered:
        return {'display': 'none'}

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "show-auth-modal" and open_clicks:
        return {
            'position': 'fixed',
            'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'zIndex': 9999,
            'display': 'flex',
            'justifyContent': 'flex-end',
            'alignItems': 'flex-start',
        }
    else:
        return {'display': 'none'}


# Callback для управления видимостью окна профиля
@callback(
    Output("modal-profile-overlay", "style"),
    Input("show-profile-modal", "n_clicks"),
    Input("close-profile-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal_profile(open_clicks, close_clicks):

    ctx = callback_context
    if not ctx.triggered:
        return {'display': 'none'}

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "show-profile-modal" and open_clicks:
        return {
            'position': 'fixed',
            'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'zIndex': 9999,
            'display': 'flex',
            'justifyContent': 'flex-end',
            'alignItems': 'flex-start',
        }
    else:
        return {'display': 'none'}