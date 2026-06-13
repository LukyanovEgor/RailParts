from dash import html


ORDERS_SWITCH = html.Div(
    className="tab-switcher",
    role="tablist",
    id="orders-switch",
    **{"aria-orientation": "horizontal", "data-orientation": "horizontal"},
    tabIndex='0',
    children=[
        html.Button(
            [html.Img(src='/assets/it/switch/review.svg'),
             html.Span("Все заказы")],
            className="tab-button", role="tab", id="all-type", tabIndex='-1', n_clicks=0,
            **{"aria-selected": "true", "data-state": "active"}
        ),
        html.Button(
            [html.Img(src='/assets/it/switch/by_service.svg'),
             html.Span("По пользователю")],
            className="tab-button", role="tab", id="by-user-type", tabIndex='-1', n_clicks=0,
            **{"aria-selected": "false", "data-state": "inactive"}
        )
    ]
)
