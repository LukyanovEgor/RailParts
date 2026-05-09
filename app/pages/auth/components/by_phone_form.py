from dash import html, dcc


PHONE_FORM = html.Div([
    html.H2("Вход в аккаунт", style={'textAlign': 'center'}),
    html.Label("Телефон *",  className ='label_style'),
    dcc.Input(id="phone_log", type="tel", placeholder="+7 (999) 999-99-99",  className ='input_style'),
    html.Label("Пароль *", className ='label_style'),
    dcc.Input(id="phone_password", type="password", placeholder="Минимум 6 символов", className ='input_style'),
    html.Button("Войти", id="phone_submit", className ='btn_style', n_clicks=0),
    html.Div(id="phone_output", style={'marginTop': '15px', 'textAlign': 'center', 'fontWeight': 'bold'}),
], className="form_style")