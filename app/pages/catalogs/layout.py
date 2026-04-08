from dash import html, dcc
from .components import ByNumSearcher, CatalogOutput
from app.pages.header import Header


class Layout:
    def __init__(self):

        self.layout = html.Div(

            [


                html.Div(Header()(), className="header"),
                html.Div([
                    ByNumSearcher()(),
                    CatalogOutput()(),
                ]),
            ]
        )


    def __call__(self, *args, **kwargs):
        return self.layout