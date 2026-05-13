from dash import html, dcc
from app.pages.header import Header

class Layout:
    def __init__(self):
        self.layout = html.Div(
            [
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

                        html.Div(id="product-grid", className="grid")
                    ]
                )
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.layout