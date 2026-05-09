from dash import html, dcc


EMAIL_FORM = html.Div([
    html.H2("Вход в аккаунт", style={'textAlign': 'center'}),
    html.Label("Email *",  className ='label_style'),
    dcc.Input(id="email_log", type="email", placeholder="user@example.com", className ='input_style'),
    html.Label("Пароль *", className ='label_style'),
    dcc.Input(id="email_password", type="password", placeholder="Минимум 6 символов", className ='input_style'),
    html.Button("Войти", id="email_submit", className ='btn_style', n_clicks=0),
    html.Div(id="email_output", style={'marginTop': '15px', 'textAlign': 'center', 'fontWeight': 'bold'}),
], className="form_style")