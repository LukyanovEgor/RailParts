from dash import html, dcc, callback, ctx, no_update, Input, Output, State, ALL
from app.pages.header import Header
from app.models import OEMParts, AnalogueParts
from app.db import get_db


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

                            # Цена и кнопка (справа)
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.Button(
                                                'Заказ',
                                                className="btn_style",
                                                style={
                                                    'backgroundColor': '#007bff',
                                                    'color': 'white',
                                                    'border': 'none',
                                                    'padding': '10px 24px',
                                                    'borderRadius': '6px',
                                                    'cursor': 'pointer',
                                                    'fontWeight': '500',
                                                    'fontSize': '14px'
                                                }
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
                    html.H3('Аналоги', style={'marginBottom': '20px', 'color': '#007bff'}),

                    html.Div(
                        [
                            create_analogue_card(part) for part in analogue_parts
                        ]
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

                    # Цена и кнопка (справа)
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Button(
                                        'Заказ',
                                        className="btn_style",
                                        style={
                                            'backgroundColor': '#007bff',
                                            'color': 'white',
                                            'border': 'none',
                                            'padding': '10px 24px',
                                            'borderRadius': '6px',
                                            'cursor': 'pointer',
                                            'fontWeight': '500',
                                            'fontSize': '14px'
                                        }
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