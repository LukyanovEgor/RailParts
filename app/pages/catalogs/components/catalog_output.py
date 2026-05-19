from dash import html, dcc


class CatalogOutput:
    def __init__(self):
        self.catalog = html.Div([
            html.Div(
                id='output-result',
                style={
                    'margin-top': '20px',
                    'border': '1px solid #e2e8f0',
                    'border-radius': '12px',
                    'background-color': '#ffffff',
                    'box-shadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
                    'padding': '30px',
                    'width': '100%',
                    'box-sizing': 'border-box',
                    'min-height': '80px'
                }
            ),
        ])

    def __call__(self, *args, **kwargs):
        return self.catalog