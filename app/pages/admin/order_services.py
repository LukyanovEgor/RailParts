from dash import Output, Input, callback, html, callback_context, ALL, no_update, ctx, dcc
import dash
from sqlalchemy.orm import joinedload
from sqlalchemy import select, or_, cast, String
from app.models import Orders, OrderItems, Users, AnalogueParts, OEMParts
from app.db import get_db


def render_all():
    db = get_db()
    try:
        # Загружаем заказы сразу с элементами и привязанными деталями (без N+1 запросов)

        orders = db.query(Orders).options(
            joinedload(Orders.items).joinedload(OrderItems.oem_part),
            joinedload(Orders.items).joinedload(OrderItems.analogue_part)
        ).order_by(
            Orders.created_at.desc()  # Сортировка по убыванию (от новых к старым)
        ).all()

        if not orders:
            return html.Div(
                "Заказы пока не оформлены",
                style={'textAlign': 'center', 'padding': '40px', 'color': '#718096'}
            )

        rows = []
        for order in orders:
            # Формируем список товаров с количеством
            items_list = []
            if order.items:
                for item in order.items:
                    part_info = "Неизвестная деталь"
                    if item.oem_part:
                        part_info = f"{item.oem_part.name} ({item.oem_part.oem_num})"
                    elif item.analogue_part:
                        part_info = f"{item.analogue_part.name} ({item.analogue_part.analogue_num})"

                    items_list.append(
                        html.Div(f" {part_info} - {item.quantity} шт.", style={'marginBottom': '6px'})
                    )
            else:
                items_list.append(html.Div("Пустой заказ", style={'color': '#a0aec0'}))

            # Безопасное форматирование даты
            created_date = order.created_at.strftime('%Y-%m-%d %H:%M') if order.created_at else '-'

            stmt = (
                select(Users)
                .where(Users.user_id == order.user_id)
            )

            user = db.scalar(stmt)

            firstname = user.firstname if user else ''
            lastname = user.lastname if user else ''
            patronymic = user.patronymic if user else ''

            rows.append(
                html.Tr(
                    [
                        html.Td(
                            order.id, style={'padding': '12px',
                                             'textAlign': 'center',
                                             'fontWeight': 'bold'
                                             }
                            ),
                        html.Td(f"{lastname} {firstname} {patronymic}", style={'padding': '12px'}),
                        html.Td(html.Div(items_list), style={'padding': '12px'}),
                        html.Td(
                            created_date, style={
                                'padding': '12px',
                                'whiteSpace': 'nowrap',
                                'textAlign': 'center'
                            }
                            ),
                        html.Td(
                            f'{order.status}', style={
                                'padding': '12px',
                                'whiteSpace': 'nowrap',
                                'textAlign': 'center'
                            }
                            ),
                        html.Td(
                            html.Button(
                                "Создать документ",
                                id={'type': 'btn-create-doc', 'index': order.id},
                                className='btn_style',
                                n_clicks=0
                            ),
                            style={'padding': '12px', 'textAlign': 'center'}
                        )
                    ], style={'borderBottom': '1px solid #e2e8f0'}
                )
            )

        table = html.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th(
                                '№', style={'padding': '12px', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}
                            ),
                            html.Th(
                                'Оформитель', style={
                                    'padding': '12px',
                                    'backgroundColor': '#f8f9fa',
                                    'textAlign': 'left'
                                }
                                ),
                            html.Th(
                                'Состав заказа', style={
                                    'padding': '12px',
                                    'backgroundColor': '#f8f9fa',
                                    'textAlign': 'left'
                                }
                                ),
                            html.Th(
                                'Дата формирования',
                                style={'padding': '12px',
                                       'backgroundColor': '#f8f9fa',
                                       'whiteSpace': 'nowrap',
                                       'align': 'center'}
                            ),

                            html.Th(
                                'Статус',
                                style={'padding': '12px', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}
                            ),

                            html.Th(
                                'Действие',
                                style={'padding': '12px', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}
                            )
                        ]
                    )
                ),
                html.Tbody(rows)
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px'
            }
        )

        return html.Div(
            [table], style={
                'border': '1px solid #e2e8f0',
                'borderRadius': '12px',
                'backgroundColor': '#ffffff',
                'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
                'width': '100%',
                'boxSizing': 'border-box',
                'padding': '20px',
                'marginTop': '20px'
            }
        )

    except Exception as e:
        return html.Div(f"Ошибка загрузки!", style={'color': '#e53e3e', 'padding': '20px'})


def render_by_users():
        return html.Div(
            [
                html.Div(
                    [
                        html.Div('Поиск', className="card-label"),
                        html.Div(
                            [
                                dcc.Input(
                                    id='input-order',
                                    type='text',
                                    placeholder='Поиск по оформителю, Составу заказа, Статусу',
                                    className="search-input"
                                ),

                            ], className="search-row"
                        ),
                    ]
                ),
                html.Div(id='filtered-table')
            ], style={
                'border': '1px solid #e2e8f0',
                'borderRadius': '12px',
                'backgroundColor': '#ffffff',
                'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.08)',
                'width': '100%',
                'boxSizing': 'border-box',
                'padding': '20px',
                'marginTop': '20px'
            }
        )


def render_filtered_table(filter=None):

    if not filter:
        return html.Div(
            "Введите поисковый запрос",
            style={'textAlign': 'center', 'padding': '40px', 'color': '#718096'}
        ),

    db = get_db()
    try:

        # Базовый запрос с подгрузкой связанных данных (чтобы не делать N+1 запросов)
        query = db.query(Orders).options(
            joinedload(Orders.items).joinedload(OrderItems.oem_part),
            joinedload(Orders.items).joinedload(OrderItems.analogue_part)
        )


        query = query.join(Users, Orders.user_id == Users.user_id)

        # Если есть поисковый запрос, применяем сложные условия фильтрации
        if filter and filter.strip():
            term = f"%{filter.strip()}%"  # Добавляем % для поиска подстроки (ilike - регистронезависимый)

            search_condition = or_(
                # 1. Поиск по ФИО пользователя
                Users.lastname.ilike(term),
                Users.firstname.ilike(term),
                Users.patronymic.ilike(term),

                # 2. Поиск по статусу заказа
                Orders.status.ilike(term),

                # 3. Поиск по дате (преобразуем дату в строку, чтобы искать "2023", "15" и т.д.)
                cast(Orders.created_at, String).ilike(term),

                # 4. Поиск по составу заказа (OEM детали)
                Orders.items.any(
                    or_(
                        OrderItems.oem_part.has(OEMParts.name.ilike(term)),
                        OrderItems.oem_part.has(OEMParts.oem_num.ilike(term))
                    )
                ),

                # 5. Поиск по составу заказа (Аналоги)
                Orders.items.any(
                    or_(
                        OrderItems.analogue_part.has(AnalogueParts.name.ilike(term)),
                        OrderItems.analogue_part.has(AnalogueParts.analogue_num.ilike(term))
                    )
                )
            )

            query = query.filter(search_condition)

        # Сортировка от новых к старым
        orders =  query.order_by(Orders.created_at.desc()).all()

        if not orders:
            return html.Div(
                "Заказы не найдены",
                style={'textAlign': 'center', 'padding': '40px', 'color': '#718096'}
            )

        rows = []
        for order in orders:
            # Формируем список товаров с количеством
            items_list = []
            if order.items:
                for item in order.items:
                    part_info = "Неизвестная деталь"
                    if item.oem_part:
                        part_info = f"{item.oem_part.name} ({item.oem_part.oem_num})"
                    elif item.analogue_part:
                        part_info = f"{item.analogue_part.name} ({item.analogue_part.analogue_num})"

                    items_list.append(
                        html.Div(f" {part_info} - {item.quantity} шт.", style={'marginBottom': '6px'})
                    )
            else:
                items_list.append(html.Div("Пустой заказ", style={'color': '#a0aec0'}))

            # Безопасное форматирование даты
            created_date = order.created_at.strftime('%Y-%m-%d %H:%M') if order.created_at else '-'

            stmt = (
                select(Users)
                .where(Users.user_id == order.user_id)
            )

            user = db.scalar(stmt)

            firstname = user.firstname if user else ''
            lastname = user.lastname if user else ''
            patronymic = user.patronymic if user else ''

            rows.append(
                html.Tr(
                    [
                        html.Td(
                            order.id, style={'padding': '12px',
                                             'textAlign': 'center',
                                             'fontWeight': 'bold'
                                             }
                            ),
                        html.Td(f"{lastname} {firstname} {patronymic}", style={'padding': '12px'}),
                        html.Td(html.Div(items_list), style={'padding': '12px'}),
                        html.Td(
                            created_date, style={
                                'padding': '12px',
                                'whiteSpace': 'nowrap',
                                'textAlign': 'center'
                            }
                            ),
                        html.Td(
                            f'{order.status}', style={
                                'padding': '12px',
                                'whiteSpace': 'nowrap',
                                'textAlign': 'center'
                            }
                            ),
                        html.Td(
                            html.Button(
                                "Создать документ",
                                id={'type': 'btn-create-doc', 'index': order.id},
                                className='btn_style',
                                n_clicks=0
                            ),
                            style={'padding': '12px', 'textAlign': 'center'}
                        )
                    ], style={'borderBottom': '1px solid #e2e8f0'}
                )
            )

        table = html.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th(
                                '№', style={'padding': '12px', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}
                            ),
                            html.Th(
                                'Оформитель', style={
                                    'padding': '12px',
                                    'backgroundColor': '#f8f9fa',
                                    'textAlign': 'left'
                                }
                            ),
                            html.Th(
                                'Состав заказа', style={
                                    'padding': '12px',
                                    'backgroundColor': '#f8f9fa',
                                    'textAlign': 'left'
                                }
                            ),
                            html.Th(
                                'Дата формирования',
                                style={'padding': '12px',
                                       'backgroundColor': '#f8f9fa',
                                       'whiteSpace': 'nowrap',
                                       'align': 'center'}
                            ),

                            html.Th(
                                'Статус',
                                style={'padding': '12px', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}
                            ),

                            html.Th(
                                'Действие',
                                style={'padding': '12px', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}
                            )
                        ]
                    )
                ),
                html.Tbody(rows)
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'fontFamily': 'Arial, sans-serif',
                'fontSize': '14px'
            }
        )

        return table

    except Exception as e:
        return html.Div(f"Ошибка загрузки!", style={'color': '#e53e3e', 'padding': '20px'})