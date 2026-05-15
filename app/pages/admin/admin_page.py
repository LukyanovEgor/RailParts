from .layout import Layout
from dash import Output, Input, callback, html

layout = Layout()


@callback(
    Output("order-table", "children"),
    Input("data-refresh-interval", "data"),
    prevent_initial_call=False
)
def render_table(data):

    return html.Div('f')