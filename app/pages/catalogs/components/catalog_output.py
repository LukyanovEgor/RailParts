from dash import html, dcc


class CatalogOutput:
    def __init__(self):
        self.catalog = html.Div([

            html.Div(
                id='output-result', style={
                    'margin-top': '20px',
                    'border': '2px solid',
                }
            ),
        ])

    def __call__(self, *args, **kwargs):
        return self.catalog
