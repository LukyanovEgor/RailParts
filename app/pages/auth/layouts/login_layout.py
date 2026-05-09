from dash import html, dcc
from app.pages.auth import SWITCH
from app.pages.header import Header


class Layout:
    def __init__(self):
        self.layout = html.Div(
            [
                dcc.Store(id='form-store', data='phone'),

                html.Div(Header()(), className="card-header"),
                html.Div([SWITCH], className="buttons-row"),


                html.Div(
                    id="form",
                    style={
                        'display': 'flex',
                        'justifyContent': 'center',
                        'width': '100%',
                        'marginTop': '20px'
                    }
                ),
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'width': '100%',
                'minHeight': '100vh'
            }
        )

    def __call__(self):
        return self.layout