from .layout import Layout
from dash import Output, Input, callback, html, callback_context, ALL, no_update, ctx, dcc
import dash
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.models import Orders, OrderItems, OEMParts, AnalogueParts, Users
from app.db import get_db


layout = Layout()


@callback(
    Output("order-table", "children"),
    Input("data-refresh-interval", "data"),
    prevent_initial_call=False
)
def render_table(data):
    db = get_db()
    try:
        # Загружаем заказы сразу с элементами и привязанными деталями (без N+1 запросов)
        orders = db.query(Orders).options(
            joinedload(Orders.items).joinedload(OrderItems.oem_part),
            joinedload(Orders.items).joinedload(OrderItems.analogue_part)
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
            lastname =  user.lastname if user else ''
            patronymic = user.patronymic if user else ''

            rows.append(
                html.Tr(
                    [
                        html.Td(order.id, style={'padding': '12px',
                                                'textAlign': 'center',
                                                 'fontWeight': 'bold'
                                                 }),
                        html.Td(f"{lastname} {firstname} {patronymic}", style={'padding': '12px'}),
                        html.Td(html.Div(items_list), style={'padding': '12px'}),
                        html.Td(created_date, style={
                                                        'padding': '12px',
                                                        'whiteSpace': 'nowrap',
                                                        'textAlign': 'center'
                                                    }),
                        html.Td(f'{order.status}', style={
                                                            'padding': '12px',
                                                            'whiteSpace': 'nowrap',
                                                            'textAlign': 'center'
                                                            }),
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
                            html.Th('Оформитель', style={
                                                            'padding': '12px',
                                                            'backgroundColor': '#f8f9fa',
                                                            'textAlign': 'left'
                                                        }),
                            html.Th('Состав заказа', style={
                                                                'padding': '12px',
                                                                'backgroundColor': '#f8f9fa',
                                                                'textAlign': 'left'
                                                            }),
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
        return html.Div(f"Ошибка загрузки: {str(e)}", style={'color': '#e53e3e', 'padding': '20px'})


@callback(
    Output("dummy-output", "children"),
    Input({'type': 'btn-create-doc', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def handle_create_document(n_clicks_list):
    if not dash.callback_context.triggered:
        return no_update

    triggered_id = ctx.triggered_id
    if triggered_id and triggered_id.get('type') == 'btn-create-doc':
        order_id = triggered_id['index']
        print(f"️ Генерация PDF для заказа №{order_id}")

        # Возвращаем скрипт для открытия ссылки в новой вкладке (стандартный паттерн для скачивания в Dash)
        return dash.no_update  # В реальном проекте лучше использовать dcc.Download, но redirect проще

    return no_update


from dash import callback, Output, Input, ALL, no_update, ctx, dcc
from app.models import Orders
from app.db import get_db

@callback(
    Output("download-pdf", "data"),
    Input({'type': 'btn-create-doc', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def trigger_pdf_download(n_clicks_list):
    # 🛡️ Guard clause: если ни одна кнопка не нажата (все None или 0) → ничего не делаем
    if not n_clicks_list or all(nc is None or nc == 0 for nc in n_clicks_list):
        return no_update

    triggered = ctx.triggered_id
    if triggered and triggered.get('type') == 'btn-create-doc':
        order_id = triggered['index']

        db = get_db()
        order = db.query(Orders).filter_by(id=order_id).first()

        if order:
            from app.pages.admin.create_doc.create_order_doc import generate_order_pdf
            pdf_buffer = generate_order_pdf(order, db)
            return dcc.send_bytes(pdf_buffer.getvalue(), filename=f"Zakaz_Naryad_{order_id}.pdf")

    return no_update