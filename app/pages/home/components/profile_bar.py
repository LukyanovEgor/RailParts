from dash import html, dcc


class ProfileBar:
    def __init__(self):
        self.profile_bar = html.Div(
            [
                html.H2("Меню"),
                dcc.Link(
                    html.P('Профиль'),
                    href="/signin"
                ),

                dcc.Link(
                    html.P('Депо'),
                    href="/signup"
                ),

                dcc.Link(
                    html.P('Избранные'),
                    href="/signup"
                ),

                html.A('Выйти', href="/auth/logout"),

                html.Button(
                    "Закрыть", id="close-profile-btn",
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
        return self.profile_bar
