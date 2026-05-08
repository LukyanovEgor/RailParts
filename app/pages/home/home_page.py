from .layout import Layout
from dash import ctx, callback, callback_context, Output, Input


layout = Layout()


# Callback для управления видимостью
@callback(
    Output("modal-overlay", "style"),
    Input("show-auth-modal", "n_clicks"),
    Input("close-modal-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_modal(open_clicks, close_clicks):


    ctx = callback_context
    if not ctx.triggered:
        return {'display': 'none'}

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "show-auth-modal":
        return {
            'position': 'fixed',
            'top': 0, 'left': 0, 'right': 0, 'bottom': 0,
            'backgroundColor': 'rgba(0,0,0,0.5)',
            'zIndex': 9999,
            'display': 'flex',
            'justifyContent': 'flex-end',
            'alignItems': 'flex-start',
        }
    else:
        return {'display': 'none'}