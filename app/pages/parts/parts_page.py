import dash
from dash import html, dcc, callback, Input, Output, ctx, ALL, no_update, State
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
                className="card-partq",
                children=[
                    html.Img(src=p["img"], className="card-img"),
                    html.Div(f"{p['code']} {p['article']}", className="meta"),
                    html.Div(p["name"], className="title"),
                    html.Button(
                        'Заказать',
                        id={'type': 'order-btn', 'part_id': p['id'], 'part_type': p['type']},
                        className="order-button"
                    )
                ]
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
            parts = db.query(OEMParts).order_by(func.random()).limit(6).all()
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

        parts = db.query(OEMParts).order_by(func.random()).limit(6).all()
        return render_cards(format_for_cards(parts, 'oem'))
    finally:
        db.close()

# @callback(
#     Output("point-modal1", "is_open"),       # <-- ID как в layout (без 1)
#     Output("modal-content1", "children"),   # <-- ID как в layout (с 1)
#     Input({"type": "order-btn", "part_id": ALL, "part_type": ALL}, "n_clicks"),
#     Input({"type": "point-btn", "index": ALL}, "n_clicks"),  # <-- Добавили старый инпут
#     Input("close-modal-btn1", "n_clicks"),
#     State("point-modal1", "is_open"),
#     prevent_initial_call=True
# )
# def toggle_modal(order_clicks, point_clicks, close_clicks, is_open):
#     triggered = ctx.triggered_id
#
#     # 1. Закрытие модалки
#     if triggered == "close-modal-btn1":
#         return False, no_update
#
#     # 2. Обработка клика на кнопку "Заказать"
#     if isinstance(triggered, dict) and triggered.get('type') == 'order-btn':
#         if not order_clicks or all(click is None or click == 0 for click in order_clicks):
#             return no_update, no_update
#
#         part_id = triggered['part_id']
#         part_type = triggered['part_type']
#
#         # Проверка авторизации
#         token = request.cookies.get('auth_token')
#         if not token:
#             modal_content = html.Div([
#                 html.H3("⚠️ Требуется авторизация", style={'color': '#dc3545', 'marginBottom': '20px'}),
#                 html.P("Необходимо войти в аккаунт.", style={'fontSize': '16px'}),
#                 html.A("Войти", href="/signin", style={'backgroundColor': '#8B0000', 'color': 'white', 'padding': '10px 20px', 'textDecoration': 'none', 'borderRadius': '6px', 'display': 'inline-block', 'marginTop': '15px'})
#             ])
#             return True, modal_content
#
#         try:
#             payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
#             user_id = payload.get("user_id")
#             if not user_id:
#                 return True, html.Div(html.H3("️ Сессия невалидна", style={'color': '#dc3545'}))
#         except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
#             return True, html.Div(html.H3("⏰ Сессия истекла или невалидна", style={'color': '#dc3545'}))
#
#         # Создание заказа
#         db = get_db()
#         try:
#             if part_type == 'oem':
#                 part_name = db.query(OEMParts).filter(OEMParts.id == part_id).first().name
#             else:
#                 part_name = db.query(AnalogueParts).filter(AnalogueParts.id == part_id).first().name
#
#             make_order(db=db, user_id=user_id, part_id=part_id, is_oem=(part_type == 'oem'))
#             modal_content = html.Div([
#                 html.H3("✅ Добавлено!", style={'color': '#28a745', 'marginBottom': '20px', 'align': 'center', 'textAlign': 'center'}),
#                 html.P(f"Деталь", style={'fontSize': '16px', 'textAlign': 'center'}),
#                 html.P(f"{part_name}", style={'fontSize': '16px', 'fontWeight': 'bold', 'textAlign': 'center'}),
#                 html.P("добавлена в заказ!", style={'fontSize': '16px', 'textAlign': 'center'})
#             ])
#             return True, modal_content
#         except Exception as e:
#             db.rollback()
#             return True, html.Div(html.H3(f"❌ Ошибка: {e}", style={'color': '#dc3545'}))
#         finally:
#             db.close()
#
#     # 3. Обработка клика по точке на изображении (ваша старая логика)
#     if isinstance(triggered, dict) and triggered.get('type') == 'point-btn':
#         if not point_clicks or all(click is None or click == 0 for click in point_clicks):
#             return no_update, no_update
#
#         part_id = triggered['index']
#         db = get_db()
#         try:
#             point_data = db.query(OEMParts).filter(OEMParts.id == part_id).first()
#             if not point_data:
#                 return True, html.Div("Деталь не найдена", style={'color': 'red'})
#
#             extracted_point_id = None
#             if point_data.img_coordinates:
#                 try:
#                     coords_list = json.loads(point_data.img_coordinates)
#                     if isinstance(coords_list, list) and len(coords_list) > 0:
#                         extracted_point_id = coords_list[0].get('id')
#                 except (json.JSONDecodeError, TypeError):
#                     pass
#
#             modal_content = html.Div([
#                 html.H3(f"Деталь {extracted_point_id}", style={'marginBottom': '20px', 'color': '#2d3748', 'fontSize': '24px', 'fontWeight': '600'}),
#                 html.Div([
#                     html.H5("Название:", style={'color': '#4a5568', 'marginBottom': '10px', 'fontSize': '16px', 'fontWeight': '600'}),
#                     html.P(point_data.name, style={'color': '#718096', 'fontSize': '15px', 'lineHeight': '1.6', 'padding': '15px', 'backgroundColor': '#f7fafc', 'borderRadius': '8px', 'borderLeft': '4px solid #4299e1'})
#                 ], style={'marginBottom': '25px'}),
#                 html.Div([
#                     html.H5("OEM номер:", style={'color': '#4a5568', 'marginBottom': '10px', 'fontSize': '16px', 'fontWeight': '600'}),
#                     html.P(dcc.Link(point_data.oem_num, href=f"/original_catalogs/analogs/{point_data.id}"), style={'color': '#2d3748', 'fontSize': '18px', 'fontWeight': '500', 'fontFamily': 'monospace', 'padding': '15px', 'backgroundColor': '#edf2f7', 'borderRadius': '8px', 'textAlign': 'center'})
#                 ])
#             ])
#             return True, modal_content
#         finally:
#             db.close()
#
#     return no_update, no_update
@callback(
    Output("point-modal1", "is_open"),
    Output("modal-content1", "children"),
    Input({"type": "order-btn", "part_id": ALL, "part_type": ALL}, "n_clicks"),
    Input({"type": "point-btn", "index": ALL}, "n_clicks"),
    Input("close-modal-btn1", "n_clicks"),
    State("point-modal1", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(order_clicks, point_clicks, close_clicks, is_open):
    triggered = ctx.triggered_id

    # Закрытие модалки
    if triggered == "close-modal-btn1":
        return False, no_update

    # Обработка клика на кнопку "Заказать"
    if isinstance(triggered, dict) and triggered.get('type') == 'order-btn':
        if not order_clicks or all(click is None or click == 0 for click in order_clicks):
            return no_update, no_update

        part_id = triggered['part_id']
        part_type = triggered['part_type']

        # Проверка авторизации
        token = request.cookies.get('auth_token')
        if not token:
            modal_content = html.Div(
                [
                    html.H3("⚠️ Требуется авторизация", style={'color': '#dc3545', 'marginBottom': '20px'}),
                    html.P("Необходимо войти в аккаунт.", style={'fontSize': '16px'}),
                    html.A(
                        "Войти", href="/signin",
                        style={'backgroundColor': '#8B0000', 'color': 'white', 'padding': '10px 20px',
                               'textDecoration': 'none', 'borderRadius': '6px', 'display': 'inline-block',
                               'marginTop': '15px'}
                        )
                ]
            )
            return True, modal_content

        try:
            payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return True, html.Div(html.H3("️ Сессия невалидна", style={'color': '#dc3545'}))
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return True, html.Div(html.H3("⏰ Сессия истекла или невалидна", style={'color': '#dc3545'}))

        # Создание заказа
        db = get_db()
        try:
            # Получаем название детали ДО создания заказа (чтобы не зависеть от коммита)
            Model = OEMParts if part_type == 'oem' else AnalogueParts
            part = db.query(Model).filter_by(id=part_id).first()
            part_name = part.name if part else "Неизвестная деталь"

            # Вызываем make_order (без commit внутри)
            make_order(db=db, user_id=user_id, part_id=part_id, is_oem=(part_type == 'oem'))

            # КОММИТИМ ЗДЕСЬ, ПОСЛЕ УСПЕШНОГО ВЫПОЛНЕНИЯ ВСЕЙ ЛОГИКИ
            db.commit()

            modal_content = html.Div(
                [
                    html.H3("✅ Добавлено!", style={'color': '#28a745', 'marginBottom': '20px', 'textAlign': 'center'}),
                    html.P("Деталь", style={'fontSize': '16px', 'textAlign': 'center'}),
                    html.P(part_name, style={'fontSize': '16px', 'fontWeight': 'bold', 'textAlign': 'center'}),
                    html.P("добавлена в заказ!", style={'fontSize': '16px', 'textAlign': 'center'})
                ]
            )
            return True, modal_content

        except Exception as e:
            # ОТКАТЫВАЕМ ТОЛЬКО ЕСЛИ ЧТО-ТО ПОШЛО НЕ ТАК
            db.rollback()
            return True, html.Div(html.H3(f"❌ Ошибка: {e}", style={'color': '#dc3545', 'textAlign': 'center'}))
        finally:
            db.close()

    # Обработка клика по точке на изображении
    if isinstance(triggered, dict) and triggered.get('type') == 'point-btn':
        if not point_clicks or all(click is None or click == 0 for click in point_clicks):
            return no_update, no_update

        part_id = triggered['index']
        db = get_db()
        try:
            point_data = db.query(OEMParts).filter(OEMParts.id == part_id).first()
            if not point_data:
                return True, html.Div("Деталь не найдена", style={'color': 'red'})

            extracted_point_id = None
            if point_data.img_coordinates:
                try:
                    coords_list = json.loads(point_data.img_coordinates)
                    if isinstance(coords_list, list) and len(coords_list) > 0:
                        extracted_point_id = coords_list[0].get('id')
                except (json.JSONDecodeError, TypeError):
                    pass

            modal_content = html.Div(
                [
                    html.H3(
                        f"Деталь {extracted_point_id}",
                        style={'marginBottom': '20px', 'color': '#2d3748', 'fontSize': '24px', 'fontWeight': '600'}
                        ),
                    html.Div(
                        [
                            html.H5(
                                "Название:", style={'color': '#4a5568', 'marginBottom': '10px', 'fontSize': '16px',
                                                    'fontWeight': '600'}
                                ),
                            html.P(
                                point_data.name, style={'color': '#718096', 'fontSize': '15px', 'lineHeight': '1.6',
                                                        'padding': '15px', 'backgroundColor': '#f7fafc',
                                                        'borderRadius': '8px', 'borderLeft': '4px solid #4299e1'}
                                )
                        ], style={'marginBottom': '25px'}
                    ),
                    html.Div(
                        [
                            html.H5(
                                "OEM номер:", style={'color': '#4a5568', 'marginBottom': '10px', 'fontSize': '16px',
                                                     'fontWeight': '600'}
                                ),
                            html.P(
                                dcc.Link(point_data.oem_num, href=f"/original_catalogs/analogs/{point_data.id}"),
                                style={'color': '#2d3748', 'fontSize': '18px', 'fontWeight': '500',
                                       'fontFamily': 'monospace', 'padding': '15px', 'backgroundColor': '#edf2f7',
                                       'borderRadius': '8px', 'textAlign': 'center'}
                                )
                        ]
                    )
                ]
            )
            return True, modal_content
        finally:
            db.close()

    return no_update, no_update