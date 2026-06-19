from dash import html, dcc
from app.pages.header import Header
import dash_bootstrap_components as dbc


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

                        html.Div(id='order-notification', style={'marginTop': '10px'}),

                        dbc.Modal(
                            [
                                dbc.ModalBody(
                                    id="modal-content1",
                                    style={
                                        'minHeight': '300px',
                                        'padding': '30px'
                                    }
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Закрыть",
                                        id="close-modal-btn1",
                                        className="ms-auto",
                                        color="secondary"
                                    )
                                )
                            ],
                            id="point-modal1",
                            is_open=False,
                            size="sm",
                            centered=True,
                            fade=True,
                            scrollable=True,
                            style={
                                'zIndex': '9999',  # Самый верхний слой
                            },
                            backdrop=True

                        )
                    ]
                )
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.layout