from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL
from app.pages.header import Header
from app.models import OEMParts, AnalogueParts
from app.db import get_db
import json
import jwt
from flask import request
from app.order_services.make_order import make_order
import dash_bootstrap_components as dbc


def analogue_parts_layout(oem_part_id=None):
    db = get_db()

    # Получаем OEM запчасть
    oem_part = db.query(OEMParts).filter(OEMParts.id == oem_part_id).first()

    # Получаем аналоги
    analogue_parts = db.query(AnalogueParts).filter(
        AnalogueParts.oem_id == oem_part_id
    ).all() if oem_part_id else []

    return html.Div(
        [
            html.Div(Header()(), className="card-header"),

            # Запрошенный товар
            html.Div(
                [
                    html.H3('Запрошенный товар', style={'marginBottom': '20px', 'color': '#212529'}),

                    # Карточка OEM детали
                    html.Div(
                        [
                            # Изображение
                            html.Div(
                                [
                                    html.Img(
                                        src=oem_part.img_url if oem_part and oem_part.img_url
                                                             else "/assets/no_icon_part.png",
                                        style={'width': '120px', 'height': '120px', 'objectFit': 'contain'}
                                    )
                                ], style={'marginRight': '20px'}
                            ),

                            # Информация о детали
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Span(
                                                oem_part.oem_num if oem_part else '',
                                                style={'color': '#007bff', 'marginRight': '10px', 'fontWeight': '500'}
                                                ),
                                            html.Span(
                                                f'Код: {oem_part.id}' if oem_part else '',
                                                style={'color': '#6c757d', 'fontSize': '13px'}
                                                ),
                                        ], style={'marginBottom': '8px'}
                                    ),

                                    html.Div(
                                        [
                                            html.A(
                                                oem_part.name if oem_part else '',
                                                href=f'/original_catalogs/{oem_part_id}',
                                                style={'color': '#212529', 'fontWeight': '600',
                                                       'textDecoration': 'none', 'fontSize': '16px'}
                                            )
                                        ], style={'marginBottom': '8px'}
                                    ),

                                    html.Div(
                                        [
                                            html.I(className='bi bi-bookmark', style={'color': '#6c757d', 'cursor': 'pointer'})
                                        ]
                                    )
                                ], style={'flex': 1}
                            ),

                            # кнопка (справа)
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Button(
                                                'Заказ',
                                                id={'type': 'order-btn', 'part_id': oem_part_id, 'part_type': 'oem'},
                                                className="btn_style"
                                            )
                                        ]
                                    )
                                ], style={'display': 'flex', 'alignItems': 'center', 'marginLeft': '20px'}
                            )
                        ], style={
                            'display': 'flex',
                            'padding': '20px',
                            'borderBottom': '1px solid #dee2e6',
                            'alignItems': 'center'
                        }
                    )
                ], style={'marginBottom': '40px'}
            ),

            # Аналоги
            html.Div(
                [
                    html.H3('Аналоги', style={'marginBottom': '20px', 'color': '#8B0000'}),

                    html.Div(
                        [
                            create_analogue_card(part) for part in analogue_parts
                        ]
                    ),

                    html.Div(id='order-notification-analogue', style={'marginBottom': '15px'}),

                    dbc.Modal(
                        [
                            dbc.ModalBody(
                                id="modal-content2",
                                style={
                                    'minHeight': '300px',
                                    'padding': '30px'
                                }
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Закрыть",
                                    id="close-modal-btn2",
                                    className="ms-auto",
                                    color="secondary"
                                )
                            )
                        ],
                        id="point-modal2",
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
            ),
        ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'}
    )


def create_analogue_card(part):
    """Создаёт карточку аналоговой запчасти"""

    return html.Div(
        [
            html.Div(
                [
                    # Иконка "аналог"
                    html.Div(
                        [
                            html.I(
                                className='bi bi-arrow-left-right',
                                style={'color': '#28a745', 'fontSize': '16px'}
                                )
                        ], style={'marginRight': '15px', 'marginTop': '10px'}
                    ),

                    # Изображение
                    html.Div(
                        [
                            html.Img(
                                src=part.img_url if part.img_url else "/assets/no_icon_part.png",
                                style={'width': '120px', 'height': '120px', 'objectFit': 'contain'}
                            )
                        ], style={'marginRight': '20px'}
                    ),

                    # Информация о детали
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Span(
                                        part.manufacturer,
                                        style={'color': '#007bff', 'fontWeight': '500', 'marginRight': '10px'}
                                        ),
                                    html.Span(
                                        part.analogue_num,
                                        style={'color': '#007bff', 'marginRight': '10px'}
                                        ),
                                    html.Span(
                                        f'Код: {part.id}',
                                        style={'color': '#6c757d', 'fontSize': '13px'}
                                        ),
                                ], style={'marginBottom': '8px'}
                            ),

                            html.Div(
                                [
                                    html.A(
                                        part.name,
                                        href=f'/analogue_parts/{part.id}',
                                        style={'color': '#212529', 'fontWeight': '600', 'textDecoration': 'none', 'fontSize': '16px'}
                                    )
                                ], style={'marginBottom': '8px'}
                            ),

                            html.Div(
                                [
                                    html.I(className='bi bi-bookmark', style={'color': '#6c757d', 'cursor': 'pointer'})
                                ]
                            )
                        ], style={'flex': 1}
                    ),

                    # кнопка (справа)
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Button(
                                        'Заказ',
                                        id={'type': 'order-btn', 'part_id': part.id, 'part_type': 'analogue'},
                                        # 👈 добавлено
                                        className="btn_style"
                                    )
                                ]
                            )
                        ], style={'display': 'flex', 'alignItems': 'center', 'marginLeft': '20px'}
                    )
                ], style={
                    'display': 'flex',
                    'padding': '20px',
                    'borderBottom': '1px solid #dee2e6',
                    'alignItems': 'center'
                }
            )
        ], style={'marginBottom': '10px'}
    )

#
# @callback(
#     Output('order-notification-analogue', 'children'),
#     Input({'type': 'order-btn', 'part_id': ALL, 'part_type': ALL}, 'n_clicks'),
#     prevent_initial_call=True
# )
# def handle_analogue_order(n_clicks_list):
#     if not any(n_clicks_list):
#         return no_update
#
#     triggered = ctx.triggered
#     if not triggered:
#         return no_update
#
#     # 1️⃣ Парсим ID нажатой кнопки
#     prop_id = triggered[0]['prop_id']
#     id_data = json.loads(prop_id.split('.n_clicks')[0])
#     part_id = id_data['part_id']
#     part_type = id_data['part_type']
#
#     # 2️⃣ Проверка авторизации (как в прошлом примере)
#     token = request.cookies.get('auth_token')
#     if not token:
#         return html.Div(
#             "🔐 Войдите в аккаунт, чтобы оформить заказ",
#             style={'color': '#dc3545', 'padding': '10px', 'backgroundColor': '#fff3cd', 'borderRadius': '4px'}
#             )
#
#     try:
#         # Замените на ваш реальный SECRET_KEY
#         payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
#         user_id = payload.get("user_id")
#         if not user_id:
#             return html.Div("️ Сессия невалидна", style={'color': '#dc3545', 'padding': '10px'})
#     except jwt.ExpiredSignatureError:
#         return html.Div("⏳ Срок действия сессии истёк", style={'color': '#dc3545', 'padding': '10px'})
#     except jwt.InvalidTokenError:
#         return html.Div("🔒 Ошибка токена", style={'color': '#dc3545', 'padding': '10px'})
#
#     # 3️⃣ Вызов вашей функции make_order
#     try:
#
#         make_order(
#             db=get_db(),
#             user_id=user_id,
#             part_id=part_id,
#             is_oem=part_type == 'oem'
#         )
#
#         db = get_db()
#         if part_type == 'oem':
#             part_name = db.query(OEMParts).filter(OEMParts.id == part_id).first().name
#         else:
#             part_name = db.query(AnalogueParts).filter(AnalogueParts.id == part_id).first().name
#
#         return html.Div(
#             f"✅ {part_name} #{part_id} успешно добавлен в заказ!",
#             style={'color': '#155724', 'padding': '10px', 'backgroundColor': '#d4edda', 'borderRadius': '4px',
#                    'fontWeight': '500'}
#             )
#     except Exception as e:
#         return html.Div(
#             f"❌ Ошибка при оформлении: {str(e)}",
#             style={'color': '#721c24', 'padding': '10px', 'backgroundColor': '#f8d7da', 'borderRadius': '4px'}
#             )


@callback(
    Output("point-modal2", "is_open"),
    Output("modal-content2", "children"),
    Input({"type": "order-btn", "part_id": ALL, "part_type": ALL}, "n_clicks"),
    Input("close-modal-btn2", "n_clicks"),
    State("point-modal2", "is_open"),
    prevent_initial_call=True
)
def handle_analogue_order(order_clicks, close_clicks, is_open):
    triggered = ctx.triggered_id

    # Закрытие модалки
    if triggered == "close-modal-btn2":
        return False, no_update

    # Обработка клика на кнопку "Заказ"
    if isinstance(triggered, dict) and triggered.get('type') == 'order-btn':
        if not order_clicks or all(click is None or click == 0 for click in order_clicks):
            return no_update, no_update

        part_id = triggered['part_id']
        part_type = triggered['part_type']

        # Проверка авторизации
        token = request.cookies.get('auth_token')
        if not token:
            modal_content = html.Div([
                html.H3("⚠️ Требуется авторизация", style={'color': '#dc3545', 'marginBottom': '20px', 'textAlign': 'center'}),
                html.P("Необходимо войти в аккаунт для оформления заказа.", style={'fontSize': '16px', 'textAlign': 'center'}),
                html.A(
                    "Войти",
                    href="/signin",
                    style={
                        'backgroundColor': '#8B0000',
                        'color': 'white',
                        'padding': '10px 20px',
                        'textDecoration': 'none',
                        'borderRadius': '6px',
                        'display': 'block',
                        'textAlign': 'center',
                        'marginTop': '15px'
                    }
                )
            ])
            return True, modal_content

        try:
            payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                modal_content = html.Div([
                    html.H3("⚠️ Сессия невалидна", style={'color': '#dc3545', 'marginBottom': '20px', 'textAlign': 'center'}),
                    html.P("Пожалуйста, войдите в аккаунт снова.", style={'fontSize': '16px', 'textAlign': 'center'})
                ])
                return True, modal_content
        except jwt.ExpiredSignatureError:
            modal_content = html.Div([
                html.H3("⏰ Сессия истекла", style={'color': '#dc3545', 'marginBottom': '20px', 'textAlign': 'center'}),
                html.P("Срок действия сессии истёк. Пожалуйста, войдите снова.", style={'fontSize': '16px', 'textAlign': 'center'})
            ])
            return True, modal_content
        except jwt.InvalidTokenError:
            modal_content = html.Div([
                html.H3(" Ошибка токена", style={'color': '#dc3545', 'marginBottom': '20px', 'textAlign': 'center'}),
                html.P("Не удалось проверить токен авторизации.", style={'fontSize': '16px', 'textAlign': 'center'})
            ])
            return True, modal_content

        # Создание заказа
        db = get_db()
        try:
            make_order(
                db=db,
                user_id=user_id,
                part_id=part_id,
                is_oem=(part_type == 'oem')
            )

            db.commit()

            # Получаем название детали
            Model = OEMParts if part_type == 'oem' else AnalogueParts
            part = db.query(Model).filter_by(id=part_id).first()
            part_name = part.name if part else "Неизвестная деталь"

            modal_content = html.Div([
                html.H3("✅ Добавлено!", style={'color': '#28a745', 'marginBottom': '20px', 'textAlign': 'center'}),
                html.P("Деталь", style={'fontSize': '16px', 'textAlign': 'center'}),
                html.P(
                    part_name,
                    style={'fontSize': '18px', 'fontWeight': 'bold', 'textAlign': 'center', 'marginBottom': '10px'}
                ),
                html.P(
                    f"успешно добавлена в заказ!",
                    style={'fontSize': '16px', 'textAlign': 'center'}
                )
            ])
            return True, modal_content

        except Exception as e:
            db.rollback()
            modal_content = html.Div([
                html.H3("❌ Ошибка оформления", style={'color': '#dc3545', 'marginBottom': '20px', 'textAlign': 'center'}),
                html.P(f"Не удалось добавить деталь в заказ: {str(e)}", style={'fontSize': '16px', 'textAlign': 'center'})
            ])
            return True, modal_content
        finally:
            db.close()

    return no_update, no_update