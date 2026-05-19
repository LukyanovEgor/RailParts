from dash import html, dcc
from .components import AuthBar, ProfileBar
from app.pages.header import Header


class Layout:
    def __init__(self):
        self.layout = html.Div([
            dcc.Store(id='auth-trigger', data='init', storage_type='memory'),

            # Хедер
            html.Div(Header()(), className="card-header"),

            # Контейнер для динамической подмены Auth/Profile
            html.Div(id='auth-or-profile'),

            # Сетка с двумя большими карточками
            html.Div([
                # Карточка 1: Оригинальные каталоги
                dcc.Link(
                    href='/original_catalogs',
                    refresh=True,
                    className='card-link',
                    children=[
                        html.Div(className='card-content', children=[
                            html.Div('📋', className='card-icon'),
                            html.H2('Оригинальные каталоги', className='card-title'),
                            html.P('Подбор деталей по подвижному составу', className='card-subtitle')
                        ]),
                        html.Img(
                            src='/assets/orig.png',
                            className='card-img'
                        )
                    ]
                ),
                # Карточка 2: Поиск деталей
                dcc.Link(
                    href='/parts',
                    refresh=True,
                    className='card-link',
                    children=[
                        html.Div(className='card-content', children=[
                            html.Div('🔍', className='card-icon'),
                            html.H2('Поиск деталей', className='card-title'),
                            html.P('Поиск по номеру или названию', className='card-subtitle')
                        ]),
                        html.Img(
                            src='/assets/parts_button.png',
                            className='card-img'
                        )
                    ]
                )
            ], className='cards-grid'),

            # Контейнер для динамической подмены Auth/Profile
            html.Div(id='auth-or-profile'),

            # Модалки
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
        ])

    def __call__(self, *args, **kwargs):
        return self.layout