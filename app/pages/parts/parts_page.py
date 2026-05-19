import dash
from dash import html, dcc, callback, Input, Output, ctx, ALL, no_update
from app.models import OEMParts, AnalogueParts
from sqlalchemy import func
from .layout import Layout
from app.db import get_db
from flask import request
import json
import jwt


from app.order_services.make_order import make_order
layout = Layout()


def render_cards(items):
    if not items:
        return html.Div("Товары не найдены", className="empty")

    cards = []
    for p in items:
        cards.append(
            html.Div(
                children=[
                    html.Img(src=p["img"], className="card-img"),
                    html.Div(f"{p['code']} {p['article']}", className="meta"),
                    html.Div(p["name"], className="title"),

                    html.Button(
                        'Заказать',
                        # 👈 Уникальный ID для каждой кнопки
                        id={'type': 'order-btn', 'part_id': p['id'], 'part_type': p['type']},
                        style={
                            'backgroundColor': '#8B0000', 'color': 'white', 'border': 'none',
                            'padding': '10px 20px', 'text-align': 'center', 'text-decoration': 'none',
                            'display': 'inline-block', 'fontSize': '16px', 'cursor': 'pointer',
                            'borderRadius': '5px', 'marginTop': 'auto',  # 👈 ГЛАВНОЕ: прижимает к низу
                            'width': 'calc(100% - 20px)',
                        }
                    )
                ], className="card-part",
                style={"padding": "40px"}
            )
        )
    return cards


def format_for_cards(parts, part_type='oem'):
    """Упрощённая и безопасная версия"""
    return [
        {
            "name": p.name,
            "code": p.oem_num if part_type == 'oem' else p.analogue_num,
            "article": p.oem_num if part_type == 'oem' else p.analogue_num,
            "img": p.img_url or "/assets/no_icon_part.png",
            "id": p.id,
            "type": part_type  # 👈 Явно сохраняем тип
        } for p in parts
    ]


@callback(
    Output("product-grid", "children"),
    Input("search-input", "value"),
    Input({"type": "filter-btn", "index": ALL}, "n_clicks"),
    prevent_initial_call=False
)
def update_view(search_val, n_clicks_list):
    db = get_db()
    triggered = ctx.triggered
    try:
        if not triggered:
            parts = db.query(OEMParts).order_by(func.random()).limit(8).all()
            return render_cards(format_for_cards(parts, 'oem'))

        if search_val and search_val.strip():
            query = search_val.strip()
            oems = db.query(OEMParts).filter(
                (OEMParts.name.ilike(f"%{query}%")) | (OEMParts.oem_num.ilike(f"%{query}%"))
            ).all()
            analogs = db.query(AnalogueParts).filter(
                (AnalogueParts.name.ilike(f"%{query}%")) | (AnalogueParts.analogue_num.ilike(f"%{query}%"))
            ).all()
            # Объединяем, сохраняя типы
            return render_cards(format_for_cards(oems, 'oem') + format_for_cards(analogs, 'analogue'))

        parts = db.query(OEMParts).order_by(func.random()).limit(8).all()
        return render_cards(format_for_cards(parts, 'oem'))
    finally:
        db.close()


@callback(
    Output('order-notification', 'children'),
    Output('url-redirect', 'href'),  # 👈 Вывод для редиректа
    Input({'type': 'order-btn', 'part_id': ALL, 'part_type': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def handle_order_click(n_clicks_list):
    if not any(n_clicks_list):
        return no_update, no_update

    triggered = ctx.triggered
    if not triggered:
        return no_update, no_update

    #  Парсим ID нажатой кнопки
    prop_id = triggered[0]['prop_id']
    id_data = json.loads(prop_id.split('.n_clicks')[0])
    part_id = id_data['part_id']
    part_type = id_data['part_type']

    #  Проверка авторизации
    token = request.cookies.get('auth_token')
    if not token:
        return html.Div("️ Необходимо войти в аккаунт", style={'color': '#dc3545', 'padding': '10px'}), '/signin'

    try:

        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return html.Div("⚠️ Сессия невалидна", style={'color': '#dc3545', 'padding': '10px'}), '/signin'
    except jwt.ExpiredSignatureError:
        return html.Div(" Срок действия сессии истёк", style={'color': '#dc3545', 'padding': '10px'}), '/signin'
    except jwt.InvalidTokenError:
        return html.Div("🔒 Ошибка проверки токена", style={'color': '#dc3545', 'padding': '10px'}), '/signin'

    # 3 Создание заказа (если авторизован)
    db = get_db()
    try:

        make_order(
            db=db,
            user_id=user_id,
            part_id=part_id,
            is_oem=part_type == 'oem'
            )

        return html.Div(f"✅ Деталь #{part_id} добавлена в заказ!", style={'color': '#28a745', 'padding': '10px'}), no_update
    except Exception as e:
        db.rollback()
        return html.Div(f"❌ Ошибка: {e}", style={'color': '#dc3545', 'padding': '10px'}), no_update
    finally:
        db.close()