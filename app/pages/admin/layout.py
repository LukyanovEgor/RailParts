from dash import html, dcc
# from .components import CatalogBut, AuthBar, ProfileBar, PartsBut
from app.pages.header import Header


class Layout:
    def __init__(self):
        self.layout = html.Div(
            [
                dcc.Store(id='auth-trigger', data='init', storage_type='memory'),

                html.Div(Header()(), className="card-header"),
                html.Div(
                    [
                        # CatalogBut()(),
                        #
                        # PartsBut()(),



                    ], className="buttons-row"
                )
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.layout
