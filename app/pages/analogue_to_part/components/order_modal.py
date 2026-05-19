from dash import html, dcc


class InfoModal:
    def __init__(self, info):
        self.info_modal = html.Div(
            [
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
                html.Button(
                    "Закрыть", id="close-modal-btn",
                    style={'marginTop': '20px', 'padding': '8px 16px'}
                    )
            ], style={
                'backgroundColor': 'white',
                'padding': '30px',
                'marginTop': '50px',
                'marginRight': '50px',
                'borderRadius': '8px',
                'maxWidth': '400px'
            }
        )

    def __call__(self, *args, **kwargs):
        return self.info_modal