from dash import html, dcc


class AuthBar:
    def __init__(self):
        self.auth_bar = html.Div([
            html.Div([
                html.H2("Авторизация"),
                dcc.Link(
                    html.P('Войти в аккаунт'),
                    href="/signin"
                ),
                html.P("Еще нет аккаунта?"),
                dcc.Link(
                    html.P('Зарегистрироваться'),
                    href="/signup"
                ),
                html.Button("Закрыть", id="close-modal-btn",
                            style={'marginTop': '20px', 'padding': '8px 16px'})
            ], style={
                'backgroundColor': 'white',
                'padding': '30px',
                'marginTop': '50px',
                'marginRight': '50px',
                'borderRadius': '8px',
                'maxWidth': '400px'
            })
        ], id="modal-overlay", style={
            'position': 'fixed',
            'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'zIndex': 9999,
            'justifyContent': 'center',
            'alignItems': 'center',
            'display': 'none'  # Скрыто по умолчанию
        })

    def __call__(self, *args, **kwargs):
        return self.auth_bar