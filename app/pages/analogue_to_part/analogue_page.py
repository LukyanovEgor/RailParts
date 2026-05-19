from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL
from app.pages.header import Header
from app.models import OEMParts, AnalogueParts
from app.db import get_db
import json
import jwt
from flask import request
from app.order_services.make_order import make_order


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


@callback(
    Output('order-notification-analogue', 'children'),
    Input({'type': 'order-btn', 'part_id': ALL, 'part_type': ALL}, 'n_clicks'),
    prevent_initial_call=True
)
def handle_analogue_order(n_clicks_list):
    if not any(n_clicks_list):
        return no_update

    triggered = ctx.triggered
    if not triggered:
        return no_update

    # 1️⃣ Парсим ID нажатой кнопки
    prop_id = triggered[0]['prop_id']
    id_data = json.loads(prop_id.split('.n_clicks')[0])
    part_id = id_data['part_id']
    part_type = id_data['part_type']

    # 2️⃣ Проверка авторизации (как в прошлом примере)
    token = request.cookies.get('auth_token')
    if not token:
        return html.Div(
            "🔐 Войдите в аккаунт, чтобы оформить заказ",
            style={'color': '#dc3545', 'padding': '10px', 'backgroundColor': '#fff3cd', 'borderRadius': '4px'}
            )

    try:
        # Замените на ваш реальный SECRET_KEY
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
        user_id = payload.get("user_id")
        if not user_id:
            return html.Div("️ Сессия невалидна", style={'color': '#dc3545', 'padding': '10px'})
    except jwt.ExpiredSignatureError:
        return html.Div("⏳ Срок действия сессии истёк", style={'color': '#dc3545', 'padding': '10px'})
    except jwt.InvalidTokenError:
        return html.Div("🔒 Ошибка токена", style={'color': '#dc3545', 'padding': '10px'})

    # 3️⃣ Вызов вашей функции make_order
    try:

        make_order(
            db=get_db(),
            user_id=user_id,
            part_id=part_id,
            is_oem=part_type == 'oem'
        )

        part_name = "Оригинал" if part_type == "oem" else "Аналог"
        return html.Div(
            f"✅ {part_name} #{part_id} успешно добавлен в заказ!",
            style={'color': '#155724', 'padding': '10px', 'backgroundColor': '#d4edda', 'borderRadius': '4px',
                   'fontWeight': '500'}
            )
    except Exception as e:
        return html.Div(
            f"❌ Ошибка при оформлении: {str(e)}",
            style={'color': '#721c24', 'padding': '10px', 'backgroundColor': '#f8d7da', 'borderRadius': '4px'}
            )