from .layout import Layout
from dash import Output, Input, callback, html, callback_context, ALL, no_update, ctx, dcc
import dash
from .order_services import render_all, render_by_users, render_filtered_table
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.models import Orders
from app.db import get_db


layout = Layout()

# переключатель
@callback(
    Output('data-store', 'data'),
    Output('all-type', 'data-state'),
    Output('by-user-type', 'data-state'),
    Input('by-user-type', 'n_clicks'),
    Input('all-type', 'n_clicks'),
    prevent_initial_call=True
)
def switch(n1, n2):
    triggered = ctx.triggered_id
    if triggered == 'all-type':
        return 'all-type', 'active', 'inactive'
    return 'by-user-type', 'inactive', 'active'

#модуль данных
@callback(
    Output('order-table', 'children'),
    Input('data-store', 'data')
)
def render_data(active_tab):

    if active_tab == 'all-type':
        return render_all()
    return render_by_users()

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

@callback(
    Output("download-pdf", "data"),
    Input({'type': 'btn-create-doc', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def trigger_pdf_download(n_clicks_list):
    # Guard clause: если ни одна кнопка не нажата (все None или 0) → ничего не делаем
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

            db.query(Orders).filter_by(id=order_id).update({"status": "В работе"})
            db.commit()

            return dcc.send_bytes(pdf_buffer.getvalue(), filename=f"Zakaz_Naryad_{order_id}.pdf")

    return no_update


@callback(
    Output("filtered-table", "children"),
    Input("input-order", "value")
)
def filtered_table(filter):
    return render_filtered_table(filter)