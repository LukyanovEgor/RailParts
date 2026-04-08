from dash import html
from .components import CatalogBut
from app.pages.header import Header


class Layout:
    def __init__(self):

        self.layout = html.Div(

            [
                html.Div(Header()(), className="card-header"),
                html.Div(CatalogBut()(), className="r"),
            ]
        )


    def __call__(self, *args, **kwargs):
        return self.layout