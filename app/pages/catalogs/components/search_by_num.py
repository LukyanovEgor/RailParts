# from dash import html, dcc
#
#
# class ByNumSearcher:
#     def __init__(self):
#         self.searcher = html.Div([
#
#             dcc.Store(id='store-search-data'),
#
#             html.Div([
#                 html.Div([
#                     html.Div(
#                         html.H2('Оригинальные каталоги'), style={'font-weight': 'bold'}
#                     ),
#                     html.Div(
#                         'Искать по номеру',
#                         style={
#
#                         }
#                     ),
#                     html.Div([
#
#                         dcc.Input(
#                             id='input-part-number',
#                             type='text',
#                             placeholder='Введите номер (например: 81-717)',
#                             debounce=True,  # Отправлять данные только после паузы в вводе
#                             style={'width': '300px', 'padding': '10px'}
#                         ),
#
#                         html.Button('Найти', id='btn-search', n_clicks=0,
#                                     style={'margin-left': '10px', 'padding': '10px'}),
#
#                     ]),
#                     html.Div(
#                         [
#                             'Например:',
#                             html.A(
#                                 '8867'
#                             ),
#                             " или ",
#                             html.A(
#                                 '8867'
#                             ),
#
#                         ], style={}
#                     )
#                 ], style={'background-color': '#f0ffff'}
#                 ),
#                 html.Div(style={
#                     'width': '2px',  # Толщина
#                     'height': '100%',  # Высота
#                     'background-color': 'black',  # Цвет
#                     'margin': '0 20px',  # Отступы слева и справа
#                 }),
#                 html.Div([
#                     html.H2('Поиск по названию состава')
#                     ], style={'background-color': '#f0ffff'}
#                 )
#             ], style={
#                 'display': 'flex',
#                 'justify-content': 'center',
#                 'align-items': 'center',
#                 'gap': '20px',
#
#                 'border': '2px solid',  # 333;
#                 'padding': '20px',
#                 'height': '200px'
#             }
#             ),
#         ], style={}
#         )
#
#     def __call__(self, *args, **kwargs):
#         return self.searcher
from dash import html, dcc

class ByNumSearcher:
    def __init__(self):
        self.searcher = html.Div([
            dcc.Store(id='store-search-data'),

            html.Div([
                # Левая карточка: Поиск по номеру
                html.Div([
                    html.H2('Оригинальные каталоги', className="card-title"),
                    html.Div('Искать по номеру', className="card-label"),
                    html.Div([
                        dcc.Input(
                            id='input-part-number',
                            type='text',
                            placeholder='Введите номер (например: 81-717)',
                            debounce=True,
                            className="search-input"
                        ),
                        html.Button('Найти', id='btn-search', n_clicks=0, className="btn_style")
                    ], className="search-row"),
                    html.Div([
                        html.Span('Например:'),
                        html.A('8867', href='#', className="example-link"),
                    ], className="card-hint")
                ], className="card search-card"),

                # Разделитель (опционально)
                html.Div(className="divider"),

                # Правая карточка: Поиск по названию
                html.Div([
                    html.H2('Поиск по названию состава', className="card-title"),
                    # Сюда можно добавить input для поиска по названию
                ], className="card name-card")
            ], className="searcher-container")
        ])

    def __call__(self, *args, **kwargs):
        return self.searcher