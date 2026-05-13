from dash import html, dcc


class PartsBut:
    def __init__(self, href='/parts'): # Добавили аргумент для ссылки
        self.but = dcc.Link(
            'Поиск деталей',
            href=href,
            style={
                'backgroundColor': '#007bff',
                'color': 'white',
                'border': 'none',
                'padding': '10px 20px',
                'text-align': 'center',
                'text-decoration': 'none', # Убираем подчеркивание
                'display': 'inline-block',
                'fontSize': '16px',
                'cursor': 'pointer',
                'borderRadius': '5px',
                'margin': '10px'
            }
        )

    def __call__(self, *args, **kwargs):
        return self.but