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