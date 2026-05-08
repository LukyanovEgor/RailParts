from dash import html, dcc
from app.pages.auth import SWITCH
from app.pages.header import Header

class Layout:
    def __init__(self):
        form_style = {
            'maxWidth': '400px', 'margin': '20px auto', 'padding': '20px',
            'border': '1px solid #ddd', 'borderRadius': '8px',
            'fontFamily': 'Arial, sans-serif'
        }
        input_style = {'padding': '8px', 'margin': '5px 0 10px', 'width': '100%', 'boxSizing': 'border-box'}
        label_style = {'fontWeight': 'bold', 'marginTop': '10px', 'display': 'block'}
        btn_style = {
            'padding': '10px', 'backgroundColor': '#007BFF', 'color': '#fff',
            'border': 'none', 'borderRadius': '4px', 'cursor': 'pointer',
            'width': '100%', 'marginTop': '10px', 'fontSize': '16px'
        }

        self.layout = html.Div([
            html.Div(Header()(), className="card-header"),
            html.Div([
                SWITCH,
                html.Div([
                    html.H2("Вход в аккаунт", style={'textAlign': 'center'}),
                    html.Label("Email *", style=label_style),
                    dcc.Input(id="email_log", type="email", placeholder="user@example.com", style=input_style),
                    html.Label("Телефон *", style=label_style),
                    dcc.Input(id="phone_log", type="tel", placeholder="+7 (999) 999-99-99", style=input_style),
                    html.Label("Пароль *", style=label_style),
                    dcc.Input(id="password_log", type="password", placeholder="Минимум 6 символов", style=input_style),
                    html.Button("Войти", id="submit-btn", style=btn_style, n_clicks=0),
                    html.Div(id="output-msg", style={'marginTop': '15px', 'textAlign': 'center', 'fontWeight': 'bold'}),
                ], style=form_style)
            ], className="buttons-row")
        ])

    def __call__(self):
        return self.layout