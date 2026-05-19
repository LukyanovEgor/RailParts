from dash import html, dcc
from app.pages.header import Header

class Layout:
    def __init__(self):
        self.layout = html.Div(
            [
                dcc.Location(id='url-redirect', refresh=True),

                Header()(),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Span("🔍", style={"marginRight": "10px", "fontSize": "18px"}),
                                dcc.Input(
                                    id="search-input", className="search-input", type="text",
                                    placeholder="Введите артикул, наименование, код оригинальной детали"
                                )
                            ], className="search-box"
                        ),

                        html.Div(id="product-grid", className="grid"),

                        html.Div(id='order-notification', style={'marginTop': '10px'})
                    ]
                )
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.layout