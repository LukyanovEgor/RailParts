from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL
from app.pages.header import Header
from .services import get_categories_tree, show_image
from app.db import get_db


def types_docs_layout(train_type_id=None):

    db = get_db()

    categories = []

    data = get_categories_tree(db, train_type_id)

    for category in data:
        categories.append(category)

    return html.Div([
        dcc.Store(id='train-type-id-store', data=train_type_id),

        html.Div(Header()(), className="card-header"),

        html.Div([
            html.P(f'Тип поезда: {train_type_id}')
        ], style={
            'backgroundColor': '#f0ffff',
        }),

        html.Div([
            html.Div([
                html.H2('Оригинальные каталоги', style={'textAlign': 'left', 'margin': '0 0 8px'}),
                html.P('Выберите категорию', style={'textAlign': 'center', 'margin': '0 0 24px'}),

                dcc.Loading(
                    id="loading-catalog",
                    type="circle",
                    children=html.Div(id='categories-container')
                )
            ], style={
                'display': 'flex', 'flexDirection': 'column',
                'gap': '20px', 'padding': '30px', 'margin': '0 auto'
            }),
            html.Div(id='img_output')
        ], style={
            'display': 'flex', 'flexDirection': 'row',
            'gap': '20px',
            'padding': '32px 24px',
            'marginTop': '20px', 'border': '2px solid'
        }),
    ])


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
        header = html.Div([
            html.Span(category.get('name', 'Без названия'), style={'fontWeight': '600', 'fontSize': '16px', 'color': '#1a202c'}),
            html.Span(f"({len(children)})", style={'color': '#718096', 'marginLeft': '8px', 'fontSize': '13px'}) if has_children else None,
            html.Span("▼", style={'marginLeft': 'auto', 'fontSize': '12px', 'color': '#a0aec0'}) if has_children else html.Span("🔗", style={'marginLeft': 'auto', 'fontSize': '12px', 'color': '#a0aec0'})
        ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'})

        if has_children:
            # Если есть дети -> аккордеон
            return html.Details([
                html.Summary(header, style=summary_style),
                html.Div([build_tree(child) for child in children], style=content_style)
            ], style={'marginBottom': '12px'})
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
    return html.Div([build_tree(cat) for cat in data], style={'width': '100%', 'maxWidth': '800px'})


@callback(
    Output('img_output', 'children'),
    Input({'type': 'category-link', 'index': ALL}, 'n_clicks'),
    State('train-type-id-store', 'data'),
    prevent_initial_call=True
)
def handle_category_click(n_clicks_list, train_type_id):
    if not n_clicks_list or all(click is None for click in n_clicks_list):
        return no_update

    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and triggered.get('type') == 'category-link':
        category_id = triggered['index']

        url = show_image(db = get_db(), part_category_id=category_id)

        if url:
            return html.Div(
                    html.Img(src=f"{url}", style={"width": "1100px", "height": "700px"})
                )
        return None
    return no_update