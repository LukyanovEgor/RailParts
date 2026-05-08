from dash import html


SWITCH = html.Div(
    className="tab-switcher",
    role="tablist",
    id="switch",
    **{"aria-orientation": "horizontal", "data-orientation": "horizontal"},
    tabIndex='0',
    children=[
        html.Button(
            [html.Img(src='/assets/it/switch/review.svg'), html.Span("По электронной почте")],
            className="tab-button", role="tab", id="tab-overview", tabIndex='-1', n_clicks=0,
            **{"aria-selected": "true", "data-state": "active"}
        ),
        html.Button(
            [html.Img(src='/assets/it/switch/by_service.svg'), html.Span("По номеру телефона")],
            className="tab-button", role="tab", id="tab-services", tabIndex='-1', n_clicks=0,
            **{"aria-selected": "false", "data-state": "inactive"}
        )
    ]
)