from dash import html


class UserBut:
    def __init__(self, username="User", icon=None):

        style = {'width': '20px', 'height': '20px', 'borderRadius': '4px'}

        if icon is None:
            icon = '/assets/no_icon_user.png'
            style={'width': '12px', 'height': '12px', 'borderRadius': '4px'}

        self.but = html.Button(
            children=[
                html.Div(
                    html.Img(
                        src=icon,
                        style=style
                    ),
                    style={
                        'width': '20px', 'height': '20px',
                        'backgroundColor': '#cccccc',  # серый прямоугольный фон
                        'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                        'marginRight': '8px',
                        'borderRadius': '4px',
                        'align': 'right',
                    }
                ),
                html.Span(username, style={'fontWeight': '500', 'fontSize': '15px'})
            ],
            id='show-profile-modal1',
            n_clicks=0,
            style={
                'backgroundColor': '#8B0000', 'color': 'white', 'border': 'none',
                'padding': '8px 14px',
                'display': 'inline-flex', 'alignItems': 'center',
                'cursor': 'pointer', 'borderRadius': '6px',
                'whiteSpace': 'nowrap',
                'flexShrink': '0'
            }
        )

    def __call__(self):
        return self.but
