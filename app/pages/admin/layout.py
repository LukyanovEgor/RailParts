from dash import html, dcc
from .components import ORDERS_SWITCH
from app.pages.header import Header


class Layout:
    def __init__(self):
        self.layout = html.Div(
            [
                dcc.Interval(
                    id='data-refresh-interval',
                    interval=30 * 1000,  # 30 секунд
                    n_intervals=0
                ),

                dcc.Store(id='data-store', data='all-type'),

                dcc.Download(id="download-pdf"),

                html.Div(id='dummy-output', style={'display': 'none'}),

                html.Div(Header()(), className="card-header"),
                html.Div(
                    [
                        html.H2('Заказы запчастей со склада'),

                        html.Div(
                            [ORDERS_SWITCH], className="buttons-row"
                        ),

                        html.Div(id='order-table'),

                    ]
                )
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.layout
