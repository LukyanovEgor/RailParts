from dash import html, dcc
from .components import CatalogBut, AuthBar, ProfileBar, PartsBut
from app.pages.header import Header


class Layout:
    def __init__(self):
        self.layout = html.Div(
            [
                dcc.Store(id='auth-trigger', data='init', storage_type='memory'),

                html.Div(Header()(), className="card-header"),
                html.Div(
                    [
                        CatalogBut()(),

                        PartsBut()(),
                        
                        html.Div(
                            id='auth-or-profile'
                        ),

                        html.Div(
                            [
                                AuthBar()(),
                            ], id="modal-overlay", style={
                                'position': 'fixed',
                                'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
                                'backgroundColor': 'rgba(0,0,0,0.5)',
                                'zIndex': 9999,
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'display': 'none'  # Скрыто по умолчанию
                            }
                        ),
                        html.Div(
                            [
                                ProfileBar()(),
                            ], id="modal-profile-overlay", style={
                                'position': 'fixed',
                                'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
                                'backgroundColor': 'rgba(0,0,0,0.5)',
                                'zIndex': 9998,
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'display': 'none'  # Скрыто по умолчанию
                            }
                        )
                    ], className="buttons-row"
                )
            ]
        )

    def __call__(self, *args, **kwargs):
        return self.layout
