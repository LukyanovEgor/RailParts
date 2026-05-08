from dash import html
from .components import CatalogBut, AuthBut, AuthBar
from app.pages.header import Header


class Layout:
    def __init__(self):

        self.layout = html.Div([
            html.Div(Header()(), className="card-header"),
            html.Div([
                CatalogBut()(),
                AuthBut()(),
                AuthBar()(),
            ], className="buttons-row")
        ])



    def __call__(self, *args, **kwargs):
        return self.layout