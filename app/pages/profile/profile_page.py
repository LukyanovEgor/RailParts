from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL
from datetime import datetime
from app.pages.header import Header
from sqlalchemy.orm import joinedload
from app.models import Users, Orders, OrderItems
from app.db import get_db
import os, base64


def profile_layout(user_id=None):

    db = get_db()

    user_data = db.query(Users).filter(Users.user_id == user_id).first()

    if user_data is None:

        return html.Div('Пользователь не найден')

    style_icon = {'width': '280px', 'height': '280px', 'borderRadius': '4px'}
    icon = user_data.icon

    if icon is None:
        icon = '/assets/no_icon_user.png'
        style_icon = {'width': '240px', 'height': '240px', 'borderRadius': '4px'}


    user = {
        "firstname": user_data.firstname,
        "lastname": user_data.lastname,
        "patronymic": user_data.patronymic,
        "email": user_data.email,
        "phone": user_data.phone,
        "age": user_data.age,
        "is_admin": user_data.is_admin,

        # Форматируем дату в российский формат ДД.ММ.ГГГГ
        "reg_date": (
            user_data.reg_date.strftime('%d.%m.%Y')
            if isinstance(user_data.reg_date, datetime)
            else (user_data.reg_date.split('T')[0] if user_data.reg_date else 'Нет данных')
        ),

        "orders_count": 12
    }

    full_name = f"{user['lastname']} {user['firstname']}"
    if user['patronymic']:
        full_name += f" {user['patronymic']}"

    try:

        order_data = db.query(Orders).options(
            joinedload(Orders.items).joinedload(OrderItems.oem_part),
            joinedload(Orders.items).joinedload(OrderItems.analogue_part)
        ).filter(
            Orders.user_id == user_id
        ).order_by(
            Orders.created_at.desc()
        ).limit(3).all()


        if not order_data:

            orders = [html.Tr(
                "Заказы пока не оформлены",
                style={'textAlign': 'center', 'padding': '40px', 'color': '#718096'}
            )]
        else:
            orders = []
            for order in order_data:
                created_date = order.created_at.strftime('%Y-%m-%d %H:%M') if order.created_at else '-'

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

                orders.append(
                    html.Tr(
                        [
                            html.Td(
                                f"{order.id}",
                                style={'border': '1px solid #eee',
                                       'padding': '10px'}
                            ),
                            html.Td(html.Div(items_list), style={'border': '1px solid #eee',
                                                          'padding': '10px',
                                                          'fontSize': '10px'
                                                          }),

                            html.Td(
                                f"{created_date}",
                                style={'border': '1px solid #eee',
                                       'padding': '10px'}
                            ),
                            html.Td(
                                f"{order.status}", style={'border': '1px solid #eee',
                                                          'padding': '10px',
                                                          'color': '#28a745'}
                            ),
                        ]
                    )
                )

    except Exception as e:

        print(e)
        orders = [html.Tr(
            "Ошибка загрузки данных",
            style={'textAlign': 'center', 'padding': '40px', 'color': '#718096'}
        )]

    return html.Div(
        [
            dcc.Store(id='current-user-id-store', data=user_id),

            Header()(),

            html.Div(
                className="profile-wrapper",
                style={
                    'maxWidth': '1100px',
                    'margin': '30px auto',
                    'padding': '0 20px',
                    'fontFamily': 'system-ui, -apple-system, sans-serif',
                    'color': '#333'
                },
                children=[
                    html.H2("Личный кабинет", style={'marginBottom': '25px', 'fontWeight': '600'}),

                    html.Div(
                        style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap'},
                        children=[
                            # ЛЕВАЯ КОЛОНКА: Аватар + роль
                            html.Div(
                                style={
                                    'flex': '1',
                                    'minWidth': '280px',
                                    'backgroundColor': '#fff',
                                    'padding': '25px',
                                    'borderRadius': '12px',
                                    'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'alignItems': 'center',
                                    'textAlign': 'center'
                                },
                                children=[
                                    html.Div(
                                        html.Img(
                                            id='user-avatar-img',
                                            src=icon,
                                            style=style_icon
                                        ),
                                        style={
                                            'width': '280px', 'height': '280px',
                                            'backgroundColor': '#cccccc',
                                            'display': 'flex',
                                            'alignItems': 'center',
                                            'justifyContent': 'center',
                                            'borderRadius': '8px',
                                            'marginBottom': '35px',  # Отступ до имени
                                            'marginTop': '25px'
                                        }
                                    ),
                                    html.H3(full_name, style={'margin': '0 0 5px', 'fontSize': '1.2rem'}),
                                    html.Span(
                                        "Администратор" if user['is_admin'] else "Пользователь",
                                        style={
                                            'display': 'inline-block',
                                            'padding': '4px 12px',
                                            'borderRadius': '20px',
                                            'fontSize': '0.85rem',
                                            'fontWeight': '500',
                                            'color': '#fff',
                                            'backgroundColor': '#28a745' if user['is_admin'] else '#6c757d',
                                            'marginBottom': '20px',
                                            'marginTop': '12px'
                                        }
                                    ),

                                    dcc.Upload(
                                        id='upload-avatar-btn',
                                        children=html.Button("Загрузить фото", className='btn_style'),
                                        style={'width': '100%', 'border': 'none', 'background': 'transparent',
                                               'padding': 0},
                                        multiple=False
                                    )
                                ]
                            ),
                            # ПРАВАЯ КОЛОНКА: Данные + Заказы
                            html.Div(
                                style={
                                    'flex': '2',
                                    'minWidth': '320px',
                                    'display': 'flex',
                                    'flexDirection': 'column',
                                    'gap': '20px'
                                },
                                children=[
                                    # Карточка с личными данными
                                    html.Div(
                                        style={
                                            'backgroundColor': '#fff',
                                            'padding': '25px',
                                            'borderRadius': '12px',
                                            'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'
                                        },
                                        children=[
                                            html.H4(
                                                "Контактные данные", style={'marginTop': '0', 'marginBottom': '15px',
                                                                            'borderBottom': '2px solid #f0f2f5',
                                                                            'paddingBottom': '10px'}
                                                ),

                                            html.Div(
                                                [
                                                    html.P(
                                                        [html.B(
                                                            "Email: ",
                                                            style={'minWidth': '160px', 'display': 'inline-block'}
                                                            ), user['email']],
                                                        style={'margin': '0'}  # Убираем лишние отступы у параграфа
                                                    ),
                                                    html.P(
                                                        [html.B(
                                                            "Телефон: ",
                                                            style={'minWidth': '160px', 'display': 'inline-block'}
                                                            ), user['phone']],
                                                        style={'margin': '0'}
                                                    ),
                                                    html.P(
                                                        [html.B(
                                                            "Возраст: ",
                                                            style={'minWidth': '160px', 'display': 'inline-block'}
                                                            ), str(user['age'])],
                                                        style={'margin': '0'}
                                                    ),
                                                    html.P(
                                                        [html.B(
                                                            "Дата регистрации: ",
                                                            style={'minWidth': '160px', 'display': 'inline-block'}
                                                            ), user['reg_date']],
                                                        style={'margin': '0'}
                                                    ),
                                                ],
                                                style={'fontSize': '0.95rem', 'lineHeight': '1.8'}
                                            )
                                        ]
                                    ),

                                    # Карточка с заказами (relationship)
                                    html.Div(
                                        style={
                                            'backgroundColor': '#fff',
                                            'padding': '25px',
                                            'borderRadius': '12px',
                                            'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'
                                        },
                                        children=[
                                            html.H4(
                                                "История заказов", style={'marginTop': '0', 'marginBottom': '15px',
                                                                          'borderBottom': '2px solid #f0f2f5',
                                                                          'paddingBottom': '10px'}
                                                ),
                                            html.P(
                                                f"Всего заказов: {user['orders_count']}",
                                                style={'fontSize': '0.9rem', 'color': '#666', 'marginBottom': '15px'}
                                                ),

                                            html.Table(
                                                style={'width': '100%', 'borderCollapse': 'collapse',
                                                       'fontSize': '0.9rem'},
                                                children=[
                                                    html.Thead(
                                                        html.Tr(
                                                            [
                                                                html.Th(
                                                                    "№", style={'border': '1px solid #eee',
                                                                                'padding': '10px', 'textAlign': 'left',
                                                                                'backgroundColor': '#f8f9fa'}
                                                                    ),
                                                                html.Th(
                                                                    "Состав заказа", style={'border': '1px solid #eee',
                                                                                    'padding': '10px',
                                                                                    'textAlign': 'left',
                                                                                    'backgroundColor': '#f8f9fa'}
                                                                ),
                                                                html.Th(
                                                                    "Дата", style={'border': '1px solid #eee',
                                                                                   'padding': '10px',
                                                                                   'textAlign': 'left',
                                                                                   'backgroundColor': '#f8f9fa'}
                                                                    ),
                                                                html.Th(
                                                                    "Статус", style={'border': '1px solid #eee',
                                                                                     'padding': '10px',
                                                                                     'textAlign': 'left',
                                                                                     'backgroundColor': '#f8f9fa'}
                                                                    ),
                                                            ]
                                                        )
                                                    ),
                                                    html.Tbody(orders)
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


UPLOAD_DIR = os.path.join('test_images', 'user_icons')
os.makedirs(UPLOAD_DIR, exist_ok=True)


@callback(
    Output('user-avatar-img', 'src'),
    Input('upload-avatar-btn', 'contents'),
    State('upload-avatar-btn', 'filename'),
    State('current-user-id-store', 'data'),
    prevent_initial_call=True
)
def handle_avatar_upload(contents, filename, user_id):


    if contents is None or user_id is None:
        return no_update

    # Разделяем заголовок и base64-данные
    content_type, content_string = contents.split(',')

    # Проверяем, что это изображение
    if not content_type.startswith('data:image/'):

        return no_update

    # Декодируем
    decoded = base64.b64decode(content_string)

    # Определяем расширение и формируем имя файла
    ext = filename.split('.')[-1].lower() if '.' in filename else 'png'
    if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        ext = 'png'

    # Перезаписываем старый аватар пользователя

    new_filename = f"user_{user_id}_avatar.{ext}"
    filepath = os.path.join(UPLOAD_DIR, new_filename)

    print(filepath)

    # Сохраняем на диск
    with open(filepath, 'wb') as f:
        f.write(decoded)

    with get_db() as db:
        user = db.query(Users).filter(Users.user_id == user_id).first()
        if user:
            user.icon = f"http://127.0.0.1:8050/test_images/user_icons/{new_filename}"
            db.commit()
            return user.icon
        return no_update