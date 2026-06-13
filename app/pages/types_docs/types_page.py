from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL
from app.pages.header import Header
from .services import get_categories_tree, show_image
from app.models import OEMParts
from app.db import get_db
import dash_bootstrap_components as dbc
import json


def types_docs_layout(train_type_id=None):
    db = get_db()
    categories = []
    data = get_categories_tree(db, train_type_id)

    for category in data:
        categories.append(category)

    return html.Div(
        [
            dcc.Store(id='selected-cat-id-store', data=None),
            dcc.Store(id='train-type-id-store', data=train_type_id),

            html.Div(Header()(), className="card-header"),

            # Основной блок: категории + картинка
            html.Div(
                [
                    html.Div(
                        [
                            html.H2('Оригинальные каталоги', style={'textAlign': 'left', 'margin': '0 0 8px'}),
                            html.P('Выберите категорию', style={'textAlign': 'center', 'margin': '0 0 24px'}),
                            dcc.Loading(
                                id="loading-catalog",
                                type="circle",
                                children=html.Div(id='categories-container')
                            )
                        ], style={
                            'display': 'flex', 'flexDirection': 'column',
                            'gap': '20px', 'padding': '30px', 'width': '320px',
                            'flexShrink': 0,
                        }
                    ),
                    html.Div(id='img_output')
                ], style={
                    'display': 'flex', 'flexDirection': 'row',
                    'gap': '20px',
                    'padding': '32px 24px',
                    'marginTop': '20px',
                    'border': '1px solid #e2e8f0',
                    'borderRadius': '12px',
                    'backgroundColor': '#ffffff',
                    'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
                    'width': '100%',
                    'boxSizing': 'border-box',

                    'alignItems': 'flex-start',
                }
            ),

            html.Div(id='parts-table'),

            dbc.Modal(
                [
                    dbc.ModalBody(
                        id="modal-content",
                        style={
                            'minHeight': '300px',
                            'padding': '30px'
                        }
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Закрыть",
                            id="close-modal-btn",
                            className="ms-auto",
                            color="secondary"
                        )
                    )
                ],
                id="point-modal",
                is_open=False,
                size="sm",
                centered=True,
                fade=True,
                scrollable=True,
                style={
                    'zIndex': '9999',  # Самый верхний слой
                },
                backdrop=True

            )
        ]
    )

@callback(
    Output('categories-container', 'children'),
    Input('train-type-id-store', 'data'),
    prevent_initial_call=False
)
def show_catalog(train_type_id):
    if not train_type_id:
        return html.Div("Не выбран тип поезда", style={'color': 'gray', 'padding': '20px', 'textAlign': 'center'})

    db = get_db()
    data = get_categories_tree(db, train_type_id)

    if not data:
        return html.Div("Категории не найдены", style={'color': 'gray', 'padding': '20px', 'textAlign': 'center'})

    # Единые стили для всех уровней
    summary_style = {
        'cursor': 'pointer', 'padding': '14px 16px',
        'backgroundColor': '#ffffff', 'border': '1px solid #e2e8f0',
        'borderRadius': '8px', 'display': 'flex', 'alignItems': 'center',
        'width': '100%', 'listStyle': 'none', 'outline': 'none'
    }

    content_style = {
        'padding': '12px 16px', 'backgroundColor': '#f8fafc',
        'border': '1px solid #e2e8f0', 'borderTop': 'none',
        'borderRadius': '0 0 8px 8px', 'marginTop': '-1px'
    }

    def build_tree(category):
        children = category.get('children', [])
        has_children = len(children) > 0

        # Заголовок категории (общий для всех уровней)
        header = html.Div(
            [
                html.Span(
                    category.get('name', 'Без названия'),
                    style={'fontWeight': '600', 'fontSize': '16px', 'color': '#1a202c'}
                    ),
                html.Span(
                    f"({len(children)})", style={'color': '#718096', 'marginLeft': '8px', 'fontSize': '13px'}
                    ) if has_children else None,
                html.Span(
                    "▼", style={'marginLeft': 'auto', 'fontSize': '12px', 'color': '#a0aec0'}
                    ) if has_children else html.Span(
                    "🔗", style={'marginLeft': 'auto', 'fontSize': '12px', 'color': '#a0aec0'}
                    )
            ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'}
        )

        if has_children:
            # Если есть дети -> аккордеон
            return html.Details(
                [
                    html.Summary(header, style=summary_style),
                    html.Div([build_tree(child) for child in children], style=content_style)
                ], style={'marginBottom': '12px'}
            )
        else:
            # Если детей нет -> прямая ссылка (без <details>, чтобы избежать дублей)
            return html.Div(
                children=[
                    html.Span(f"{category.get('name')} ({category.get('code', '')})")
                ],
                # Pattern Matching ID для динамического отслеживания
                id={'type': 'category-link', 'index': str(category.get('id'))},
                n_clicks=None,  # Инициализация счётчика кликов
                style={
                    **summary_style,
                    'cursor': 'pointer',
                    'textDecoration': 'none',
                    'color': '#2d3748',

                }
            )

    # Рекурсивная сборка дерева
    return html.Div([build_tree(cat) for cat in data],
                    style={'width': '100%', 'maxWidth': '800px', 'alignItems': 'left'})


@callback(
    Output('img_output', 'children'),
    Output('selected-cat-id-store', 'data'),
    Input({'type': 'category-link', 'index': ALL}, 'n_clicks'),
    State('train-type-id-store', 'data'),
    prevent_initial_call=True
)
def handle_category_click(n_clicks_list, train_type_id):
    db = get_db()

    if not n_clicks_list or all(click is None for click in n_clicks_list):
        return no_update, no_update

    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and triggered.get('type') == 'category-link':
        category_id = triggered['index']
        url = show_image(db=db, part_category_id=category_id)

        if url:
            data = db.query(OEMParts).filter(OEMParts.category_id == category_id).all()

            points = []
            for part in data:
                if part.img_coordinates:
                    try:
                        coords = json.loads(part.img_coordinates)

                        # Если в БД лежит словарь, оборачиваем в список
                        if isinstance(coords, dict):
                            coords = [coords]
                        elif not isinstance(coords, list):
                            continue

                        for coord in coords:
                            if isinstance(coord, dict):
                                # Добавляем ID детали к координатам для надежности
                                new_point = {
                                    **coord,
                                    'part_db_id': part.id
                                }
                                points.append(new_point)
                    except (json.JSONDecodeError, TypeError) as e:
                        print(f"Ошибка парсинга JSON для детали {part.id}: {e}")

            # Генерируем кнопки
            buttons = []
            for point in points:
                # Берем ID из JSON (тот самый, что вы записали: 1, 33 и т.д.)
                point_id = point.get('id')
                part_id = point.get('part_db_id')

                buttons.append(
                    html.Button(
                        children=str(point_id),  # <-- ВИДИМЫЙ ТЕКСТ НА КНОПКЕ
                        id={"type": "point-btn", "index": part_id},  # <-- ID ДЛЯ КОЛБЭКА
                        style={
                            "position": "absolute",
                            "left": f"{point['x'] * 100}%",
                            "top": f"{point['y'] * 100}%",
                            "transform": "translate(-50%, -50%)",
                            "background": "yellow",
                            "border": "1px solid black",
                            "borderRadius": "50%",
                            "width": "24px",
                            "height": "24px",
                            "cursor": "pointer",
                            "zIndex": 10,
                            "fontWeight": "bold",
                            "fontSize": "12px"
                        }
                    )
                )

            return html.Div(
                [
                    html.Div(
                        [
                            html.Img(src=f"{url}", style={"width": "100%", "height": "auto", "display": "block"}),
                            *buttons
                        ],
                        style={"position": "relative", "width": "800px", "margin": "0 auto"}
                    ),
                ]
            ), category_id

        return None, None
    return no_update, None

@callback(
    Output("point-modal", "is_open"),
    Output("modal-content", "children"),
    Input({"type": "point-btn", "index": ALL}, "n_clicks"),
    Input("close-modal-btn", "n_clicks"),
    State("point-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(point_clicks, close_clicks, is_open):
    db = get_db()

    triggered = ctx.triggered_id

    if triggered == "close-modal-btn":
        if close_clicks and close_clicks > 0:  # Проверяем, что кнопка реально нажата
            return False, no_update
        return no_update, no_update  # Игнорируем начальную загрузку

    # Если нажали на кнопку точки
    if isinstance(triggered, dict) and triggered.get('type') == 'point-btn':

        if not point_clicks or all(click is None or click == 0 for click in point_clicks):
            return no_update, no_update

        part_id = triggered['index']
        point_data = db.query(OEMParts).filter(OEMParts.id == part_id).first()

        if not point_data:
            return no_update, html.Div("Деталь не найдена", style={'color': 'red'})


        extracted_point_id = None

        if point_data.img_coordinates:
            try:
                # 1. Превращаем строку '[{"id": 2, "x": 10}]' в список Python: [{"id": 2, "x": 10}]
                coords_list = json.loads(point_data.img_coordinates)

                # 2. Проверяем, что это список и он не пустой
                if isinstance(coords_list, list) and len(coords_list) > 0:
                    # 3. Берем первый элемент списка и получаем значение по ключу 'id'
                    extracted_point_id = coords_list[0].get('id')

            except (json.JSONDecodeError, TypeError) as e:
                print(f"Ошибка парсинга координат для детали {part_id}: {e}")

        modal_content = html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            f"Деталь {extracted_point_id}",
                            style={
                                'marginBottom': '20px',
                                'color': '#2d3748',
                                'fontSize': '24px',
                                'fontWeight': '600'
                            }
                        ),

                        # Блок с описанием
                        html.Div(
                            [
                                html.H5(
                                    "Название:",
                                    style={
                                        'color': '#4a5568',
                                        'marginBottom': '10px',
                                        'fontSize': '16px',
                                        'fontWeight': '600'
                                    }
                                ),
                                html.P(
                                    # point_data.get('description', 'Нет данных'),
                                    # 'Нет данных',
                                    point_data.name if point_data else 'Нет данных',
                                    style={
                                        'color': '#718096',
                                        'fontSize': '15px',
                                        'lineHeight': '1.6',
                                        'padding': '15px',
                                        'backgroundColor': '#f7fafc',
                                        'borderRadius': '8px',
                                        'borderLeft': '4px solid #4299e1'
                                    }
                                )
                            ], style={'marginBottom': '25px'}
                        ),

                        # Блок с OEM номером
                        html.Div(
                            [
                                html.H5(
                                    "OEM номер:",
                                    style={
                                        'color': '#4a5568',
                                        'marginBottom': '10px',
                                        'fontSize': '16px',
                                        'fontWeight': '600'
                                    }
                                ),
                                html.P(
                                    dcc.Link(
                                        point_data.oem_num if point_data else 'Нет данных',
                                        href=f"/original_catalogs/analogs/{point_data.id}"
                                    ),
                                    style={
                                        'color': '#2d3748',
                                        'fontSize': '18px',
                                        'fontWeight': '500',
                                        'fontFamily': 'monospace',
                                        'padding': '15px',
                                        'backgroundColor': '#edf2f7',
                                        'borderRadius': '8px',
                                        'textAlign': 'center'
                                    }
                                )
                            ], style={'marginBottom': '25px'}
                        ),

                    ]
                )
            ]
        )

        return True, modal_content

    return no_update, no_update

# Вспомогательная функция для получения данных о точке
def get_point_data(point_id):
    """Замените на реальный запрос к БД"""

    return {
        "description": f"Тестовое описание для точки {point_id}",
        "oem_num": f"OEM-{point_id:05d}",
    }

@callback(
    Output('parts-table', 'children'),
    Input('selected-cat-id-store', 'data'),
    prevent_initial_call=True
)
def show_parts(selected_cat_id):
    if selected_cat_id is None:
        return None

    db = get_db()
    parts = db.query(OEMParts).filter_by(category_id=selected_cat_id).all()

    rows = []
    for idx, part in enumerate(parts, start=1):
        rows.append(
            html.Tr(
                [
                    html.Td(idx, style={'fontWeight': 'bold', 'width': '50px', 'textAlign': 'center'}),
                    html.Td(part.name, style={'width': '400px'}),
                    html.Td(
                        dcc.Link(
                            part.oem_num,
                            href=f'/original_catalogs/analogs/{part.id}',
                            style={'fontFamily': 'monospace',
                                   'width': '150px',
                                   'display': 'block',
                                   'textAlign': 'center'}
                        ), style={'width': '150px',
                                  'padding': '10px',
                                  'verticalAlign': 'middle'}
                    ),
                ], style={'borderBottom': '1px solid #dee2e6'}
            )
        )

    table = html.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th('№', style={'padding': '10px', 'backgroundColor': '#f8f9fa'}),
                        html.Th(
                            'Название', style={'padding': '10px',
                                               'backgroundColor': '#f8f9fa',
                                               'textAlign': 'left'}
                        ),
                        html.Th(
                            'Оригинальный номер', style={
                                'padding': '10px',
                                'backgroundColor': '#f8f9fa',
                                'textAlign': 'left'}
                        ),
                    ]
                )
            ),
            html.Tbody(rows)
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'fontFamily': 'Arial, sans-serif'
        }
    )

    return html.Div(
        [table], style={
            'display': 'flex', 'flexDirection': 'row',
            'gap': '20px',
            'padding': '32px 24px',
            'marginTop': '20px',
            'border': '1px solid #e2e8f0',
            'borderRadius': '12px',
            'backgroundColor': '#ffffff',
            'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
            'width': '100%',
            'boxSizing': 'border-box',
        }
    )