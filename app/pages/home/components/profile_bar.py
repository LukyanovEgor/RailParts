# from dash import html, dcc
#
#
# class ProfileBar:
#     def __init__(self):
#
#
#         self.profile_bar = html.Div(
#             [
#                 html.H2("Меню"),
#                 dcc.Link(
#                     html.P('Профиль'),
#                     href="/profile"
#                 ),
#
#                 html.A('Мои заказы', href="/orders/redirect/my_orders/"),
#
#                 dcc.Link(
#                     html.P('Депо'),
#                     href="/signup"
#                 ),
#
#                 dcc.Link(
#                     html.P('Избранные'),
#                     href="/signup"
#                 ),
#
#                 html.A('Выйти', href="/auth/logout"),
#
#                 html.Button(
#                     "Закрыть", id="close-profile-btn",
#                     style={'marginTop': '20px', 'padding': '8px 16px'}
#                     )
#             ], style={
#                 'backgroundColor': 'white',
#                 'padding': '30px',
#                 'marginTop': '50px',
#                 'marginRight': '50px',
#                 'borderRadius': '8px',
#                 'maxWidth': '400px'
#             }
#         )
#
#     def __call__(self, *args, **kwargs):
#         return self.profile_bar

from dash import html, dcc

class ProfileBar:
    def __init__(self):
        self.profile_bar = html.Div([
            html.H2("Меню", className="profile-title"),

            # Ссылки выстроены в столбик
            html.Div([
                dcc.Link('Профиль', href="/profile", className="profile-link"),
                html.A('Мои заказы', href="/orders/redirect/my_orders/", className="profile-link"),
                dcc.Link('Депо', href="/signup", className="profile-link"),
                dcc.Link('Избранные', href="/signup", className="profile-link"),
                html.A('Выйти', href="/auth/logout", className="profile-link"),
            ], className="profile-links"),

            # Кнопка под ссылками
            html.Button("Закрыть", id="close-profile-btn", className="btn_style_profile")
        ], className="profile-bar")

    def __call__(self, *args, **kwargs):
        return self.profile_bar