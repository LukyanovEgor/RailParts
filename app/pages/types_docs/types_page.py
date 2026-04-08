from .layout import Layout
from dash import html

# def types_docs_layout(train_type_id=None, **kwargs):
#
#     print(f"🔍 Получено: train_type_id={train_type_id}, kwargs={kwargs}")  # Отладка
#     return Layout(train_type_id=train_type_id)()
#
# def types_docs_layout():
#     layout = html.Div([
#         html.Div([
#             html.P('Номер вагона: 8867')
#         ],
#             style={'background-color': '#f0ffff',
#                    }
#         ),
#         html.Div([
#             html.H2('Оригинальные каталоги', style={'align': 'center',
#                                                             'padding-left': '200px',
#                                                             'padding-right': '200px'}),
#             html.Div(
#                     'Выберите категорию',
#                     style = {'align': 'center',
#                             'margin': '70px',
#                              'padding-left': '200px',
#                              'padding-right': '200px',
#                              'padding-top': '100px',
#                             }
#             )
#         ], style={'background-color': '#f0ffff',
#                   'padding-top': '100px',
#                   })
#     ], style={
#                 'display': 'flex',
#                 'justify-content': 'center',
#                 'align-items': 'center',
#                 'gap': '20px',
#                 # 'align': 'center',
#                 'border': '2px solid',  # 333;
#                 'padding': '20px',
#                 # 'height': '200px'
#             })
#
#     return layout

from dash import html, dcc, callback, Input, Output
import dash


# ---------------------------------------------------------
# 🔽 ЗАГЛУШКА ДЛЯ БД (замените на ваш реальный запрос)
# ---------------------------------------------------------
def fetch_categories_db(train_type_id: int):
    """Возвращает список категорий с вложенными подкатегориями"""
    return [
        {
            "id": 1, "name": "Тормозная система", "code": "BRK",
            "children": [
                {
                    "id": 3, "name": "Тормозная система", "code": "BRK",
                    "children": [
                        {"id": 103, "name": "Колодки", "code": "BRK-PAD"},
                        {"id": 104, "name": "Диски", "code": "BRK-DSK"},
                    ]
                },
                {"id": 102, "name": "Диски", "code": "BRK-DSK"},
            ]
        },
        {
            "id": 2, "name": "Ходовая часть", "code": "SUS",
            "children": [
                {"id": 201, "name": "Рессоры", "code": "SUS-SPR"},
                {"id": 202, "name": "Амортизаторы", "code": "SUS-SHK"},
            ]
        }
    ]


# ---------------------------------------------------------
# 🟢 CALLBACK: рендеринг аккордеона (только инлайн-стили)
# ---------------------------------------------------------
@callback(
    Output('categories-container', 'children'),
    Input('train-type-id-store', 'data'),
    prevent_initial_call=False
)
def render_collapsible_catalog(train_type_id):
    if not train_type_id:
        return html.P("❌ Тип поезда не указан", style={'color': '#e53e3e', 'textAlign': 'center'})

    try:
        train_id = int(train_type_id)
    except ValueError:
        return html.P("❌ Некорректный ID", style={'color': '#e53e3e', 'textAlign': 'center'})

    catalog_data = fetch_categories_db(train_id)
    if not catalog_data:
        return html.P("📭 Категории для данного типа поезда не найдены.",
                      style={'color': '#718096', 'textAlign': 'center', 'marginTop': '40px'})

    accordion_items = []
    for cat in catalog_data:
        # Ссылки на подкатегории
        sub_links = [
            html.A(
                f"🔹 {child['name']} ({child['code']})",
                href=f"/original_catalogs/{train_id}/category/{child['id']}",
                style={
                    'display': 'block', 'padding': '10px 14px', 'margin': '6px 0',
                    'textDecoration': 'none', 'color': '#2d3748',
                    'backgroundColor': '#f7fafc', 'borderRadius': '6px',
                    'border': '1px solid #e2e8f0', 'fontSize': '14px'
                }
            ) for child in cat['children']
        ]

        # Стили для заголовка категории
        summary_style = {
            'cursor': 'pointer', 'padding': '14px 16px',
            'backgroundColor': '#ffffff', 'border': '1px solid #e2e8f0',
            'borderRadius': '8px', 'display': 'flex', 'alignItems': 'center',
            'width': '100%', 'listStyle': 'none', 'outline': 'none'
        }

        # Стили для контента подкатегорий
        content_style = {
            'padding': '12px 16px', 'backgroundColor': '#f8fafc',
            'border': '1px solid #e2e8f0', 'borderTop': 'none',
            'borderRadius': '0 0 8px 8px'
        }

        # Элемент аккордеона
        item = html.Details([
            html.Summary(
                html.Div([
                    html.Span(cat['name'], style={'fontWeight': '600', 'fontSize': '16px', 'color': '#1a202c'}),
                    html.Span(f"({len(cat['children'])})",
                              style={'color': '#718096', 'marginLeft': '8px', 'fontSize': '13px'}),
                    html.Span("▼", style={'marginLeft': 'auto', 'fontSize': '12px', 'color': '#a0aec0'})
                ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'})
                , style=summary_style),
            html.Div(sub_links, style=content_style)
        ], style={'marginBottom': '12px', 'border': 'none'})
        accordion_items.append(item)

    return html.Div(accordion_items, style={'width': '100%', 'maxWidth': '800px'})


# ---------------------------------------------------------
# 🟢 LAYOUT СТРАНИЦЫ
# ---------------------------------------------------------
def types_docs_layout(train_type_id=None, **kwargs):
    default_id = train_type_id or "8867"

    return html.Div([
        dcc.Store(id='train-type-id-store', data=default_id),

        html.Div([
            html.P(f'Тип поезда: {default_id}', style={'margin': 0, 'fontWeight': '600'})
        ], style={
            'backgroundColor': '#f0ffff', 'padding': '14px 20px',
        }),

        html.Div([
            html.H2('Оригинальные каталоги', style={'textAlign': 'center', 'margin': '0 0 8px'}),
            html.P('Выберите категорию', style={'textAlign': 'center', 'margin': '0 0 24px'}),

            dcc.Loading(
                id="loading-catalog",
                type="circle",
                children=html.Div(id='categories-container')
            )
        ], style={
            'backgroundColor': '#f0ffff', 'padding': '32px 24px',
             'marginTop': '20px', 'maxWidth': '3800px',
        })
    ], style={
        'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center',
        'gap': '20px', 'padding': '30px', 'maxWidth': '5000px', 'margin': '0 auto'
    })