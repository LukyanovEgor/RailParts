from .layout import Layout
from dash import html, dcc, Input, Output, callback, State
from app.db import get_db, Base
from .services.train_searcher import search_train_db


db = get_db()
Base.metadata.create_all(bind=db.bind, checkfirst=True)

layout = Layout()


# --- ЛОГИКА (CALLBACKS) ---
@callback(
    Output('output-result', 'children'),
    Input('btn-search', 'n_clicks'),  # Триггер: клик по кнопке
    State('input-part-number', 'value')  # Состояние: значение поля ввода
)
def update_output(n_clicks, part_number):

    # Защита от срабатывания при загрузке страницы
    if not n_clicks or not part_number:
        return 'Введите артикул и нажмите "Найти"'

    info = search_train_db(db, part_number)

    if info:
        return dcc.Link(
            html.Div([
                html.P(f"Поезд найден: {info['train']['unique_id']}",),
                html.P(f"Тип поезда: {info['train_type']['name']}"),
                html.P(f"Дата выпуска: {info['train']['manufactured_date']}"),
                html.P('Описание:'),
                html.P(info['train_type']['description']),
                html.P(info['train']['details']),
            ]),
            href=f'/original_catalogs/{info["train_type"]["id"]}'
        )
    return html.Div([
        html.P(f"Поезд с уникальным ID '{part_number}' не найден.")
    ])
