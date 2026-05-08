from dash import html


class AuthBut:
    def __init__(self):  # Добавили id
        self.but = html.Button(
            'Зарегистрироваться или войти',
            id='show-auth-modal',  # ID для callback
            style={
                'backgroundColor': '#007bff',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'text-align': 'center',
                'text-decoration': 'none',
                'display': 'inline-block',
                'fontSize': '16px',
                'cursor': 'pointer',
                'borderRadius': '5px',
                'margin': '10px'
            }
        )

    def __call__(self, *args, **kwargs):
        return self.but