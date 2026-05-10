from dash import html


class UserBut:
    def __init__(self, username="User"):
        self.but = html.Button(
            children=[
                html.Div(
                    html.Img(
                        src='/assets/no_icon_user.png',
                        style={'width': '12px', 'height': '12px', 'filter': 'brightness(0) invert(1)'}
                    ),
                    style={
                        'width': '20px', 'height': '20px',
                        'backgroundColor': '#cccccc',  # серый прямоугольный фон
                        'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                        'marginRight': '8px',
                        'borderRadius': '4px'
                    }
                ),
                html.Span(username, style={'fontWeight': '500', 'fontSize': '15px'})
            ],
            id='show-profile-modal',
            style={
                'backgroundColor': '#007bff', 'color': 'white', 'border': 'none',
                'padding': '8px 14px',
                'display': 'inline-flex', 'alignItems': 'center',
                'cursor': 'pointer', 'borderRadius': '6px',
                'whiteSpace': 'nowrap',
                'flexShrink': '0'
            }
        )

    def __call__(self):
        return self.but
