from dash import html, dcc


class Header:
    def __init__(self):


        self.header = html.Div([

            dcc.Store(id='store-search-data'),

            dcc.Link('Рельсы-Шпалы',
                     href='/')
            ,

        ],
            style = {
                'text-align': 'center',
            }
        )


    def __call__(self, *args, **kwargs):
        return self.header

