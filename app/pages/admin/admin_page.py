from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL

from functools import wraps
from flask import session, redirect, url_for, request

# Сохранение данных после успешного входа
def login_user(user_id: int, role: str):
    session['user_id'] = user_id
    session['role'] = role
    session.permanent = True  # если нужно

def logout_user():
    session.clear()

# Декоратор защиты маршрутов (Flask + Dash)
def requires_role(required_role: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('role') != required_role:
                return redirect('/login?error=access_denied')
            return f(*args, **kwargs)
        return wrapper
    return decorator

layout = html.Div(['админская странца типа'])
#
#
# admin_dash = Dash(__name__, server=app, url_base_pathname='/admin-dash/', suppress_callback_exceptions=True)
#
# admin_dash.layout = html.Div([
#     dcc.Location(id='admin-redirect', refresh=True),
#     html.Div(id='admin-content')
# ])

@callback(
    Output('admin-content', 'children'),
    Output('admin-redirect', 'href'),
    Input('admin-redirect', 'pathname')
)
def check_admin_access(pathname):
    if session.get('role') != 'admin':
        return no_update, '/login?error=access_denied'
    return html.H1('🔒 Панель администратора'), no_update