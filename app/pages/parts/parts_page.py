import dash
from dash import html, dcc, callback, Input, Output, ctx, ALL
from app.models import OEMParts, AnalogueParts
from sqlalchemy import func
from .layout import Layout
from app.db import get_db
import random


layout = Layout()

def render_cards(items):
    if not items:
        return html.Div("Товары не найдены", className="empty")
    cards = []
    for p in items:
        cards.append(
            html.Div(
                children = [
                    html.Img(src=p["img"], className="card-img"),
                    html.Div(f"{p['code']}  Код товара: {p['article']}", className="meta"),
                    html.Div(p["name"], className="title")
                ], className="card",
                style={"padding": "40px"}
            )
        )
    return cards

def format_for_cards(parts):

    part_list = []
    for p in parts:
        try:
            part =  {
                "name": p.name,
                "code": p.oem_num,
                "article": p.oem_num,
                "img": p.img_url if p.img_url else "/assets/no_icon_part.png",
                "id": p.id
                # добавьте другие поля, если render_cards их требует
            }
        except AttributeError:

            part = {
                "name": p.name,
                "code": p.analogue_num,
                "article": p.analogue_num,
                 "img": p.img_url if p.img_url else "/assets/no_icon_part.png",
                "id": p.id
                # добавьте другие поля, если render_cards их требует
            }

        part_list.append(part)

    return part_list

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
        # 🎲 Первая загрузка -> 8 случайных записей из БД
        if not triggered:
            random_parts = db.query(OEMParts).order_by(func.random()).limit(8).all()
            return render_cards(format_for_cards(random_parts))

        # 🔍 Поиск по вводу
        if search_val and search_val.strip():
            query = search_val.strip()
            # case-insensitive поиск по названию и артикулу
            results_oem = db.query(OEMParts).filter(
                (OEMParts.name.ilike(f"%{query}%")) |
                (OEMParts.oem_num.ilike(f"%{query}%"))
            ).all()

            results_analogue = db.query(AnalogueParts).filter(
                (AnalogueParts.name.ilike(f"%{query}%")) |
                (AnalogueParts.analogue_num.ilike(f"%{query}%"))
            ).all()

            results = results_oem + results_analogue

            return render_cards(format_for_cards(results))

        random_parts = db.query(AnalogueParts).order_by(func.random()).limit(8).all()
        return render_cards(format_for_cards(random_parts))

    finally:
        db.close()