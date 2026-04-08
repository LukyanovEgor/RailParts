from dash import html
from app.pages.header import Header


class Layout:
    def __init__(self, train_type_id: str = None):

        self.train_type_id = train_type_id

        self.layout = html.Div(

            [


                html.Div(Header()(), className="header"),
                html.Div([
                    train_type_id
                ]),
            ]
        )


    # def __call__(self, *args, **kwargs):
    #     return self.layout

    def __call__(self, *args, **kwargs):
        # ✅ __call__ будет вызван Dash с параметрами маршрута
        return html.Div([
            html.Div(Header()(), className="header"),
            html.Div([
                html.H2(f"Тип поезда: {self.train_type_id}"),
            ]),
        ])

# # Фабричная функция для Dash
# def types_docs_layout(train_type_id=None, **kwargs):
#     return Layout(train_type_id=train_type_id)()